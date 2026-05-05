"""Compare KG retrieval quality: MiniLM vs OpenAI embeddings.

Both use the same Enhanced KG pipeline (hybrid node matching + community
summaries + path scoring). The only difference is the embedding model:
- MiniLM: all-MiniLM-L6-v2 (local, 384-dim, free)
- OpenAI: text-embedding-3-small (API, 1536-dim, paid)

Usage:
    python scripts/benchmark_kg_embeddings_compare.py -v
    python scripts/benchmark_kg_embeddings_compare.py --llm-summaries
    python scripts/benchmark_kg_embeddings_compare.py --output tests/results_kg_embeddings_compare.json
"""

import json
import logging
import sys
import time
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from logicbroker_agent.graph import GeneratedAnswer, HallucinationVerdict
from logicbroker_agent.kg_enhanced import EnhancedKnowledgeGraphRetriever
from logicbroker_agent.kg_openai import OpenAIKnowledgeGraphRetriever
from benchmark_e2e import BENCHMARK, QueryResult, check_facts_in_answer, print_summary, results_to_json

logger = logging.getLogger(__name__)


def retrieve_kg(query: str, kg_retriever) -> list[dict]:
    """Retrieve context using a KG retriever (either MiniLM or OpenAI)."""
    kg_results = kg_retriever.query(query, max_results=30, max_hops=3)

    if not kg_results:
        return []

    kg_text = "Knowledge Graph relationships:\n" + "\n".join(f"• {r}" for r in kg_results)
    return [{
        "text": kg_text,
        "title": "Knowledge Graph (embeddings + communities)",
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


def run_pipeline(query: str, kg_retriever) -> dict:
    """Run the full pipeline with a given KG retriever."""
    docs = retrieve_kg(query, kg_retriever)
    gen = generate_answer(query, docs)
    grounded = check_hallucination(query, gen["answer"], docs) if gen["answer"] else False

    return {
        "answer": gen["answer"],
        "sources": gen["sources"],
        "grounded": grounded,
        "doc_count": len(docs),
    }


def run_benchmark_for_retriever(
    name: str,
    kg_retriever,
    verbose: bool = False,
) -> list[QueryResult]:
    """Run all benchmark queries through a given KG retriever."""
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"  Nodes: {kg_retriever.node_count}, Communities: {kg_retriever.community_count}")
    print(f"{'='*60}")

    results = []
    for i, bench in enumerate(BENCHMARK):
        query = bench["query"]
        if verbose:
            print(f"\n  Q{i+1:02d} [{bench['category']}]: {query}")

        start = time.time()
        try:
            state = run_pipeline(query, kg_retriever)
            duration = time.time() - start

            answer = state.get("answer", "")
            fact_details = check_facts_in_answer(answer, bench["key_facts"])
            facts_found = sum(1 for _, f in fact_details if f)

            result = QueryResult(
                query=query,
                category=bench["category"],
                expected_classification=bench["expected_classification"],
                actual_classification=name,
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
                actual_classification=name,
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
            print(f"    [{status}] {result.facts_found}/{result.facts_total} facts | "
                  f"grounded={result.grounded} | {result.duration_secs:.1f}s")
            for desc, found in result.fact_details:
                print(f"      {'Y' if found else 'N'} {desc}")
            if result.error:
                print(f"    ERROR: {result.error}")

    return results


def compute_metrics(results: list[QueryResult]) -> dict:
    """Compute aggregate metrics from results."""
    total_facts_found = sum(r.facts_found for r in results)
    total_facts = sum(r.facts_total for r in results)
    grounded_count = sum(1 for r in results if r.grounded)
    avg_latency = sum(r.duration_secs for r in results) / len(results)

    cat_facts = defaultdict(lambda: [0, 0])
    cat_grounded = defaultdict(lambda: [0, 0])
    for r in results:
        cat_facts[r.category][0] += r.facts_found
        cat_facts[r.category][1] += r.facts_total
        cat_grounded[r.category][0] += 1 if r.grounded else 0
        cat_grounded[r.category][1] += 1

    return {
        "facts_found": total_facts_found,
        "facts_total": total_facts,
        "fact_pct": total_facts_found / total_facts * 100,
        "grounded_count": grounded_count,
        "grounded_total": len(results),
        "grounding_pct": grounded_count / len(results) * 100,
        "avg_latency": avg_latency,
        "per_category": {
            cat: {
                "fact_pct": cat_facts[cat][0] / cat_facts[cat][1] * 100 if cat_facts[cat][1] > 0 else 0,
                "grounding_pct": cat_grounded[cat][0] / cat_grounded[cat][1] * 100 if cat_grounded[cat][1] > 0 else 0,
            }
            for cat in sorted(cat_facts.keys())
        },
    }


def print_comparison(minilm_metrics: dict, openai_metrics: dict):
    """Print a side-by-side comparison table."""
    print("\n" + "=" * 75)
    print("COMPARISON: MiniLM (all-MiniLM-L6-v2) vs OpenAI (text-embedding-3-small)")
    print("=" * 75)

    print(f"\n{'Metric':<25} {'MiniLM':<20} {'OpenAI':<20} {'Delta':<10}")
    print("-" * 75)

    # Fact coverage
    ml_fc = f"{minilm_metrics['facts_found']}/{minilm_metrics['facts_total']} ({minilm_metrics['fact_pct']:.0f}%)"
    oa_fc = f"{openai_metrics['facts_found']}/{openai_metrics['facts_total']} ({openai_metrics['fact_pct']:.0f}%)"
    delta_fc = openai_metrics['facts_found'] - minilm_metrics['facts_found']
    print(f"{'Fact Coverage':<25} {ml_fc:<20} {oa_fc:<20} {'+' if delta_fc > 0 else ''}{delta_fc}")

    # Grounding
    ml_gr = f"{minilm_metrics['grounding_pct']:.0f}%"
    oa_gr = f"{openai_metrics['grounding_pct']:.0f}%"
    delta_gr = openai_metrics['grounding_pct'] - minilm_metrics['grounding_pct']
    print(f"{'Grounding Rate':<25} {ml_gr:<20} {oa_gr:<20} {'+' if delta_gr > 0 else ''}{delta_gr:.0f}%")

    # Latency
    ml_lat = f"{minilm_metrics['avg_latency']:.1f}s"
    oa_lat = f"{openai_metrics['avg_latency']:.1f}s"
    delta_lat = openai_metrics['avg_latency'] - minilm_metrics['avg_latency']
    print(f"{'Avg Latency':<25} {ml_lat:<20} {oa_lat:<20} {'+' if delta_lat > 0 else ''}{delta_lat:.1f}s")

    # Per-category
    print(f"\n{'Category':<20} {'MiniLM Facts':<15} {'OpenAI Facts':<15} {'Delta':<10}")
    print("-" * 60)

    all_cats = sorted(set(list(minilm_metrics['per_category'].keys()) + list(openai_metrics['per_category'].keys())))
    for cat in all_cats:
        ml_pct = minilm_metrics['per_category'].get(cat, {}).get('fact_pct', 0)
        oa_pct = openai_metrics['per_category'].get(cat, {}).get('fact_pct', 0)
        delta = oa_pct - ml_pct
        print(f"{cat:<20} {ml_pct:.0f}%{'':>11} {oa_pct:.0f}%{'':>11} {'+' if delta > 0 else ''}{delta:.0f}%")

    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Compare MiniLM vs OpenAI embeddings for KG retrieval")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show per-query details")
    parser.add_argument("--output", type=str, help="Write JSON results to file")
    parser.add_argument("--llm-summaries", action="store_true",
                        help="Use LLM community summaries (costs API credits)")
    args = parser.parse_args()

    print("Initializing retrievers...")

    # MiniLM retriever
    print("\n  Loading MiniLM (all-MiniLM-L6-v2)...")
    minilm_retriever = EnhancedKnowledgeGraphRetriever()

    # OpenAI retriever
    print("  Loading OpenAI (text-embedding-3-small)...")
    openai_retriever = OpenAIKnowledgeGraphRetriever()

    if args.llm_summaries:
        print("\n  Building LLM community summaries...")
        minilm_retriever.build_llm_community_summaries()
        openai_retriever.build_llm_community_summaries()

    # Run benchmarks
    minilm_results = run_benchmark_for_retriever("MiniLM", minilm_retriever, verbose=args.verbose)
    openai_results = run_benchmark_for_retriever("OpenAI", openai_retriever, verbose=args.verbose)

    # Compute metrics and compare
    minilm_metrics = compute_metrics(minilm_results)
    openai_metrics = compute_metrics(openai_results)
    print_comparison(minilm_metrics, openai_metrics)

    # Per-query head-to-head
    print("\nPer-Query Head-to-Head (queries where results differ):")
    print("-" * 75)
    print(f"{'Q#':<5} {'Category':<15} {'MiniLM':<20} {'OpenAI':<20} {'Winner':<10}")
    print("-" * 75)
    for i, (ml, oa) in enumerate(zip(minilm_results, openai_results)):
        if ml.facts_found != oa.facts_found or ml.grounded != oa.grounded:
            ml_str = f"{ml.facts_found}/{ml.facts_total} {'G' if ml.grounded else 'U'}"
            oa_str = f"{oa.facts_found}/{oa.facts_total} {'G' if oa.grounded else 'U'}"
            if oa.facts_found > ml.facts_found:
                winner = "OpenAI"
            elif ml.facts_found > oa.facts_found:
                winner = "MiniLM"
            else:
                winner = "Tie"
            print(f"Q{i+1:02d}  {ml.category:<15} {ml_str:<20} {oa_str:<20} {winner:<10}")
    print()

    if args.output:
        output_data = {
            "minilm": {
                "metrics": minilm_metrics,
                "results": results_to_json(minilm_results),
            },
            "openai": {
                "metrics": openai_metrics,
                "results": results_to_json(openai_results),
            },
        }
        output_path = Path(args.output)
        output_path.write_text(json.dumps(output_data, indent=2))
        print(f"Results written to {output_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
