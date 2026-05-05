"""Check the similarity score for the POST /api/v3/Orders chunk."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sentence_transformers import SentenceTransformer
import chromadb

query = "How do I create an order in Logicbroker?"

client = chromadb.PersistentClient(path="data/chroma_db")
col = client.get_collection("logicbroker_docs")
model = SentenceTransformer("all-MiniLM-L6-v2")

embedding = model.encode([query]).tolist()

# Query with API doc filter, top 20 to see where chunk_1448 lands
results = col.query(
    query_embeddings=embedding,
    n_results=20,
    where={"doc_type": "api_doc"},
    include=["documents", "metadatas", "distances"],
)

for i in range(len(results["ids"][0])):
    doc_id = results["ids"][0][i]
    meta = results["metadatas"][0][i]
    sim = 1 - results["distances"][0][i]
    marker = " <<<" if doc_id == "chunk_1448" else ""
    preview = results["documents"][0][i][:80].replace("\n", " ")
    print(f"{i+1:2}. [{sim:.3f}] {doc_id} — {meta['title']} (chunk {meta['chunk_index']}) {preview}{marker}")
