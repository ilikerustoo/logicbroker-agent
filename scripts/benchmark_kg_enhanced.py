"""Benchmark using the Enhanced Knowledge Graph (embeddings + community summaries).

Compares against the baseline KG-only results to measure improvement from:
1. Embedding-based node lookup (replacing keyword matching)
2. Community detection with summaries (capturing multi-hop relationships)

Usage:
    python scripts/benchmark_kg_enhanced.py -v
    python scripts/benchmark_kg_enhanced.py --output tests/results_kg_enhanced.json
    python scripts/benchmark_kg_enhanced.py --llm-summaries  # use LLM for community summaries
"""

import json
import logging
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from logicbroker_agent.graph import GeneratedAnswer, HallucinationVerdict
from logicbroker_agent.kg_enhanced import EnhancedKnowledgeGraphRetriever

# Reuse benchmark queries and scoring from the main benchmark
sys.path.insert(0, str(Path(__file__).parent))
from benchmark_e2e import BENCHMARK, QueryResult, check_facts_in_answer, print_summary, results_to_json

logger = logging.getLogger(__name__)


def retrieve_kg_enhanced(query: str, kg_retriever: EnhancedKnowledgeGraphRetriever) -> list[dict]:
    """Retrieve context using the enhanced knowledge graph."""
    kg_results = kg_retriever.query(query, max_results=30, max_hops=3)

    if not kg_results:
        return []

    kg_text = "Knowledge Graph relationships:\n" + "\n".join(f"• {r}" for r in kg_results)
    return [{
        "text": kg_text,
        "title": "Enhanced Knowledge Graph (embeddings + communities)",
        "source_url": "",
        "category": "knowledge_graph",
        "doc_type": "kg_edges",
        "chunk_index": 0,
        "total_chunks": 1,
        "score": 1.0,
    }]


def generate_answer(query: str, docs: list[dict]) -> dict:
    """Generate a grounded answer from retrieved docs."""
    if not docs:
        return {"answer": "", "sources": []}

    context_parts = []
    for i, doc in enumerate(docs, 1):
        context_parts.append(f"[Source {i}: {doc['title']}]\n{doc['text']}")
    context_block = "\n\n---\n\n".join(context_parts)

    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=1024)
    structured_llm = llm.with_structured_output(GeneratedAnswer)

    result = structured_llm.invoke([
        SystemMessage(content=(
            "You are a Logicbroker support agent. Answer the user's question using ONLY "
            "the provided source documents (knowledge graph relationships and community summaries). "
            "Follow these rules:\n\n"
            "1. Every factual claim must cite its source using [N] notation.\n"
            "2. If the sources don't contain enough information, say so explicitly.\n"
            "3. Be concise and direct.\n\n"
            f"Source documents:\n\n{context_block}"
        )),
        HumanMessage(content=query),
    ])

    sources = [{"title": c.source_title, "url": c.source_url} for c in result.citations]
    return {"answer": result.answer, "sources": sources}


def check_hallucination(query: str, answer: str, docs: list[dict]) -> bool:
    """Check if the answer is grounded in sources."""
    if not docs or not answer:
        return False

    source_text = "\n\n---\n\n".join(
        f"[{doc['title']}]\n{doc['text']}" for doc in docs
    )

    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=1024)
    structured_llm = llm.with_structured_output(HallucinationVerdict)

    result = structured_llm.invoke([
        SystemMessage(content=(
            "You are a hallucination detector. Given an answer and source documents, "
            "determine whether every factual claim is supported by the sources.\n\n"
            "Mark as grounded if all claims are directly supported.\n"
            "Mark as NOT grounded if specific facts, numbers, or procedures aren't in sources.\n\n"
            f"Source documents:\n\n{source_text}"
        )),
        HumanMessage(content=f"Answer to verify:\n\n{answer}"),
    ])

    return result.grounded


def run_kg_enhanced_pipeline(query: str, kg_retriever: EnhancedKnowledgeGraphRetriever) -> dict:
    """Run the full pipeline with enhanced KG retrieval."""
    docs = retrieve_kg_enhanced(query, kg_retriever)
    gen = generate_answer(query, docs)
    grounded = check_hallucination(query, gen["answer"], docs) if gen["answer"] else False

    return {
        "answer": gen["answer"],
        "sources": gen["sources"],
        "grounded": grounded,
        "doc_count": len(docs),
    }


def run_benchmark(
    categories: list[str] | None = None,
    verbose: bool = False,
    use_llm_summaries: bool = False,
) -> list[QueryResult]:
    """Run all benchmark queries through the enhanced KG pipeline."""
    kg_retriever = EnhancedKnowledgeGraphRetriever()
    print(f"Enhanced KG loaded: {kg_retriever.node_count} nodes, {kg_retriever.community_count} communities")

    if use_llm_summaries:
        print("Building LLM community summaries (this may take a few minutes)...")
        kg_retriever.build_llm_community_summaries()
        print(f"  Done — {kg_retriever.community_count} communities summarized")

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
            state = run_kg_enhanced_pipeline(query, kg_retriever)
            duration = time.time() - start

            answer = state.get("answer", "")
            fact_details = check_facts_in_answer(answer, bench["key_facts"])
            facts_found = sum(1 for _, f in fact_details if f)

            result = QueryResult(
                query=query,
                category=bench["category"],
                expected_classification=bench["expected_classification"],
                actual_classification="kg-enhanced",
                classification_correct=True,
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
                actual_classification="kg-enhanced",
                classification_correct=True,
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
            print(f"  [{status}] {result.facts_found}/{result.facts_total} facts | "
                  f"grounded={result.grounded} | {result.duration_secs:.1f}s")
            for desc, found in result.fact_details:
                print(f"    {'Y' if found else 'N'} {desc}")
            if result.error:
                print(f"  ERROR: {result.error}")

    return results


def print_comparison(enhanced_results: list[QueryResult]):
    """Print comparison against previous KG-only baseline."""
    # Previous KG-only results
    baseline = {
        "fact_coverage": (31, 43),
        "grounding_rate": 0.67,
        "avg_latency": 14.9,
        "per_category": {
            "Relational": 0.70,
            "Factual": 1.00,
            "API": 0.62,
            "Troubleshooting": 0.43,
            "Conceptual": 0.80,
        }
    }

    # Compute enhanced metrics
    total_facts_found = sum(r.facts_found for r in enhanced_results)
    total_facts = sum(r.facts_total for r in enhanced_results)
    grounded_count = sum(1 for r in enhanced_results if r.grounded)
    avg_latency = sum(r.duration_secs for r in enhanced_results) / len(enhanced_results)

    # Per-category
    from collections import defaultdict
    cat_facts = defaultdict(lambda: [0, 0])
    for r in enhanced_results:
        cat_facts[r.category][0] += r.facts_found
        cat_facts[r.category][1] += r.facts_total

    print("\n" + "=" * 70)
    print("COMPARISON: Enhanced KG vs Baseline KG-Only")
    print("=" * 70)
    print(f"\n{'Metric':<25} {'Baseline KG':<20} {'Enhanced KG':<20} {'Delta':<10}")
    print("-" * 70)

    bl_fc = baseline["fact_coverage"]
    print(f"{'Fact Coverage':<25} {bl_fc[0]}/{bl_fc[1]} ({bl_fc[0]/bl_fc[1]*100:.0f}%)"
          f"{'':>4} {total_facts_found}/{total_facts} ({total_facts_found/total_facts*100:.0f}%)"
          f"{'':>4} {'+' if total_facts_found > bl_fc[0] else ''}{total_facts_found - bl_fc[0]}")

    gr_pct = grounded_count / len(enhanced_results) * 100
    bl_gr = baseline["grounding_rate"] * 100
    print(f"{'Grounding Rate':<25} {bl_gr:.0f}%{'':>15} {gr_pct:.0f}%{'':>15} "
          f"{'+' if gr_pct > bl_gr else ''}{gr_pct - bl_gr:.0f}%")

    print(f"{'Avg Latency':<25} {baseline['avg_latency']:.1f}s{'':>14} {avg_latency:.1f}s")

    print(f"\n{'Category':<20} {'Baseline':<12} {'Enhanced':<12} {'Delta':<10}")
    print("-" * 55)
    for cat, bl_pct in baseline["per_category"].items():
        if cat_facts[cat][1] > 0:
            enh_pct = cat_facts[cat][0] / cat_facts[cat][1]
            delta = enh_pct - bl_pct
            print(f"{cat:<20} {bl_pct*100:.0f}%{'':>9} {enh_pct*100:.0f}%{'':>9} "
                  f"{'+' if delta > 0 else ''}{delta*100:.0f}%")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Enhanced KG benchmark (embeddings + communities)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show per-query details")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--output", type=str, help="Write JSON results to file")
    parser.add_argument("--llm-summaries", action="store_true",
                        help="Use LLM to generate community summaries (costs API credits)")
    args = parser.parse_args()

    categories = [args.category] if args.category else None

    print(f"Running {len(BENCHMARK)} queries through ENHANCED KG pipeline...")
    print("(Embedding-based node lookup + community detection + path scoring)\n")
    results = run_benchmark(
        categories=categories,
        verbose=args.verbose,
        use_llm_summaries=args.llm_summaries,
    )

    if args.json:
        data = results_to_json(results)
        print(json.dumps(data, indent=2))
    else:
        print_summary(results)
        print_comparison(results)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(results_to_json(results), indent=2))
        print(f"\nResults written to {output_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
