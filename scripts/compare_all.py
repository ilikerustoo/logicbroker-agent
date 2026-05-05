"""Side-by-side comparison: MiniLM vs OpenAI embeddings vs Knowledge Graph.

Same query, same format — measures which approach surfaces the 4 key facts.

OpenAI embeddings are indexed into a separate ChromaDB collection on first run
(~1,600 chunks, costs ~$0.003). Subsequent runs reuse the cached collection.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import chromadb
import networkx as nx
from sentence_transformers import SentenceTransformer

QUERY = (
    "What status does an order have after a supplier receives it, "
    "and what API call does the supplier make to advance it to Ready to Ship?"
)

CHROMA_DIR = Path("data/chroma_db")
COLLECTION = "logicbroker_docs"
OPENAI_COLLECTION = "logicbroker_docs_openai"
KG_PATH = Path("data/knowledge_graph.json")

KEY_FACTS = [
    (["150 ready to acknowledge", "150: ready to acknowledge", "status 150"],
     "Order starts at status 150 (Ready to Acknowledge)"),
    (["500 ready to ship", "500: ready to ship", "advances order to 500",
      "advances_order_to.*500", "moves to ready to ship"],
     "Acknowledgement advances order to 500 (Ready to Ship)"),
    (["post /api/v3/acknowledgement", "post acknowledgement", "post.*acknowledgement"],
     "POST endpoint/action to create acknowledgement"),
    (["acknowledgement.*order", "order.*acknowledgement", "acknowledge.*order"],
     "Acknowledgement advances the order lifecycle"),
]


def check_facts(texts: list[str]) -> list[tuple[str, bool]]:
    """Check which key facts appear — any needle in the group is sufficient.

    Needles use simple substring matching (case-insensitive). Wildcards (.*) in
    needles are matched literally as substrings (not regex) unless the needle
    contains no wildcard.
    """
    import re
    combined = " ".join(texts).lower()
    results = []
    for needles, desc in KEY_FACTS:
        found = False
        for needle in needles:
            if ".*" in needle:
                if re.search(needle, combined):
                    found = True
                    break
            elif needle in combined:
                found = True
                break
        results.append((desc, found))
    return results


# ---------- MiniLM ----------

def test_minilm():
    print("=" * 70)
    print("1. MiniLM (all-MiniLM-L6-v2) — current system")
    print("=" * 70)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION)
    embedding = model.encode([QUERY]).tolist()

    results = collection.query(
        query_embeddings=embedding,
        n_results=10,
        include=["documents", "metadatas", "distances"],
    )

    print(f"\nQuery: {QUERY}\n")
    texts = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        score = 1 - results["distances"][0][i]
        doc_type = meta.get("doc_type", "?")
        title = meta.get("title", "?")
        text = results["documents"][0][i]
        preview = text[:120].replace("\n", " ")
        print(f"  [{score:.3f}] ({doc_type:10}) {title} (chunk {meta.get('chunk_index', 0)})")
        print(f"            {preview}...")
        texts.append(text)

    print("\n  Key facts found:")
    facts = check_facts(texts)
    for desc, found in facts:
        print(f"    {'Y' if found else 'N'} {desc}")
    return sum(1 for _, f in facts if f)


# ---------- OpenAI ----------

def _ensure_openai_collection(oai, client):
    """Create an OpenAI-indexed collection if it doesn't exist yet."""
    existing = [c.name for c in client.list_collections()]
    if OPENAI_COLLECTION in existing:
        col = client.get_collection(OPENAI_COLLECTION)
        if col.count() > 0:
            print(f"  Using cached OpenAI collection ({col.count()} chunks)")
            return col

    # Pull all docs from the MiniLM collection
    src = client.get_collection(COLLECTION)
    total = src.count()
    print(f"  Indexing {total} chunks with OpenAI embeddings (one-time)...")

    all_data = src.get(include=["documents", "metadatas"])

    # Batch embed with OpenAI (max 2048 per request)
    batch_size = 512
    all_embeddings = []
    for start in range(0, total, batch_size):
        batch_texts = all_data["documents"][start:start + batch_size]
        resp = oai.embeddings.create(model="text-embedding-3-small", input=batch_texts)
        all_embeddings.extend([d.embedding for d in resp.data])
        done = min(start + batch_size, total)
        print(f"    Embedded {done}/{total}")

    # Create collection and insert
    try:
        client.delete_collection(OPENAI_COLLECTION)
    except Exception:
        pass

    col = client.create_collection(
        name=OPENAI_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )
    col.add(
        ids=all_data["ids"],
        documents=all_data["documents"],
        metadatas=all_data["metadatas"],
        embeddings=all_embeddings,
    )
    print(f"  OpenAI collection ready: {col.count()} chunks")
    return col


def test_openai():
    import os
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n" + "=" * 70)
        print("2. OpenAI (text-embedding-3-small) — SKIPPED (no OPENAI_API_KEY)")
        print("=" * 70)
        return -1

    print("\n" + "=" * 70)
    print("2. OpenAI (text-embedding-3-small)")
    print("=" * 70)

    oai = OpenAI(api_key=api_key)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = _ensure_openai_collection(oai, client)

    # Embed query with OpenAI
    resp = oai.embeddings.create(model="text-embedding-3-small", input=[QUERY])
    embedding = [resp.data[0].embedding]

    results = collection.query(
        query_embeddings=embedding,
        n_results=10,
        include=["documents", "metadatas", "distances"],
    )

    print(f"\nQuery: {QUERY}\n")
    texts = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        score = 1 - results["distances"][0][i]
        doc_type = meta.get("doc_type", "?")
        title = meta.get("title", "?")
        text = results["documents"][0][i]
        preview = text[:120].replace("\n", " ")
        print(f"  [{score:.3f}] ({doc_type:10}) {title} (chunk {meta.get('chunk_index', 0)})")
        print(f"            {preview}...")
        texts.append(text)

    print("\n  Key facts found:")
    facts = check_facts(texts)
    for desc, found in facts:
        print(f"    {'Y' if found else 'N'} {desc}")
    return sum(1 for _, f in facts if f)


# ---------- Knowledge Graph ----------

def test_kg():
    print("\n" + "=" * 70)
    print("3. Knowledge Graph (entity traversal)")
    print("=" * 70)

    if not KG_PATH.exists():
        print("  SKIPPED — no knowledge_graph.json")
        return -1

    data = json.loads(KG_PATH.read_text())
    G = nx.DiGraph()
    for node in data["nodes"]:
        G.add_node(node)
    for edge in data["edges"]:
        G.add_edge(edge["source"], edge["target"],
                   predicate=edge.get("predicate", ""),
                   context=edge.get("context", ""))

    print(f"\nGraph: {len(G.nodes())} nodes, {len(G.edges())} edges")
    print(f"Query: {QUERY}\n")

    # Find seed nodes matching query terms
    keywords = ["order", "supplier", "status", "ready to ship", "acknowledge",
                "acknowledgement", "api", "post", "150", "500"]
    seed_nodes = set()
    for node in G.nodes():
        node_lower = node.lower()
        for kw in keywords:
            if kw in node_lower:
                seed_nodes.add(node)
                break

    # Expand 1 hop
    edges = []
    visited = set(seed_nodes)
    for node in seed_nodes:
        for _, target, d in G.out_edges(node, data=True):
            edges.append((node, d["predicate"], target, d.get("context", "")))
            visited.add(target)
        for source, _, d in G.in_edges(node, data=True):
            edges.append((source, d["predicate"], node, d.get("context", "")))
            visited.add(source)

    # Score by keyword overlap
    high_value = ["order", "acknowledge", "status", "ready to ship",
                  "supplier", "post", "api", "150", "500", "advance"]
    scored = []
    for subj, pred, obj, ctx in edges:
        text = f"{subj} {pred} {obj} {ctx}".lower()
        score = sum(1 for t in high_value if t in text)
        scored.append((score, subj, pred, obj, ctx))
    scored.sort(reverse=True)

    # Deduplicate and show top 15
    seen = set()
    count = 0
    texts = []
    for score, subj, pred, obj, ctx in scored:
        key = (subj, pred, obj)
        if key in seen:
            continue
        seen.add(key)
        ctx_str = f" ({ctx})" if ctx else ""
        line = f"{subj} --[{pred}]--> {obj}{ctx_str}"
        print(f"  [{score}] {line}")
        texts.append(line)
        count += 1
        if count >= 15:
            break

    print("\n  Key facts found:")
    facts = check_facts(texts)
    for desc, found in facts:
        print(f"    {'Y' if found else 'N'} {desc}")
    return sum(1 for _, f in facts if f)


# ---------- Summary ----------

if __name__ == "__main__":
    scores = {}
    scores["MiniLM"] = test_minilm()
    scores["OpenAI"] = test_openai()
    scores["KG"] = test_kg()

    print("\n" + "=" * 70)
    print("SCORECARD (key facts found out of 4)")
    print("=" * 70)
    for name, s in scores.items():
        if s == -1:
            print(f"  {name:12} — SKIPPED")
        else:
            bar = "#" * s + "." * (4 - s)
            print(f"  {name:12} {s}/4  [{bar}]")
