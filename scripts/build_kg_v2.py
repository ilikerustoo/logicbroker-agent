"""Build an expanded knowledge graph from Logicbroker docs.

v2 improvements over v1:
- Broader source selection: processes ALL chunks, not just workflow/API subsets
- Richer extraction prompt: captures configuration, troubleshooting, features, fields
- Deduplication: merges equivalent triples across batches
- Incremental: can extend an existing graph without reprocessing
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
KG_V2_PATH = Path("data/knowledge_graph_v2.json")


def get_all_chunks():
    """Get all chunks from ChromaDB, grouped by document."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    col = client.get_collection(COLLECTION)

    all_data = col.get(include=["documents", "metadatas"])

    # Group chunks by document title for better extraction context
    docs = {}
    for doc, meta in zip(all_data["documents"], all_data["metadatas"]):
        title = meta.get("title", "untitled")
        doc_type = meta.get("doc_type", "unknown")
        chunk_idx = meta.get("chunk_index", 0)

        key = (title, doc_type)
        if key not in docs:
            docs[key] = []
        docs[key].append({
            "text": doc[:2000],
            "chunk_index": chunk_idx,
        })

    # Sort chunks within each document
    for key in docs:
        docs[key].sort(key=lambda c: c["chunk_index"])

    return docs


def select_chunks_for_extraction(docs):
    """Select chunks that are likely to contain extractable relationships.

    v2 strategy: include everything, but prioritize information-dense chunks.
    Skip very short chunks and pure navigation/boilerplate.
    """
    selected = []

    for (title, doc_type), chunks in docs.items():
        for chunk in chunks:
            text = chunk["text"]

            # Skip very short chunks (likely headers/nav)
            if len(text) < 100:
                continue

            # Skip chunks that are mostly code/JSON without explanation
            code_ratio = text.count("```") + text.count("{") + text.count("}")
            if code_ratio > len(text) * 0.4:
                continue

            selected.append({
                "text": text,
                "title": title,
                "doc_type": doc_type,
                "chunk_index": chunk["chunk_index"],
            })

    return selected


def extract_triples_batch(chunks, client):
    """Extract entity-relationship triples from a batch of chunks.

    v2: expanded extraction prompt covering more relationship types.
    """
    chunk_texts = []
    for i, chunk in enumerate(chunks):
        chunk_texts.append(
            f"[Chunk {i+1} | {chunk['title']} | {chunk['doc_type']}]\n{chunk['text']}"
        )

    combined = "\n\n---\n\n".join(chunk_texts)

    prompt = f"""Extract entity-relationship triples from these Logicbroker documentation chunks.

Extract ALL meaningful relationships you find. Categories to look for:

1. **Document lifecycle**: Document types and their flow (Order → Acknowledgement → Shipment → Invoice → Return)
2. **API operations**: Endpoints and their effects (POST /api/v3/Orders creates an Order)
3. **Status transitions**: Status codes and what triggers transitions (status 150 → 500 via Acknowledgement)
4. **Field definitions**: Required/optional fields for documents (Order requires_field PartnerPO)
5. **Configuration steps**: How to set up features (Webhook requires configuration_step "Set callback URL")
6. **Troubleshooting**: Problems and their solutions (Missing LinkKey causes "order not routing", resolved_by "check partner settings")
7. **Platform features**: Capabilities and what enables them (Inventory Sync supports real-time_updates via webhooks)
8. **Business rules**: Constraints and validation (Order quantity must_match acknowledgement quantity)
9. **Integrations**: How systems connect (EDI 850 maps_to Order, SFTP connects_via scheduled_polling)
10. **Access control**: Permissions and roles (API Key requires permission "integrations/manage")

Output JSON array of triples:
[
  {{"subject": "Order", "predicate": "has_status", "object": "150 Ready to Acknowledge", "context": "initial status when supplier receives order"}},
  {{"subject": "POST /api/v3/Acknowledgements", "predicate": "creates", "object": "Acknowledgement", "context": "acknowledges order items, rate limit 10/sec"}},
  {{"subject": "Missing LinkKey", "predicate": "causes", "object": "Order not routing to supplier", "context": "common troubleshooting issue"}},
  {{"subject": "Webhook", "predicate": "requires_setup", "object": "Callback URL", "context": "configured in portal under Settings > Webhooks"}},
  {{"subject": "EDI 850", "predicate": "maps_to", "object": "Order", "context": "standard purchase order document"}}
]

Rules:
- Use consistent entity names (capitalize: "Order" not "order", "Webhook" not "webhook")
- Include the context field for additional detail that helps answer questions
- Extract 5-20 triples per chunk depending on information density
- Predicates: short verb phrases (creates, requires_field, has_status, advances_to, causes, resolved_by, configured_in, maps_to, requires_setup, enables, supports, connects_via, must_match, requires_permission, triggers, depends_on)
- For troubleshooting: use "causes" and "resolved_by" predicates
- For configuration: use "requires_setup", "configured_in", "enabled_by" predicates
- Prefer specific entities over vague ones ("LinkKey" over "a field")

Documentation chunks:
{combined}

Return ONLY the JSON array, no other text."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(text)


def deduplicate_triples(triples):
    """Remove duplicate triples, keeping the one with the richest context."""
    seen = {}
    for t in triples:
        key = (t["subject"].lower(), t["predicate"].lower(), t["object"].lower())
        if key not in seen or len(t.get("context", "")) > len(seen[key].get("context", "")):
            seen[key] = t
    return list(seen.values())


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


def save_graph(G, triples, path=KG_V2_PATH):
    """Save graph as JSON."""
    data = {
        "version": 2,
        "triples": triples,
        "nodes": list(G.nodes()),
        "edges": [
            {"source": u, "target": v, **d}
            for u, v, d in G.edges(data=True)
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
    print(f"Saved {len(G.nodes())} nodes, {len(G.edges())} edges to {path}")


def load_existing_triples(path=KG_V2_PATH):
    """Load existing triples if graph already exists (for incremental builds)."""
    if path.exists():
        data = json.loads(path.read_text())
        return data.get("triples", [])
    return []


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Build expanded knowledge graph")
    parser.add_argument("--incremental", action="store_true",
                        help="Add to existing graph instead of rebuilding")
    parser.add_argument("--max-batches", type=int, default=None,
                        help="Limit number of batches (for testing)")
    args = parser.parse_args()

    print("Step 1: Loading chunks from ChromaDB...")
    docs = get_all_chunks()
    print(f"  Found {len(docs)} documents")

    chunks = select_chunks_for_extraction(docs)
    print(f"  Selected {len(chunks)} chunks for extraction")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        return

    client = anthropic.Anthropic(api_key=api_key)

    # Load existing triples if incremental
    existing_triples = load_existing_triples() if args.incremental else []
    if existing_triples:
        print(f"  Loaded {len(existing_triples)} existing triples")

    all_triples = list(existing_triples)
    batch_size = 6  # Slightly smaller batches for richer extraction
    batches = [chunks[i:i+batch_size] for i in range(0, len(chunks), batch_size)]

    if args.max_batches:
        batches = batches[:args.max_batches]

    print(f"\nStep 2: Extracting triples from {len(batches)} batches...")
    for i, batch in enumerate(batches):
        print(f"  Batch {i+1}/{len(batches)} ({len(batch)} chunks)...", end=" ", flush=True)
        try:
            triples = extract_triples_batch(batch, client)
            all_triples.extend(triples)
            print(f"→ {len(triples)} triples")
        except json.JSONDecodeError as e:
            print(f"PARSE ERROR: {e}")
        except Exception as e:
            print(f"ERROR: {e}")

    print(f"\nStep 3: Deduplicating {len(all_triples)} raw triples...")
    deduped = deduplicate_triples(all_triples)
    print(f"  → {len(deduped)} unique triples")

    print(f"\nStep 4: Building graph...")
    G = build_graph(deduped)
    save_graph(G, deduped)

    # Stats
    print(f"\nGraph stats:")
    print(f"  Nodes: {len(G.nodes())}")
    print(f"  Edges: {len(G.edges())}")
    print(f"  Weakly connected components: {nx.number_weakly_connected_components(G)}")

    # Predicate distribution
    predicates = {}
    for _, _, d in G.edges(data=True):
        p = d["predicate"]
        predicates[p] = predicates.get(p, 0) + 1

    print(f"\n  Top predicates:")
    for pred, count in sorted(predicates.items(), key=lambda x: -x[1])[:15]:
        print(f"    {pred}: {count}")


if __name__ == "__main__":
    main()
