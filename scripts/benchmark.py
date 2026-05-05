"""Broad retrieval benchmark: MiniLM vs OpenAI embeddings vs Knowledge Graph.

Tests 15 diverse queries across 5 categories:
- Relational/Workflow (multi-hop, status transitions)
- Factual/Detail (single-chunk, field-level)
- API-specific (endpoint discovery)
- Troubleshooting (error/failure scenarios)
- Conceptual (what-is, how-does-it-work)

Each query has its own key facts. Final output is a summary matrix.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import chromadb
import networkx as nx
from sentence_transformers import SentenceTransformer

CHROMA_DIR = Path("data/chroma_db")
COLLECTION = "logicbroker_docs"
OPENAI_COLLECTION = "logicbroker_docs_openai"
KG_PATH = Path("data/knowledge_graph.json")

# ---------------------------------------------------------------------------
# Benchmark queries — each has: category, query, key_facts
# key_facts: list of (needles[], description)
# ---------------------------------------------------------------------------

BENCHMARK = [
    # === Category 1: Relational/Workflow (multi-hop) ===
    {
        "category": "Relational",
        "query": "What status does an order move to after acknowledgement, and how does a supplier send one?",
        "key_facts": [
            (["150 ready to acknowledge", "150: ready to acknowledge", "status 150"],
             "Order starts at status 150 (Ready to Acknowledge)"),
            (["500 ready to ship", "500: ready to ship", "advances.*500", "moves.*ready to ship"],
             "Acknowledgement advances order to 500 (Ready to Ship)"),
            (["post /api/v3/acknowledgement", "post acknowledgement", "post.*acknowledgement"],
             "POST endpoint to create acknowledgement"),
            (["supplier.*acknowledgement", "supplier.*acknowledge", "acknowledgement.*order", "acknowledge.*order"],
             "Supplier sends acknowledgement to advance order"),
        ],
    },
    {
        "category": "Relational",
        "query": "What is the full document lifecycle for a typical order from creation to invoice?",
        "key_facts": [
            (["order"], "Order is the starting document"),
            (["acknowledgement", "acknowledgment"], "Acknowledgement follows order"),
            (["shipment"], "Shipment follows acknowledgement"),
            (["invoice"], "Invoice follows shipment"),
        ],
    },
    {
        "category": "Relational",
        "query": "What documents does a supplier need to send after receiving an order to complete fulfillment?",
        "key_facts": [
            (["acknowledgement", "acknowledgment"], "Supplier sends acknowledgement"),
            (["shipment"], "Supplier sends shipment"),
            (["invoice"], "Supplier sends invoice"),
        ],
    },

    # === Category 2: Factual/Detail (single-chunk) ===
    {
        "category": "Factual",
        "query": "What connection options are available for suppliers in Logicbroker?",
        "key_facts": [
            (["web portal"], "Web Portal connection"),
            (["api"], "API connection"),
            (["edi"], "EDI connection"),
            (["shopify", "shipstation"], "Advanced integrations (Shopify/ShipStation)"),
        ],
    },
    {
        "category": "Factual",
        "query": "What is a linkkey in Logicbroker and what does it do?",
        "key_facts": [
            (["linkkey", "link key"], "Mentions linkkey"),
            (["related documents", "group.*document", "ties.*order", "links.*documents"],
             "Links/groups related documents together"),
        ],
    },
    {
        "category": "Factual",
        "query": "What EDI formats does Logicbroker support for connections?",
        "key_facts": [
            (["as2"], "AS2 format"),
            (["ftp", "sftp"], "FTP/SFTP format"),
            (["edi"], "EDI mentioned"),
        ],
    },

    # === Category 3: API-specific ===
    {
        "category": "API",
        "query": "How do I search for shipments by status using the API?",
        "key_facts": [
            (["get /api/v3/shipments", "get.*shipments"], "GET shipments endpoint"),
            (["filters.status", "status.*filter"], "Status filter parameter"),
        ],
    },
    {
        "category": "API",
        "query": "How do I create a webhook in Logicbroker's API?",
        "key_facts": [
            (["post /api/v3/webhooks", "post.*webhook"], "POST webhooks endpoint"),
            (["webhook"], "Webhook concept mentioned"),
        ],
    },
    {
        "category": "API",
        "query": "What are the rate limits for the Logicbroker API?",
        "key_facts": [
            (["rate limit"], "Rate limit mentioned"),
            (["1 request every 2 seconds", "2 second", "1.*2 second"],
             "Search endpoints: 1 req/2s"),
            (["10 requests per second", "10.*per second"],
             "Other endpoints: 10 req/s"),
        ],
    },

    # === Category 4: Troubleshooting ===
    {
        "category": "Troubleshooting",
        "query": "What does the Events page show and how do I use it to diagnose document failures?",
        "key_facts": [
            (["events"], "Events page mentioned"),
            (["alert", "severity"], "Alert/severity levels"),
            (["document failure", "failed document", "error", "noncompliant"],
             "Document failure/error visibility"),
        ],
    },
    {
        "category": "Troubleshooting",
        "query": "What test cases does Logicbroker support for supplier onboarding?",
        "key_facts": [
            (["fulfillment", "order fulfillment"], "Fulfillment test case"),
            (["cancellation", "cancallation"], "Cancellation test case"),
            (["partial fulfillment", "partial.*cancel"], "Partial fulfillment test"),
            (["return"], "Return test case"),
        ],
    },
    {
        "category": "Troubleshooting",
        "query": "How does a supplier set up an EDI connection with Logicbroker?",
        "key_facts": [
            (["edi"], "EDI mentioned"),
            (["as2", "ftp", "sftp"], "Transport protocol mentioned"),
            (["connection", "set up", "onboard"], "Setup/connection process"),
        ],
    },

    # === Category 5: Conceptual ===
    {
        "category": "Conceptual",
        "query": "What is Logicbroker and what problem does it solve?",
        "key_facts": [
            (["integration platform", "supply chain", "simplif"],
             "Integration platform for supply chain"),
            (["retailer"], "Retailers use it"),
            (["supplier"], "Suppliers use it"),
        ],
    },
    {
        "category": "Conceptual",
        "query": "What document types exist in Logicbroker?",
        "key_facts": [
            (["order"], "Order document"),
            (["acknowledgement", "acknowledgment"], "Acknowledgement"),
            (["shipment"], "Shipment"),
            (["invoice"], "Invoice"),
            (["return"], "Return"),
            (["inventory"], "Inventory"),
        ],
    },
    {
        "category": "Conceptual",
        "query": "What is the difference between a retailer and a supplier in Logicbroker?",
        "key_facts": [
            (["retailer.*send.*order", "retailer.*order", "send orders to.*supplier"],
             "Retailers send orders"),
            (["supplier.*fulfill", "supplier.*ship", "supplier.*process"],
             "Suppliers fulfill/ship orders"),
        ],
    },
]


def check_facts(texts: list[str], key_facts: list) -> list[tuple[str, bool]]:
    """Check which key facts appear in the combined text."""
    combined = " ".join(texts).lower()
    results = []
    for needles, desc in key_facts:
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

def query_minilm(model, collection, query: str, n_results: int = 10) -> list[str]:
    embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=embedding,
        n_results=n_results,
        include=["documents"],
    )
    return results["documents"][0]


# ---------- OpenAI ----------

def query_openai(oai, collection, query: str, n_results: int = 10) -> list[str]:
    resp = oai.embeddings.create(model="text-embedding-3-small", input=[query])
    embedding = [resp.data[0].embedding]
    results = collection.query(
        query_embeddings=embedding,
        n_results=n_results,
        include=["documents"],
    )
    return results["documents"][0]


# ---------- Knowledge Graph ----------

def query_kg(G, query: str) -> list[str]:
    """Query KG with keyword-seeded traversal, return edge descriptions."""
    # Extract keywords from query
    query_lower = query.lower()
    # General keywords relevant to Logicbroker domain
    all_keywords = [
        "order", "supplier", "retailer", "status", "ready to ship",
        "acknowledge", "acknowledgement", "acknowledgment", "api", "post", "get",
        "shipment", "invoice", "return", "inventory", "webhook",
        "edi", "connection", "ftp", "sftp", "as2", "document",
        "event", "alert", "error", "failure", "test", "onboard",
        "150", "500", "rate limit", "linkkey", "link key",
        "fulfillment", "cancellation", "integration", "platform",
        "shopify", "shipstation",
    ]
    # Pick keywords that appear in the query
    active_keywords = [kw for kw in all_keywords if kw in query_lower]
    # Always include at least broad terms
    if not active_keywords:
        active_keywords = query_lower.split()[:5]

    # Find seed nodes
    seed_nodes = set()
    for node in G.nodes():
        node_lower = node.lower()
        for kw in active_keywords:
            if kw in node_lower:
                seed_nodes.add(node)
                break

    # Expand 1 hop
    edges = []
    for node in seed_nodes:
        for _, target, data in G.out_edges(node, data=True):
            edges.append((node, data["predicate"], target, data.get("context", "")))
        for source, _, data in G.in_edges(node, data=True):
            edges.append((source, data["predicate"], node, data.get("context", "")))

    # Score by keyword overlap
    scored = []
    for subj, pred, obj, ctx in edges:
        text = f"{subj} {pred} {obj} {ctx}".lower()
        score = sum(1 for kw in active_keywords if kw in text)
        scored.append((score, subj, pred, obj, ctx))
    scored.sort(reverse=True)

    # Deduplicate and return top 15 as text
    seen = set()
    texts = []
    for score, subj, pred, obj, ctx in scored:
        key = (subj, pred, obj)
        if key in seen:
            continue
        seen.add(key)
        line = f"{subj} --[{pred}]--> {obj}"
        if ctx:
            line += f" ({ctx})"
        texts.append(line)
        if len(texts) >= 15:
            break

    return texts


# ---------- Main ----------

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    # Load MiniLM
    print("Loading MiniLM model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    minilm_col = client.get_collection(COLLECTION)

    # Load OpenAI (optional)
    openai_col = None
    oai = None
    try:
        import os
        from dotenv import load_dotenv
        from openai import OpenAI
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            oai = OpenAI(api_key=api_key)
            openai_col = client.get_collection(OPENAI_COLLECTION)
            print("OpenAI collection loaded.")
        else:
            print("No OPENAI_API_KEY — skipping OpenAI.")
    except Exception as e:
        print(f"OpenAI unavailable: {e}")

    # Load KG
    kg_graph = None
    if KG_PATH.exists():
        data = json.loads(KG_PATH.read_text())
        kg_graph = nx.DiGraph()
        for node in data["nodes"]:
            kg_graph.add_node(node)
        for edge in data["edges"]:
            kg_graph.add_edge(edge["source"], edge["target"],
                             predicate=edge.get("predicate", ""),
                             context=edge.get("context", ""))
        print(f"KG loaded: {len(kg_graph.nodes())} nodes, {len(kg_graph.edges())} edges")
    else:
        print("No knowledge_graph.json — skipping KG.")

    print(f"\nRunning {len(BENCHMARK)} queries...\n")
    print("=" * 80)

    # Results: {approach: {query_idx: (found, total)}}
    results = {"MiniLM": {}, "OpenAI": {}, "KG": {}}

    for i, bench in enumerate(BENCHMARK):
        cat = bench["category"]
        query = bench["query"]
        key_facts = bench["key_facts"]
        total_facts = len(key_facts)

        if verbose:
            print(f"\n{'─' * 80}")
            print(f"Q{i+1:02d} [{cat}]: {query}")
            print(f"{'─' * 80}")

        # MiniLM
        texts = query_minilm(model, minilm_col, query)
        facts = check_facts(texts, key_facts)
        found = sum(1 for _, f in facts if f)
        results["MiniLM"][i] = (found, total_facts)
        if verbose:
            print(f"  MiniLM:  {found}/{total_facts}")
            for desc, f in facts:
                print(f"    {'Y' if f else 'N'} {desc}")

        # OpenAI
        if oai and openai_col:
            texts = query_openai(oai, openai_col, query)
            facts = check_facts(texts, key_facts)
            found = sum(1 for _, f in facts if f)
            results["OpenAI"][i] = (found, total_facts)
            if verbose:
                print(f"  OpenAI:  {found}/{total_facts}")
                for desc, f in facts:
                    print(f"    {'Y' if f else 'N'} {desc}")
        else:
            results["OpenAI"][i] = (-1, total_facts)

        # KG
        if kg_graph:
            texts = query_kg(kg_graph, query)
            facts = check_facts(texts, key_facts)
            found = sum(1 for _, f in facts if f)
            results["KG"][i] = (found, total_facts)
            if verbose:
                print(f"  KG:      {found}/{total_facts}")
                for desc, f in facts:
                    print(f"    {'Y' if f else 'N'} {desc}")
        else:
            results["KG"][i] = (-1, total_facts)

    # ---------- Summary ----------
    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS")
    print("=" * 80)

    # Per-query table
    header = f"{'#':<4} {'Category':<16} {'MiniLM':<10} {'OpenAI':<10} {'KG':<10} Query"
    print(f"\n{header}")
    print("─" * 100)

    for i, bench in enumerate(BENCHMARK):
        cat = bench["category"]
        query_short = bench["query"][:40] + "..." if len(bench["query"]) > 40 else bench["query"]

        cells = []
        for approach in ["MiniLM", "OpenAI", "KG"]:
            found, total = results[approach][i]
            if found == -1:
                cells.append("SKIP")
            else:
                cells.append(f"{found}/{total}")

        print(f"Q{i+1:02d} {cat:<16} {cells[0]:<10} {cells[1]:<10} {cells[2]:<10} {query_short}")

    # Category breakdown
    print(f"\n{'─' * 80}")
    print("CATEGORY BREAKDOWN (% of facts found)")
    print(f"{'─' * 80}")

    categories = ["Relational", "Factual", "API", "Troubleshooting", "Conceptual"]
    cat_header = f"{'Category':<16} {'MiniLM':<12} {'OpenAI':<12} {'KG':<12}"
    print(cat_header)

    for cat in categories:
        cat_scores = {"MiniLM": (0, 0), "OpenAI": (0, 0), "KG": (0, 0)}
        for i, bench in enumerate(BENCHMARK):
            if bench["category"] != cat:
                continue
            for approach in ["MiniLM", "OpenAI", "KG"]:
                found, total = results[approach][i]
                if found >= 0:
                    prev_f, prev_t = cat_scores[approach]
                    cat_scores[approach] = (prev_f + found, prev_t + total)

        cells = []
        for approach in ["MiniLM", "OpenAI", "KG"]:
            f, t = cat_scores[approach]
            if t == 0:
                cells.append("SKIP")
            else:
                pct = (f / t) * 100
                cells.append(f"{f}/{t} ({pct:.0f}%)")

        print(f"{cat:<16} {cells[0]:<12} {cells[1]:<12} {cells[2]:<12}")

    # Overall
    print(f"\n{'─' * 80}")
    print("OVERALL")
    print(f"{'─' * 80}")

    for approach in ["MiniLM", "OpenAI", "KG"]:
        total_found = 0
        total_possible = 0
        for i in range(len(BENCHMARK)):
            found, total = results[approach][i]
            if found >= 0:
                total_found += found
                total_possible += total
        if total_possible > 0:
            pct = (total_found / total_possible) * 100
            print(f"  {approach:<10} {total_found}/{total_possible} facts ({pct:.0f}%)")
        else:
            print(f"  {approach:<10} SKIPPED")


if __name__ == "__main__":
    main()
