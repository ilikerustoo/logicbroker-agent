"""Find the exact chunk containing POST /api/v3/Orders create endpoint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")
col = client.get_collection("logicbroker_docs")

# Search by document text
results = col.get(
    where_document={"$contains": "POST /api/v3/Orders"},
    include=["documents", "metadatas"],
)

for i, (doc_id, text, meta) in enumerate(zip(results["ids"], results["documents"], results["metadatas"])):
    if "Create an order" in text or "POST /api/v3/Orders`\n" in text:
        print(f"ID: {doc_id}")
        print(f"Title: {meta.get('title')}")
        print(f"Chunk: {meta.get('chunk_index')}/{meta.get('total_chunks')}")
        print(f"Doc type: {meta.get('doc_type')}")
        print(f"Text preview:\n{text[:300]}")
        print("---")
