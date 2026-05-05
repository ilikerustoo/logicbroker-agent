"""Compare retrieval quality with classification-first routing.

Tests both MiniLM (local) and OpenAI embeddings against the same queries
to see how routing affects which chunks surface.
"""

import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from logicbroker_agent.retriever import LogicbrokerRetriever

CHROMA_DIR = Path("data/chroma_db")

TEST_QUERIES = [
    ("How do I create an order in Logicbroker?", "order-lifecycle"),
    ("What API endpoint do I use to submit a shipment?", "api-integration"),
    ("How do I set up EDI with a new trading partner?", "edi-technical"),
    ("What is Logicbroker?", "general"),
]


def run_comparison(retriever: LogicbrokerRetriever, label: str):
    print(f"\n{'='*80}")
    print(f"  {label}")
    print(f"{'='*80}")

    api_categories = {"api-integration", "order-lifecycle", "edi-technical"}

    for query, category in TEST_QUERIES:
        print(f"\n  Query: {query}")
        print(f"  Category: {category}")

        if category in api_categories:
            api_chunks = retriever.query(query, top_k=5, doc_type_filter="api_doc")
            kb_chunks = retriever.query(query, top_k=5, doc_type_filter="kb_article")
            all_chunks = api_chunks + kb_chunks
            all_chunks.sort(key=lambda c: c.score, reverse=True)
            chunks = all_chunks[:8]

            print(f"  Routed: {len(api_chunks)} API + {len(kb_chunks)} KB → {len(chunks)} merged")
        else:
            chunks = retriever.query(query, top_k=5)
            print(f"  Unfiltered: {len(chunks)} chunks")

        for i, c in enumerate(chunks, 1):
            tag = "API" if c.doc_type == "api_doc" else "KB "
            print(f"    {i}. [{c.score:.3f}] [{tag}] {c.title} (chunk {c.chunk_index + 1})")
            # Show first 120 chars of text for context
            preview = c.text[:120].replace("\n", " ")
            print(f"       {preview}...")

        # Count API docs that made it
        api_count = sum(1 for c in chunks if c.doc_type == "api_doc")
        print(f"  → API docs in results: {api_count}/{len(chunks)}")


def main():
    print("Loading MiniLM retriever...")
    retriever = LogicbrokerRetriever()
    run_comparison(retriever, "MiniLM (all-MiniLM-L6-v2) + Classification Routing")

    # Compare with unrouted for the same queries
    print(f"\n{'='*80}")
    print(f"  MiniLM WITHOUT routing (baseline)")
    print(f"{'='*80}")
    for query, category in TEST_QUERIES:
        print(f"\n  Query: {query}")
        chunks = retriever.query(query, top_k=8)
        for i, c in enumerate(chunks, 1):
            tag = "API" if c.doc_type == "api_doc" else "KB "
            print(f"    {i}. [{c.score:.3f}] [{tag}] {c.title} (chunk {c.chunk_index + 1})")
        api_count = sum(1 for c in chunks if c.doc_type == "api_doc")
        print(f"  → API docs in results: {api_count}/{len(chunks)}")


if __name__ == "__main__":
    main()
