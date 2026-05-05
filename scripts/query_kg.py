"""Query the knowledge graph to answer multi-hop questions.

Approach:
1. Extract key entities from the query using simple keyword matching
2. Find matching nodes in the graph
3. Traverse neighbors (1-2 hops) to find related context
4. Return the subgraph as structured context for the LLM
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import networkx as nx

KG_PATH = Path("data/knowledge_graph.json")

QUERY = (
    "What status does an order have after a supplier receives it, "
    "and what API call does the supplier make to advance it to Ready to Ship?"
)


def load_graph():
    data = json.loads(KG_PATH.read_text())
    G = nx.DiGraph()
    for node in data["nodes"]:
        G.add_node(node)
    for edge in data["edges"]:
        G.add_edge(edge["source"], edge["target"],
                   predicate=edge.get("predicate", ""),
                   context=edge.get("context", ""))
    return G, data["triples"]


def find_relevant_nodes(G, query):
    """Find nodes that match query terms."""
    query_lower = query.lower()
    keywords = ["order", "supplier", "status", "ready to ship", "acknowledge",
                "acknowledgement", "api", "post", "advance", "150", "500"]

    matches = set()
    for node in G.nodes():
        node_lower = node.lower()
        for kw in keywords:
            if kw in node_lower:
                matches.add(node)
                break

    return matches


def get_subgraph(G, seed_nodes, max_hops=2):
    """Get all edges within max_hops of seed nodes."""
    visited = set(seed_nodes)
    frontier = set(seed_nodes)
    edges = []

    for hop in range(max_hops):
        next_frontier = set()
        for node in frontier:
            # Outgoing
            for _, target, data in G.out_edges(node, data=True):
                edges.append((node, data["predicate"], target, data.get("context", "")))
                if target not in visited:
                    next_frontier.add(target)
                    visited.add(target)
            # Incoming
            for source, _, data in G.in_edges(node, data=True):
                edges.append((source, data["predicate"], node, data.get("context", "")))
                if source not in visited:
                    next_frontier.add(source)
                    visited.add(source)
        frontier = next_frontier

    return edges


def score_edges(edges, query):
    """Score edges by relevance to the query."""
    query_lower = query.lower()
    high_value_terms = ["order", "acknowledge", "status", "ready to ship",
                        "supplier", "post", "api", "150", "500", "advance"]

    scored = []
    for subj, pred, obj, ctx in edges:
        score = 0
        text = f"{subj} {pred} {obj} {ctx}".lower()
        for term in high_value_terms:
            if term in text:
                score += 1
        scored.append((score, subj, pred, obj, ctx))

    scored.sort(reverse=True)
    return scored


def main():
    print(f"Query: {QUERY}\n")
    print("=" * 70)
    print("KNOWLEDGE GRAPH RETRIEVAL")
    print("=" * 70)

    G, triples = load_graph()
    print(f"Graph: {len(G.nodes())} nodes, {len(G.edges())} edges\n")

    # Step 1: Find relevant seed nodes
    seed_nodes = find_relevant_nodes(G, QUERY)
    print(f"Seed nodes ({len(seed_nodes)}):")
    for node in sorted(seed_nodes)[:20]:
        print(f"  • {node}")
    if len(seed_nodes) > 20:
        print(f"  ... and {len(seed_nodes) - 20} more")

    # Step 2: Expand to subgraph
    edges = get_subgraph(G, seed_nodes, max_hops=1)
    print(f"\nSubgraph: {len(edges)} edges within 1 hop\n")

    # Step 3: Score and rank
    scored = score_edges(edges, QUERY)

    print("Top 25 most relevant relationships:")
    seen = set()
    count = 0
    for score, subj, pred, obj, ctx in scored:
        key = (subj, pred, obj)
        if key in seen:
            continue
        seen.add(key)
        ctx_str = f" ({ctx})" if ctx else ""
        print(f"  [{score}] {subj} --[{pred}]--> {obj}{ctx_str}")
        count += 1
        if count >= 25:
            break

    # Step 4: Format as context for LLM
    print("\n" + "=" * 70)
    print("CONTEXT FOR LLM (what would be passed to the answer generator)")
    print("=" * 70)

    context_lines = []
    seen = set()
    for score, subj, pred, obj, ctx in scored[:40]:
        key = (subj, pred, obj)
        if key in seen:
            continue
        seen.add(key)
        line = f"- {subj} {pred} {obj}"
        if ctx:
            line += f" ({ctx})"
        context_lines.append(line)

    print("\n".join(context_lines))

    # Check: does the graph have what we need?
    print("\n" + "=" * 70)
    print("VERIFICATION: Does the graph contain the key facts?")
    print("=" * 70)

    needed = [
        ("status 150", "Ready to Acknowledge"),
        ("status 500", "Ready to Ship"),
        ("POST /api/v3/Acknowledgements", "creates Acknowledgement"),
        ("Acknowledgement", "advances order"),
    ]

    for fact, desc in needed:
        found = any(fact.lower() in f"{s} {p} {o} {c}".lower()
                    for _, s, p, o, c in scored)
        status = "✓ FOUND" if found else "✗ MISSING"
        print(f"  {status}: {desc} ({fact})")


if __name__ == "__main__":
    main()
