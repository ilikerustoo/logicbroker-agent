"""Direct comparison: MiniLM vs OpenAI embedding scores for key chunks.

Computes cosine similarity between the query and specific chunks using
both embedding models, without needing to re-index ChromaDB.
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

import chromadb

load_dotenv()

QUERY = "How do I create an order in Logicbroker?"

# Load the actual chunk texts from ChromaDB
client = chromadb.PersistentClient(path="data/chroma_db")
col = client.get_collection("logicbroker_docs")

# Get the top 10 API chunks + top 5 KB chunks + the target chunk
target_ids = ["chunk_1448"]  # POST /api/v3/Orders - Create an order

# Also get the chunks that actually ranked high
miniml = SentenceTransformer("all-MiniLM-L6-v2")
query_emb_mini = miniml.encode([QUERY]).tolist()

api_results = col.query(
    query_embeddings=query_emb_mini, n_results=10,
    where={"doc_type": "api_doc"},
    include=["documents", "metadatas", "distances"],
)
kb_results = col.query(
    query_embeddings=query_emb_mini, n_results=5,
    include=["documents", "metadatas", "distances"],
)

# Collect unique chunk IDs and their texts
chunks = {}
for ids, docs, metas in [
    (api_results["ids"][0], api_results["documents"][0], api_results["metadatas"][0]),
    (kb_results["ids"][0], kb_results["documents"][0], kb_results["metadatas"][0]),
]:
    for cid, text, meta in zip(ids, docs, metas):
        chunks[cid] = {"text": text, "meta": meta}

# Add the target chunk
target_data = col.get(ids=target_ids, include=["documents", "metadatas"])
for cid, text, meta in zip(target_data["ids"], target_data["documents"], target_data["metadatas"]):
    chunks[cid] = {"text": text, "meta": meta}

# Compute MiniLM similarities
all_texts = [chunks[cid]["text"] for cid in chunks]
all_ids = list(chunks.keys())

mini_embs = miniml.encode([QUERY] + all_texts)
query_mini = mini_embs[0]
chunk_mini = mini_embs[1:]

def cosine_sim(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

mini_scores = {cid: cosine_sim(query_mini, chunk_mini[i]) for i, cid in enumerate(all_ids)}

# Compute OpenAI similarities
oai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
oai_resp = oai.embeddings.create(model="text-embedding-3-small", input=[QUERY] + all_texts)
oai_embs = [np.array(d.embedding) for d in oai_resp.data]
query_oai = oai_embs[0]
chunk_oai = oai_embs[1:]

oai_scores = {cid: cosine_sim(query_oai, chunk_oai[i]) for i, cid in enumerate(all_ids)}

# Print comparison table
print(f"Query: {QUERY}\n")
print(f"{'Chunk':<45} {'Type':<8} {'MiniLM':>8} {'OpenAI':>8} {'Delta':>8}")
print("-" * 85)

# Sort by OpenAI score descending
sorted_ids = sorted(all_ids, key=lambda cid: oai_scores[cid], reverse=True)
for cid in sorted_ids:
    meta = chunks[cid]["meta"]
    title = meta.get("title", "?")[:30]
    chunk_idx = meta.get("chunk_index", "?")
    doc_type = "API" if meta.get("doc_type") == "api_doc" else "KB"
    label = f"{title} (chunk {chunk_idx})"
    ms = mini_scores[cid]
    os_ = oai_scores[cid]
    delta = os_ - ms
    marker = " <<<" if cid == "chunk_1448" else ""
    print(f"{label:<45} {doc_type:<8} {ms:>8.3f} {os_:>8.3f} {delta:>+8.3f}{marker}")
