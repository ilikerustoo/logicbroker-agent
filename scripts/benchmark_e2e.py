"""End-to-end benchmark for the Logicbroker hybrid RAG pipeline.

Runs 15 queries through the full agent (classify → retrieve → grade →
generate → hallucination check) and scores answers against expected facts.

Measures:
- Answer quality: key facts present in generated answer
- Classification accuracy
- Grounding rate (hallucination check passes)
- Citation quality (sources present)
- Latency per query

Usage:
    python scripts/benchmark_e2e.py              # run all, summary only
    python scripts/benchmark_e2e.py -v           # verbose per-query output
    python scripts/benchmark_e2e.py --json       # output JSON results
    python scripts/benchmark_e2e.py --category Relational  # filter by category
"""

import asyncio
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from logicbroker_agent.graph import run_agent

# ---------------------------------------------------------------------------
# Benchmark queries — same 15 as retrieval benchmark, with expected category
# and answer-level key facts (not just retrieval-level)
# ---------------------------------------------------------------------------

BENCHMARK = [
    # === Relational/Workflow ===
    {
        "category": "Relational",
        "expected_classification": "order-lifecycle",
        "query": "What status does an order move to after acknowledgement, and how does a supplier send one?",
        "key_facts": [
            (["150", "ready to acknowledge"], "Mentions status 150"),
            (["500", "ready to ship"], "Mentions status 500 after acknowledgement"),
            (["acknowledgement", "acknowledgment"], "Explains acknowledgement process"),
        ],
    },
    {
        "category": "Relational",
        "expected_classification": "order-lifecycle",
        "query": "What is the full document lifecycle for a typical order from creation to invoice?",
        "key_facts": [
            (["order"], "Order mentioned"),
            (["acknowledgement", "acknowledgment"], "Acknowledgement step"),
            (["shipment"], "Shipment step"),
            (["invoice"], "Invoice step"),
        ],
    },
    {
        "category": "Relational",
        "expected_classification": "order-lifecycle",
        "query": "What documents does a supplier need to send after receiving an order to complete fulfillment?",
        "key_facts": [
            (["acknowledgement", "acknowledgment"], "Acknowledgement required"),
            (["shipment"], "Shipment required"),
            (["invoice"], "Invoice required"),
        ],
    },

    # === Factual/Detail ===
    {
        "category": "Factual",
        "expected_classification": "onboarding",
        "query": "What connection options are available for suppliers in Logicbroker?",
        "key_facts": [
            (["portal", "web portal"], "Web Portal option"),
            (["api"], "API option"),
            (["edi"], "EDI option"),
        ],
    },
    {
        "category": "Factual",
        "expected_classification": "order-lifecycle",
        "query": "What is a linkkey in Logicbroker and what does it do?",
        "key_facts": [
            (["linkkey", "link key"], "LinkKey mentioned"),
            (["link", "group", "relate", "connect", "ties", "associate"],
             "Explains linking/grouping function"),
        ],
    },
    {
        "category": "Factual",
        "expected_classification": "edi-technical",
        "query": "What EDI formats does Logicbroker support for connections?",
        "key_facts": [
            (["as2"], "AS2 format"),
            (["ftp", "sftp"], "FTP/SFTP"),
            (["edi"], "EDI mentioned"),
        ],
    },

    # === API-specific ===
    {
        "category": "API",
        "expected_classification": "api-integration",
        "query": "How do I search for shipments by status using the API?",
        "key_facts": [
            (["shipment"], "Shipments endpoint"),
            (["status", "filter"], "Status filtering"),
            (["api", "get", "endpoint"], "API method reference"),
        ],
    },
    {
        "category": "API",
        "expected_classification": "api-integration",
        "query": "How do I create a webhook in Logicbroker's API?",
        "key_facts": [
            (["webhook"], "Webhook mentioned"),
            (["api", "post", "endpoint", "create"], "API creation method"),
        ],
    },
    {
        "category": "API",
        "expected_classification": "api-integration",
        "query": "What are the rate limits for the Logicbroker API?",
        "key_facts": [
            (["rate limit"], "Rate limit concept"),
            (["2 second", "1 request every 2", "1.*2 second"], "Search rate limit"),
            (["10 request", "10.*per second"], "General rate limit"),
        ],
    },

    # === Troubleshooting ===
    {
        "category": "Troubleshooting",
        "expected_classification": "platform-config",
        "query": "What does the Events page show and how do I use it to diagnose document failures?",
        "key_facts": [
            (["event"], "Events page"),
            (["error", "failure", "alert", "noncompliant"], "Error/failure visibility"),
        ],
    },
    {
        "category": "Troubleshooting",
        "expected_classification": "onboarding",
        "query": "What test cases does Logicbroker support for supplier onboarding?",
        "key_facts": [
            (["fulfillment", "order fulfillment"], "Fulfillment test"),
            (["cancellation", "cancel"], "Cancellation test"),
        ],
    },
    {
        "category": "Troubleshooting",
        "expected_classification": "edi-technical",
        "query": "How does a supplier set up an EDI connection with Logicbroker?",
        "key_facts": [
            (["edi"], "EDI mentioned"),
            (["as2", "ftp", "sftp"], "Transport protocol"),
            (["connection", "set up", "configure", "onboard"], "Setup process"),
        ],
    },

    # === Conceptual ===
    {
        "category": "Conceptual",
        "expected_classification": "general",
        "query": "What is Logicbroker and what problem does it solve?",
        "key_facts": [
            (["integration", "platform", "supply chain", "commerce"],
             "Platform description"),
            (["retailer"], "Retailers"),
            (["supplier"], "Suppliers"),
        ],
    },
    {
        "category": "Conceptual",
        "expected_classification": "order-lifecycle",
        "query": "What document types exist in Logicbroker?",
        "key_facts": [
            (["order"], "Order"),
            (["acknowledgement", "acknowledgment"], "Acknowledgement"),
            (["shipment"], "Shipment"),
            (["invoice"], "Invoice"),
            (["return"], "Return"),
        ],
    },
    {
        "category": "Conceptual",
        "expected_classification": "general",
        "query": "What is the difference between a retailer and a supplier in Logicbroker?",
        "key_facts": [
            (["retailer"], "Retailer role explained"),
            (["supplier"], "Supplier role explained"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@dataclass
class QueryResult:
    query: str
    category: str
    expected_classification: str
    actual_classification: str
    classification_correct: bool
    facts_found: int
    facts_total: int
    fact_details: list[tuple[str, bool]]
    grounded: bool
    has_sources: bool
    source_count: int
    answer_length: int
    duration_secs: float
    error: str = ""


def check_facts_in_answer(answer: str, key_facts: list) -> list[tuple[str, bool]]:
    """Check which key facts appear in the generated answer."""
    answer_lower = answer.lower()
    results = []
    for needles, desc in key_facts:
        found = False
        for needle in needles:
            if ".*" in needle:
                if re.search(needle, answer_lower):
                    found = True
                    break
            elif needle.lower() in answer_lower:
                found = True
                break
        results.append((desc, found))
    return results


def run_benchmark(categories: list[str] | None = None, verbose: bool = False) -> list[QueryResult]:
    """Run all benchmark queries through the full agent pipeline."""
    queries = BENCHMARK
    if categories:
        cats = {c.lower() for c in categories}
        queries = [q for q in queries if q["category"].lower() in cats]

    results = []
    for i, bench in enumerate(queries):
        query = bench["query"]
        if verbose:
            print(f"\nQ{i+1:02d} [{bench['category']}]: {query}")

        start = time.time()
        try:
            state = asyncio.run(run_agent(query))
            duration = time.time() - start

            answer = state.get("answer", "")
            fact_details = check_facts_in_answer(answer, bench["key_facts"])
            facts_found = sum(1 for _, f in fact_details if f)

            result = QueryResult(
                query=query,
                category=bench["category"],
                expected_classification=bench["expected_classification"],
                actual_classification=state.get("query_type", ""),
                classification_correct=state.get("query_type") == bench["expected_classification"],
                facts_found=facts_found,
                facts_total=len(bench["key_facts"]),
                fact_details=fact_details,
                grounded=state.get("grounded", False),
                has_sources=len(state.get("sources", [])) > 0,
                source_count=len(state.get("sources", [])),
                answer_length=len(answer),
                duration_secs=duration,
            )
        except Exception as e:
            duration = time.time() - start
            result = QueryResult(
                query=query,
                category=bench["category"],
                expected_classification=bench["expected_classification"],
                actual_classification="",
                classification_correct=False,
                facts_found=0,
                facts_total=len(bench["key_facts"]),
                fact_details=[(desc, False) for _, desc in bench["key_facts"]],
                grounded=False,
                has_sources=False,
                source_count=0,
                answer_length=0,
                duration_secs=duration,
                error=str(e),
            )

        results.append(result)

        if verbose:
            status = "PASS" if result.grounded else "FAIL"
            cls = "OK" if result.classification_correct else f"WRONG({result.actual_classification})"
            print(f"  [{status}] {result.facts_found}/{result.facts_total} facts | "
                  f"class={cls} | grounded={result.grounded} | "
                  f"sources={result.source_count} | {result.duration_secs:.1f}s")
            for desc, found in result.fact_details:
                print(f"    {'Y' if found else 'N'} {desc}")
            if result.error:
                print(f"  ERROR: {result.error}")

    return results


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_summary(results: list[QueryResult]):
    """Print a summary table and category breakdown."""
    print("\n" + "=" * 90)
    print("END-TO-END BENCHMARK RESULTS")
    print("=" * 90)

    # Per-query table
    header = f"{'#':<5}{'Category':<16}{'Facts':<8}{'Class':<8}{'Ground':<8}{'Srcs':<6}{'Time':<7}Query"
    print(f"\n{header}")
    print("-" * 90)

    for i, r in enumerate(results):
        query_short = r.query[:35] + "..." if len(r.query) > 35 else r.query
        cls = "OK" if r.classification_correct else "X"
        gnd = "Y" if r.grounded else "N"
        print(f"Q{i+1:02d}  {r.category:<16}{r.facts_found}/{r.facts_total:<6}{cls:<8}"
              f"{gnd:<8}{r.source_count:<6}{r.duration_secs:5.1f}s {query_short}")

    # Category breakdown
    print(f"\n{'-' * 90}")
    print("CATEGORY BREAKDOWN")
    print(f"{'-' * 90}")
    print(f"{'Category':<16}{'Fact %':<12}{'Class %':<12}{'Ground %':<12}{'Avg Time':<10}")

    categories = ["Relational", "Factual", "API", "Troubleshooting", "Conceptual"]
    for cat in categories:
        cat_results = [r for r in results if r.category == cat]
        if not cat_results:
            continue

        fact_found = sum(r.facts_found for r in cat_results)
        fact_total = sum(r.facts_total for r in cat_results)
        fact_pct = (fact_found / fact_total * 100) if fact_total else 0

        cls_correct = sum(1 for r in cat_results if r.classification_correct)
        cls_pct = cls_correct / len(cat_results) * 100

        gnd_count = sum(1 for r in cat_results if r.grounded)
        gnd_pct = gnd_count / len(cat_results) * 100

        avg_time = sum(r.duration_secs for r in cat_results) / len(cat_results)

        print(f"{cat:<16}{fact_pct:5.0f}%{'':5}{cls_pct:5.0f}%{'':5}"
              f"{gnd_pct:5.0f}%{'':5}{avg_time:5.1f}s")

    # Overall
    print(f"\n{'-' * 90}")
    print("OVERALL")
    print(f"{'-' * 90}")

    total_facts_found = sum(r.facts_found for r in results)
    total_facts = sum(r.facts_total for r in results)
    fact_pct = (total_facts_found / total_facts * 100) if total_facts else 0

    cls_correct = sum(1 for r in results if r.classification_correct)
    cls_pct = cls_correct / len(results) * 100

    grounded = sum(1 for r in results if r.grounded)
    gnd_pct = grounded / len(results) * 100

    avg_time = sum(r.duration_secs for r in results) / len(results)
    total_time = sum(r.duration_secs for r in results)

    errors = sum(1 for r in results if r.error)

    print(f"  Fact coverage:     {total_facts_found}/{total_facts} ({fact_pct:.0f}%)")
    print(f"  Classification:    {cls_correct}/{len(results)} ({cls_pct:.0f}%)")
    print(f"  Grounding rate:    {grounded}/{len(results)} ({gnd_pct:.0f}%)")
    print(f"  Avg latency:       {avg_time:.1f}s per query")
    print(f"  Total time:        {total_time:.0f}s")
    if errors:
        print(f"  Errors:            {errors}")


def results_to_json(results: list[QueryResult]) -> dict:
    """Convert results to a JSON-serializable dict."""
    total_facts_found = sum(r.facts_found for r in results)
    total_facts = sum(r.facts_total for r in results)

    return {
        "summary": {
            "total_queries": len(results),
            "fact_coverage": f"{total_facts_found}/{total_facts}",
            "fact_pct": round(total_facts_found / total_facts * 100, 1) if total_facts else 0,
            "classification_accuracy": round(
                sum(1 for r in results if r.classification_correct) / len(results) * 100, 1
            ),
            "grounding_rate": round(
                sum(1 for r in results if r.grounded) / len(results) * 100, 1
            ),
            "avg_latency_secs": round(
                sum(r.duration_secs for r in results) / len(results), 1
            ),
        },
        "queries": [
            {
                "query": r.query,
                "category": r.category,
                "classification": {
                    "expected": r.expected_classification,
                    "actual": r.actual_classification,
                    "correct": r.classification_correct,
                },
                "facts": {
                    "found": r.facts_found,
                    "total": r.facts_total,
                    "details": [{"desc": desc, "found": found} for desc, found in r.fact_details],
                },
                "grounded": r.grounded,
                "sources": r.source_count,
                "answer_length": r.answer_length,
                "duration_secs": round(r.duration_secs, 1),
                "error": r.error or None,
            }
            for r in results
        ],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="End-to-end benchmark for Logicbroker RAG agent")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show per-query details")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--category", type=str, help="Filter by category (e.g. Relational, API)")
    parser.add_argument("--output", type=str, help="Write JSON results to file")
    args = parser.parse_args()

    categories = [args.category] if args.category else None

    print(f"Running {len(BENCHMARK)} queries through the full RAG pipeline...")
    results = run_benchmark(categories=categories, verbose=args.verbose)

    if args.json:
        data = results_to_json(results)
        print(json.dumps(data, indent=2))
    else:
        print_summary(results)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(results_to_json(results), indent=2))
        print(f"\nResults written to {output_path}")


if __name__ == "__main__":
    main()
