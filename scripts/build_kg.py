"""Build a lightweight knowledge graph from Logicbroker docs.

Extracts entities and relationships from the indexed chunks using an LLM,
stores them in a NetworkX graph, then answers queries by traversing
relevant subgraphs + pulling associated chunks.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import networkx as nx
from dotenv import load_dotenv

load_dotenv()

import chromadb
import anthropic

CHROMA_DIR = Path("data/chroma_db")
COLLECTION = "logicbroker_docs"
KG_PATH = Path("data/knowledge_graph.json")


def get_chunks_for_extraction():
    """Get a representative set of chunks for KG extraction.

    Focus on chunks that describe relationships, workflows, and endpoints.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    col = client.get_collection(COLLECTION)

    # Get all chunks with their metadata
    all_data = col.get(include=["documents", "metadatas"])

    # Filter to high-value chunks for KG extraction
    selected = []
    for doc, meta in zip(all_data["documents"], all_data["metadatas"]):
        title = meta.get("title", "")
        doc_type = meta.get("doc_type", "")
        chunk_idx = meta.get("chunk_index", 0)

        # Include: API endpoint chunks (contain POST/GET/PUT/DELETE)
        if doc_type == "api_doc" and any(verb in doc for verb in ["POST ", "GET ", "PUT ", "DELETE "]):
            selected.append({"text": doc[:1500], "title": title, "doc_type": doc_type, "chunk_index": chunk_idx})

        # Include: KB articles about workflows, statuses, specifications
        elif doc_type == "kb_article" and any(kw in title.lower() for kw in [
            "status", "workflow", "specification", "lifecycle", "onboarding",
            "introduction", "order", "shipment", "acknowledgement", "invoice", "return"
        ]):
            if chunk_idx < 5:  # First few chunks of relevant articles
                selected.append({"text": doc[:1500], "title": title, "doc_type": doc_type, "chunk_index": chunk_idx})

    return selected


def extract_triples_batch(chunks, client):
    """Use Claude to extract entity-relationship triples from a batch of chunks."""

    # Build the input text
    chunk_texts = []
    for i, chunk in enumerate(chunks):
        chunk_texts.append(f"[Chunk {i+1} | {chunk['title']} | {chunk['doc_type']}]\n{chunk['text']}")

    combined = "\n\n---\n\n".join(chunk_texts)

    prompt = f"""Extract entity-relationship triples from these Logicbroker documentation chunks.

Focus on:
1. Document types and their relationships (Order → Acknowledgement → Shipment → Invoice)
2. API endpoints and what they do (POST /api/v3/Orders creates an Order)
3. Status codes and transitions (status 150 "Ready to Acknowledge" → status 500 "Ready to Ship")
4. Required fields for operations
5. Business rules and constraints

Output JSON array of triples:
[
  {{"subject": "Order", "predicate": "has_status", "object": "150 Ready to Acknowledge", "context": "initial status when supplier receives order"}},
  {{"subject": "POST /api/v3/Acknowledgements", "predicate": "creates", "object": "Acknowledgement", "context": "rate limit 10/sec"}},
  {{"subject": "Acknowledgement", "predicate": "advances_order_to", "object": "500 Ready to Ship", "context": "when supplier accepts order items"}}
]

Rules:
- Use consistent entity names (e.g., always "Order" not "order" or "Orders")
- Include the context field for additional detail
- Extract 5-15 triples per chunk (more for information-dense chunks)
- Predicates should be short verb phrases: creates, requires_field, has_status, advances_to, links_via, etc.

Documentation chunks:
{combined}

Return ONLY the JSON array, no other text."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    # Handle markdown code blocks
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(text)


def build_graph(triples):
    """Build a NetworkX graph from extracted triples."""
    G = nx.DiGraph()

    for t in triples:
        subj = t["subject"]
        obj = t["object"]
        pred = t["predicate"]
        ctx = t.get("context", "")

        G.add_node(subj)
        G.add_node(obj)
        G.add_edge(subj, obj, predicate=pred, context=ctx)

    return G


def save_graph(G, triples):
    """Save graph as JSON for later loading."""
    data = {
        "triples": triples,
        "nodes": list(G.nodes()),
        "edges": [
            {"source": u, "target": v, **d}
            for u, v, d in G.edges(data=True)
        ],
    }
    KG_PATH.parent.mkdir(parents=True, exist_ok=True)
    KG_PATH.write_text(json.dumps(data, indent=2))
    print(f"Saved {len(G.nodes())} nodes, {len(G.edges())} edges to {KG_PATH}")


def main():
    print("Step 1: Selecting chunks for extraction...")
    chunks = get_chunks_for_extraction()
    print(f"  Selected {len(chunks)} high-value chunks")

    # Process in batches of 10
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        return

    client = anthropic.Anthropic(api_key=api_key)

    all_triples = []
    batch_size = 8
    batches = [chunks[i:i+batch_size] for i in range(0, len(chunks), batch_size)]

    print(f"Step 2: Extracting triples from {len(batches)} batches...")
    for i, batch in enumerate(batches):
        print(f"  Batch {i+1}/{len(batches)} ({len(batch)} chunks)...", end=" ", flush=True)
        try:
            triples = extract_triples_batch(batch, client)
            all_triples.extend(triples)
            print(f"→ {len(triples)} triples")
        except Exception as e:
            print(f"ERROR: {e}")

    print(f"\nStep 3: Building graph from {len(all_triples)} triples...")
    G = build_graph(all_triples)
    save_graph(G, all_triples)

    # Print some stats
    print(f"\nGraph stats:")
    print(f"  Nodes: {len(G.nodes())}")
    print(f"  Edges: {len(G.edges())}")
    print(f"  Connected components: {nx.number_weakly_connected_components(G)}")

    # Show some key relationships
    print(f"\nSample relationships:")
    for u, v, d in list(G.edges(data=True))[:20]:
        print(f"  {u} --[{d['predicate']}]--> {v}")


if __name__ == "__main__":
    main()
