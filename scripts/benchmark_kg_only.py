"""Benchmark using ONLY the Knowledge Graph for retrieval (no vector search).

Runs the same 15 queries but retrieves context exclusively from the KG,
regardless of query category. Useful for measuring KG coverage in isolation.

Usage:
    python scripts/benchmark_kg_only.py              # summary only
    python scripts/benchmark_kg_only.py -v           # verbose per-query
    python scripts/benchmark_kg_only.py --json       # JSON output
    python scripts/benchmark_kg_only.py --output results_kg.json
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

from logicbroker_agent.graph import (
    AgentState,
    GeneratedAnswer,
    HallucinationVerdict,
)
from logicbroker_agent.retriever import KnowledgeGraphRetriever

# Reuse benchmark queries and scoring from the main benchmark
sys.path.insert(0, str(Path(__file__).parent))
from benchmark_e2e import BENCHMARK, QueryResult, check_facts_in_answer, print_summary, results_to_json

logger = logging.getLogger(__name__)


def retrieve_kg_only(query: str, kg_retriever: KnowledgeGraphRetriever) -> list[dict]:
    """Retrieve context using only the knowledge graph."""
    kg_results = kg_retriever.query(query, max_results=30, max_hops=3)

    if not kg_results:
        return []

    kg_text = "Knowledge Graph relationships:\n" + "\n".join(f"• {r}" for r in kg_results)
    return [{
        "text": kg_text,
        "title": "Knowledge Graph (entity relationships)",
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
        return {"answer": "", "sources": [], "grounded": False}

    context_parts = []
    for i, doc in enumerate(docs, 1):
        context_parts.append(f"[Source {i}: {doc['title']}]\n{doc['text']}")
    context_block = "\n\n---\n\n".join(context_parts)

    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=1024)
    structured_llm = llm.with_structured_output(GeneratedAnswer)

    result = structured_llm.invoke([
        SystemMessage(content=(
            "You are a Logicbroker support agent. Answer the user's question using ONLY "
            "the provided source documents (knowledge graph relationships). Follow these rules:\n\n"
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

    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=512)
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


def run_kg_pipeline(query: str, kg_retriever: KnowledgeGraphRetriever) -> dict:
    """Run the full pipeline with KG-only retrieval."""
    docs = retrieve_kg_only(query, kg_retriever)
    gen = generate_answer(query, docs)
    grounded = check_hallucination(query, gen["answer"], docs) if gen["answer"] else False

    return {
        "answer": gen["answer"],
        "sources": gen["sources"],
        "grounded": grounded,
        "doc_count": len(docs),
    }


def run_benchmark(categories: list[str] | None = None, verbose: bool = False) -> list[QueryResult]:
    """Run all benchmark queries through the KG-only pipeline."""
    kg_retriever = KnowledgeGraphRetriever()
    print(f"KG loaded: {kg_retriever.node_count} nodes")

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
            state = run_kg_pipeline(query, kg_retriever)
            duration = time.time() - start

            answer = state.get("answer", "")
            fact_details = check_facts_in_answer(answer, bench["key_facts"])
            facts_found = sum(1 for _, f in fact_details if f)

            result = QueryResult(
                query=query,
                category=bench["category"],
                expected_classification=bench["expected_classification"],
                actual_classification="kg-only",
                classification_correct=True,  # N/A for KG-only
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
                actual_classification="kg-only",
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
                  f"grounded={result.grounded} | sources={result.source_count} | "
                  f"{result.duration_secs:.1f}s")
            for desc, found in result.fact_details:
                print(f"    {'Y' if found else 'N'} {desc}")
            if result.error:
                print(f"  ERROR: {result.error}")

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="KG-only benchmark for Logicbroker RAG agent")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show per-query details")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--output", type=str, help="Write JSON results to file")
    args = parser.parse_args()

    categories = [args.category] if args.category else None

    print(f"Running {len(BENCHMARK)} queries through KG-ONLY retrieval pipeline...")
    print("(No vector search — knowledge graph edges only)\n")
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
    logging.basicConfig(level=logging.WARNING)
    main()
