"""Compare retrieval quality: MiniLM vs OpenAI embeddings vs Knowledge Graph.

Test query requires multi-doc synthesis:
- KB: order status 150 → 500 after acknowledgement
- API: POST /api/v3/Acknowledgements with PartnerPO + AckLines
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import chromadb
from sentence_transformers import SentenceTransformer

QUERY = (
    "What status does an order have after a supplier receives it, "
    "and what API call does the supplier make to advance it to Ready to Ship?"
)

CHROMA_DIR = Path("data/chroma_db")
COLLECTION = "logicbroker_docs"


def test_minilm():
    """Test with local MiniLM embeddings."""
    print("=" * 70)
    print("MODEL: all-MiniLM-L6-v2 (local)")
    print("=" * 70)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION)

    embedding = model.encode([QUERY]).tolist()

    # Unfiltered top 10
    results = collection.query(
        query_embeddings=embedding,
        n_results=10,
        include=["documents", "metadatas", "distances"],
    )

    print(f"\nQuery: {QUERY}\n")
    print("Top 10 (unfiltered):")
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        score = 1 - results["distances"][0][i]
        doc_type = meta.get("doc_type", "?")
        title = meta.get("title", "?")
        print(f"  [{score:.3f}] ({doc_type:10}) {title} (chunk {meta.get('chunk_index', 0)})")

    # API-only top 5
    results_api = collection.query(
        query_embeddings=embedding,
        n_results=5,
        include=["documents", "metadatas", "distances"],
        where={"doc_type": "api_doc"},
    )
    print("\nTop 5 (API docs only):")
    for i in range(len(results_api["ids"][0])):
        meta = results_api["metadatas"][0][i]
        score = 1 - results_api["distances"][0][i]
        title = meta.get("title", "?")
        text_preview = results_api["documents"][0][i][:100]
        print(f"  [{score:.3f}] {title} (chunk {meta.get('chunk_index', 0)})")
        print(f"          {text_preview}...")

    return results, results_api


def test_openai():
    """Test with OpenAI text-embedding-3-small."""
    import os
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\nSkipping OpenAI test — no OPENAI_API_KEY in .env")
        return None, None

    print("\n" + "=" * 70)
    print("MODEL: text-embedding-3-small (OpenAI)")
    print("=" * 70)

    oai = OpenAI(api_key=api_key)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION)

    resp = oai.embeddings.create(model="text-embedding-3-small", input=[QUERY])
    embedding = [resp.data[0].embedding]

    # Unfiltered top 10
    results = collection.query(
        query_embeddings=embedding,
        n_results=10,
        include=["documents", "metadatas", "distances"],
    )

    print(f"\nQuery: {QUERY}\n")
    print("Top 10 (unfiltered):")
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        score = 1 - results["distances"][0][i]
        doc_type = meta.get("doc_type", "?")
        title = meta.get("title", "?")
        print(f"  [{score:.3f}] ({doc_type:10}) {title} (chunk {meta.get('chunk_index', 0)})")

    # API-only top 5
    results_api = collection.query(
        query_embeddings=embedding,
        n_results=5,
        include=["documents", "metadatas", "distances"],
        where={"doc_type": "api_doc"},
    )
    print("\nTop 5 (API docs only):")
    for i in range(len(results_api["ids"][0])):
        meta = results_api["metadatas"][0][i]
        score = 1 - results_api["distances"][0][i]
        title = meta.get("title", "?")
        text_preview = results_api["documents"][0][i][:100]
        print(f"  [{score:.3f}] {title} (chunk {meta.get('chunk_index', 0)})")
        print(f"          {text_preview}...")

    return results, results_api


if __name__ == "__main__":
    test_minilm()
    test_openai()

    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print("""
The ideal answer requires information from:
  1. KB: Order arrives at status 150 "Ready to Acknowledge"
  2. KB: Acknowledgement advances order to status 500 "Ready to Ship"
  3. API: POST /api/v3/Acknowledgements
  4. API: Required fields: PartnerPO, AckLines[].Quantity

Look at the results above — did BOTH types of chunks appear in the top 10?
If not, no embedding model alone can produce the full answer without routing.
""")
