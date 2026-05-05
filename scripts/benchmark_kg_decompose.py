"""Benchmark: Enhanced KG with Query Decomposition.

For complex/multi-hop queries, decomposes into sub-questions, retrieves
KG context for each independently, merges results, then generates.

Compares against the enhanced KG baseline (91% fact coverage) to measure
the uplift from decomposition on relational and troubleshooting queries.

Usage:
    python scripts/benchmark_kg_decompose.py -v
    python scripts/benchmark_kg_decompose.py --output tests/results_kg_decompose.json
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
from pydantic import BaseModel, Field

from logicbroker_agent.graph import GeneratedAnswer, HallucinationVerdict
from logicbroker_agent.kg_enhanced import EnhancedKnowledgeGraphRetriever

sys.path.insert(0, str(Path(__file__).parent))
from benchmark_e2e import BENCHMARK, QueryResult, check_facts_in_answer, print_summary, results_to_json

logger = logging.getLogger(__name__)


# --- Query Decomposition ---


class DecomposedQuery(BaseModel):
    """A complex query split into simpler sub-questions."""

    is_complex: bool = Field(
        description="Whether this query requires decomposition (multi-hop, multi-entity, process questions)"
    )
    sub_questions: list[str] = Field(
        default_factory=list,
        description="2-4 simpler sub-questions that together answer the original query",
    )


DECOMPOSE_SYSTEM = """\
You are a query analyzer for a Logicbroker knowledge base. Your job is to determine \
if a query is complex (requires multiple pieces of information from different parts of \
the knowledge graph) and if so, decompose it into simpler sub-questions.

A query is complex if it:
- Asks about a multi-step process or lifecycle
- Combines multiple distinct concepts (e.g. "What is X and how does Y relate to it?")
- Asks about transitions, flows, or sequences
- Requires knowing about multiple entities and their relationships

A query is simple if it:
- Asks about a single concept, definition, or entity
- Can be answered with a single lookup
- Asks for a list of options or features

When decomposing, create 2-4 sub-questions that:
- Are self-contained (each makes sense on its own)
- Cover all parts of the original query
- Are specific enough for targeted retrieval
- Don't overlap significantly"""


def decompose_query(query: str) -> list[str]:
    """Decompose a complex query into sub-questions. Returns [query] if simple."""
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=300)
    structured_llm = llm.with_structured_output(DecomposedQuery)

    result = structured_llm.invoke([
        SystemMessage(content=DECOMPOSE_SYSTEM),
        HumanMessage(content=f"Analyze and optionally decompose this query:\n\n{query}"),
    ])

    if result.is_complex and result.sub_questions:
        return result.sub_questions
    return [query]


# --- Retrieval with decomposition ---


def retrieve_with_decomposition(
    query: str,
    kg_retriever: EnhancedKnowledgeGraphRetriever,
) -> tuple[list[dict], list[str]]:
    """Retrieve KG context, decomposing the query if complex.

    Returns (docs, sub_questions) where sub_questions is [query] if not decomposed.
    """
    sub_questions = decompose_query(query)

    all_results = []
    seen_edges = set()

    for sub_q in sub_questions:
        kg_results = kg_retriever.query(sub_q, max_results=20, max_hops=3)
        for r in kg_results:
            if r not in seen_edges:
                seen_edges.add(r)
                all_results.append(r)

    if not all_results:
        return [], sub_questions

    kg_text = "Knowledge Graph relationships:\n" + "\n".join(f"• {r}" for r in all_results)
    docs = [{
        "text": kg_text,
        "title": "Enhanced Knowledge Graph (decomposed query retrieval)",
        "source_url": "",
        "category": "knowledge_graph",
        "doc_type": "kg_edges",
        "chunk_index": 0,
        "total_chunks": 1,
        "score": 1.0,
    }]

    return docs, sub_questions


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


def run_pipeline(query: str, kg_retriever: EnhancedKnowledgeGraphRetriever) -> dict:
    """Run the full decomposition pipeline."""
    docs, sub_questions = retrieve_with_decomposition(query, kg_retriever)
    gen = generate_answer(query, docs)
    grounded = check_hallucination(query, gen["answer"], docs) if gen["answer"] else False

    return {
        "answer": gen["answer"],
        "sources": gen["sources"],
        "grounded": grounded,
        "doc_count": len(docs),
        "sub_questions": sub_questions,
        "was_decomposed": len(sub_questions) > 1,
    }


def run_benchmark(
    categories: list[str] | None = None,
    verbose: bool = False,
) -> list[QueryResult]:
    """Run all benchmark queries through the decomposition pipeline."""
    kg_retriever = EnhancedKnowledgeGraphRetriever()
    print(f"Enhanced KG loaded: {kg_retriever.node_count} nodes, {kg_retriever.community_count} communities")
    print("Using query decomposition for complex queries\n")

    queries = BENCHMARK
    if categories:
        cats = {c.lower() for c in categories}
        queries = [q for q in queries if q["category"].lower() in cats]

    results = []
    decomposed_count = 0

    for i, bench in enumerate(queries):
        query = bench["query"]
        if verbose:
            print(f"\nQ{i+1:02d} [{bench['category']}]: {query}")

        start = time.time()
        try:
            state = run_pipeline(query, kg_retriever)
            duration = time.time() - start

            if state["was_decomposed"]:
                decomposed_count += 1
                if verbose:
                    print(f"  Decomposed into {len(state['sub_questions'])} sub-questions:")
                    for sq in state["sub_questions"]:
                        print(f"    → {sq}")

            answer = state.get("answer", "")
            fact_details = check_facts_in_answer(answer, bench["key_facts"])
            facts_found = sum(1 for _, f in fact_details if f)

            result = QueryResult(
                query=query,
                category=bench["category"],
                expected_classification=bench["expected_classification"],
                actual_classification="kg-decomposed",
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
                actual_classification="kg-decomposed",
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

    print(f"\n  Queries decomposed: {decomposed_count}/{len(results)}")
    return results


def print_comparison(results: list[QueryResult]):
    """Print comparison against enhanced KG baseline (without decomposition)."""
    baseline = {
        "fact_coverage": (39, 43),
        "grounding_rate": 0.93,
        "avg_latency": 19.1,
        "per_category": {
            "Relational": 0.90,
            "Factual": 0.88,
            "API": 1.00,
            "Troubleshooting": 0.71,
            "Conceptual": 1.00,
        }
    }

    total_facts_found = sum(r.facts_found for r in results)
    total_facts = sum(r.facts_total for r in results)
    grounded_count = sum(1 for r in results if r.grounded)
    avg_latency = sum(r.duration_secs for r in results) / len(results)

    from collections import defaultdict
    cat_facts = defaultdict(lambda: [0, 0])
    for r in results:
        cat_facts[r.category][0] += r.facts_found
        cat_facts[r.category][1] += r.facts_total

    print("\n" + "=" * 70)
    print("COMPARISON: KG + Query Decomposition vs Enhanced KG (no decomposition)")
    print("=" * 70)
    print(f"\n{'Metric':<25} {'Enhanced KG':<20} {'+ Decomposition':<20} {'Delta':<10}")
    print("-" * 70)

    bl_fc = baseline["fact_coverage"]
    print(f"{'Fact Coverage':<25} {bl_fc[0]}/{bl_fc[1]} ({bl_fc[0]/bl_fc[1]*100:.0f}%)"
          f"{'':>4} {total_facts_found}/{total_facts} ({total_facts_found/total_facts*100:.0f}%)"
          f"{'':>4} {'+' if total_facts_found > bl_fc[0] else ''}{total_facts_found - bl_fc[0]}")

    gr_pct = grounded_count / len(results) * 100
    bl_gr = baseline["grounding_rate"] * 100
    print(f"{'Grounding Rate':<25} {bl_gr:.0f}%{'':>15} {gr_pct:.0f}%{'':>15} "
          f"{'+' if gr_pct > bl_gr else ''}{gr_pct - bl_gr:.0f}%")

    print(f"{'Avg Latency':<25} {baseline['avg_latency']:.1f}s{'':>14} {avg_latency:.1f}s")

    print(f"\n{'Category':<20} {'Enhanced KG':<12} {'+ Decomp':<12} {'Delta':<10}")
    print("-" * 55)
    for cat, bl_pct in baseline["per_category"].items():
        if cat_facts[cat][1] > 0:
            new_pct = cat_facts[cat][0] / cat_facts[cat][1]
            delta = new_pct - bl_pct
            print(f"{cat:<20} {bl_pct*100:.0f}%{'':>9} {new_pct*100:.0f}%{'':>9} "
                  f"{'+' if delta > 0 else ''}{delta*100:.0f}%")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="KG benchmark with query decomposition")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show per-query details")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--output", type=str, help="Write JSON results to file")
    args = parser.parse_args()

    categories = [args.category] if args.category else None

    print(f"Running {len(BENCHMARK)} queries through KG + QUERY DECOMPOSITION pipeline...")
    print("(Complex queries decomposed → independent KG retrieval per sub-question → merge → generate)\n")
    results = run_benchmark(categories=categories, verbose=args.verbose)

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
