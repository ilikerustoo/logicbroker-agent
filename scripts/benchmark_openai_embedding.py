"""Benchmark using ONLY OpenAI embeddings for retrieval (no KG).

Uses text-embedding-3-small for both indexing and query-time similarity search.
Creates a separate ChromaDB collection ('logicbroker_docs_openai') on first run.

Usage:
    python scripts/benchmark_openai_embedding.py              # summary only
    python scripts/benchmark_openai_embedding.py -v           # verbose per-query
    python scripts/benchmark_openai_embedding.py --json       # JSON output
    python scripts/benchmark_openai_embedding.py --reindex    # force re-index
    python scripts/benchmark_openai_embedding.py --output results_openai.json
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import chromadb
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from openai import OpenAI

from logicbroker_agent.graph import GeneratedAnswer, HallucinationVerdict
from logicbroker_agent.indexer import _chunk_documents, _load_documents, API_DIR, KB_DIR

# Reuse benchmark queries and scoring
sys.path.insert(0, str(Path(__file__).parent))
from benchmark_e2e import BENCHMARK, QueryResult, check_facts_in_answer, print_summary, results_to_json

logger = logging.getLogger(__name__)

CHROMA_DIR = Path("data/chroma_db")
COLLECTION_NAME = "logicbroker_docs_openai"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536
DEFAULT_TOP_K = 8


class OpenAIEmbedder:
    """Wrapper around OpenAI embeddings API."""

    def __init__(self, model: str = EMBEDDING_MODEL):
        self._client = OpenAI()
        self._model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts."""
        response = self._client.embeddings.create(input=texts, model=self._model)
        return [d.embedding for d in response.data]

    def embed_query(self, query: str) -> list[float]:
        """Embed a single query."""
        return self.embed([query])[0]


def ensure_index(embedder: OpenAIEmbedder, force: bool = False) -> chromadb.Collection:
    """Ensure the OpenAI-embedded collection exists, indexing if needed."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if force:
        try:
            client.delete_collection(COLLECTION_NAME)
            print("Deleted existing OpenAI collection for reindex.")
        except Exception:
            pass

    try:
        collection = client.get_collection(COLLECTION_NAME)
        if collection.count() > 0 and not force:
            print(f"OpenAI collection exists: {collection.count()} chunks. Use --reindex to rebuild.")
            return collection
    except Exception:
        pass

    # Need to index
    print("Indexing documents with OpenAI embeddings...")
    print(f"  Model: {EMBEDDING_MODEL}")

    kb_docs = _load_documents(KB_DIR, "kb_article")
    api_docs = _load_documents(API_DIR, "api_doc")
    all_docs = kb_docs + api_docs
    chunks = _chunk_documents(all_docs)

    print(f"  {len(all_docs)} documents → {len(chunks)} chunks")

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    batch_size = 100
    total_stored = 0

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c[0] for c in batch]
        metadatas = [c[1] for c in batch]
        ids = [f"oai_chunk_{i + j}" for j in range(len(batch))]

        embeddings = embedder.embed(texts)

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )
        total_stored += len(batch)

        if total_stored % 500 == 0 or total_stored == len(chunks):
            print(f"  Stored {total_stored}/{len(chunks)} chunks")

    print(f"  Indexing complete: {total_stored} chunks stored.")
    return collection


def retrieve_openai(
    query: str,
    collection: chromadb.Collection,
    embedder: OpenAIEmbedder,
    top_k: int = DEFAULT_TOP_K,
) -> list[dict]:
    """Retrieve relevant chunks using OpenAI embeddings."""
    embedding = embedder.embed_query(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    docs = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        similarity = 1 - distance

        docs.append({
            "text": results["documents"][0][i],
            "title": meta.get("title", ""),
            "source_url": meta.get("source_url", ""),
            "category": meta.get("category", ""),
            "doc_type": meta.get("doc_type", ""),
            "chunk_index": meta.get("chunk_index", 0),
            "total_chunks": meta.get("total_chunks", 1),
            "score": similarity,
        })

    return docs


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
            "the provided source documents. Follow these rules:\n\n"
            "1. Every factual claim must cite its source using [N] notation.\n"
            "2. If the sources don't contain enough information, say so explicitly.\n"
            "3. Be concise and direct.\n\n"
            f"Source documents:\n\n{context_block}"
        )),
        HumanMessage(content=query),
    ])

    sources = [{"title": c.source_title, "url": c.source_url} for c in result.citations]
    return {"answer": result.answer, "sources": sources}


def check_hallucination(answer: str, docs: list[dict]) -> bool:
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


def run_openai_pipeline(
    query: str,
    collection: chromadb.Collection,
    embedder: OpenAIEmbedder,
) -> dict:
    """Run the full pipeline with OpenAI embedding retrieval only."""
    docs = retrieve_openai(query, collection, embedder)
    gen = generate_answer(query, docs)
    grounded = check_hallucination(gen["answer"], docs) if gen["answer"] else False

    return {
        "answer": gen["answer"],
        "sources": gen["sources"],
        "grounded": grounded,
        "doc_count": len(docs),
    }


def run_benchmark(
    collection: chromadb.Collection,
    embedder: OpenAIEmbedder,
    categories: list[str] | None = None,
    verbose: bool = False,
) -> list[QueryResult]:
    """Run all benchmark queries through the OpenAI-embedding-only pipeline."""
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
            state = run_openai_pipeline(query, collection, embedder)
            duration = time.time() - start

            answer = state.get("answer", "")
            fact_details = check_facts_in_answer(answer, bench["key_facts"])
            facts_found = sum(1 for _, f in fact_details if f)

            result = QueryResult(
                query=query,
                category=bench["category"],
                expected_classification=bench["expected_classification"],
                actual_classification="openai-embedding",
                classification_correct=True,  # N/A for embedding-only
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
                actual_classification="openai-embedding",
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

    parser = argparse.ArgumentParser(
        description="OpenAI-embedding-only benchmark for Logicbroker RAG agent"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Show per-query details")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--reindex", action="store_true", help="Force re-index with OpenAI embeddings")
    parser.add_argument("--output", type=str, help="Write JSON results to file")
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set. Required for OpenAI embeddings.")
        sys.exit(1)

    categories = [args.category] if args.category else None
    embedder = OpenAIEmbedder()

    print(f"Running {len(BENCHMARK)} queries through OPENAI-EMBEDDING-ONLY retrieval pipeline...")
    print(f"(No KG — vector search with {EMBEDDING_MODEL} only)\n")

    collection = ensure_index(embedder, force=args.reindex)
    results = run_benchmark(collection, embedder, categories=categories, verbose=args.verbose)

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
