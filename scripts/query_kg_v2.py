"""Query-aware knowledge graph retrieval.

v2 improvements:
- Extracts keywords from the actual query (no hardcoded terms)
- Fuzzy node matching with partial string overlap
- Weighted scoring based on query term positions
- Returns structured context suitable for LLM consumption
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import networkx as nx

KG_PATH = Path("data/knowledge_graph_v2.json")
KG_V1_PATH = Path("data/knowledge_graph.json")


def load_graph(path=None):
    """Load graph, preferring v2 if available."""
    if path is None:
        path = KG_PATH if KG_PATH.exists() else KG_V1_PATH

    data = json.loads(path.read_text())
    G = nx.DiGraph()
    for node in data["nodes"]:
        G.add_node(node)
    for edge in data["edges"]:
        G.add_edge(
            edge["source"], edge["target"],
            predicate=edge.get("predicate", ""),
            context=edge.get("context", ""),
        )
    return G


def extract_query_terms(query):
    """Extract meaningful terms from a query for node matching.

    Removes stop words and returns both individual terms and multi-word phrases.
    """
    stop_words = {
        "what", "how", "does", "do", "is", "are", "the", "a", "an", "to",
        "and", "or", "in", "on", "at", "for", "of", "with", "from", "by",
        "can", "i", "my", "it", "this", "that", "when", "where", "which",
        "who", "after", "before", "into", "if", "then", "would", "should",
        "could", "will", "have", "has", "had", "be", "been", "being", "not",
        "about", "their", "there", "they", "them", "its", "also", "more",
        "some", "any", "all", "each", "every", "than", "other",
    }

    # Normalize
    text = query.lower().strip()

    # Extract quoted phrases first
    phrases = re.findall(r'"([^"]+)"', text)

    # Split into words
    words = re.findall(r'[a-z0-9/._-]+', text)
    terms = [w for w in words if w not in stop_words and len(w) > 1]

    # Build bigrams for multi-word entity matching
    bigrams = [f"{terms[i]} {terms[i+1]}" for i in range(len(terms) - 1)]

    return {
        "terms": terms,
        "bigrams": bigrams,
        "phrases": phrases,
    }


def find_matching_nodes(G, query_info, max_nodes=50):
    """Find nodes that match query terms with fuzzy matching.

    Scores each node by how many query terms it contains.
    """
    terms = query_info["terms"]
    bigrams = query_info["bigrams"]
    phrases = query_info["phrases"]

    scored_nodes = []
    for node in G.nodes():
        node_lower = node.lower()
        score = 0

        # Exact phrase matches (highest value)
        for phrase in phrases:
            if phrase in node_lower:
                score += 5

        # Bigram matches
        for bigram in bigrams:
            if bigram in node_lower:
                score += 3

        # Individual term matches
        for term in terms:
            if term in node_lower:
                score += 1

        if score > 0:
            scored_nodes.append((score, node))

    scored_nodes.sort(reverse=True)
    return [node for _, node in scored_nodes[:max_nodes]]


def get_subgraph(G, seed_nodes, max_hops=2):
    """Expand seed nodes by traversing edges up to max_hops."""
    visited = set(seed_nodes)
    frontier = set(seed_nodes)
    edges = []

    for _ in range(max_hops):
        next_frontier = set()
        for node in frontier:
            for _, target, data in G.out_edges(node, data=True):
                edges.append((node, data["predicate"], target, data.get("context", "")))
                if target not in visited:
                    next_frontier.add(target)
                    visited.add(target)
            for source, _, data in G.in_edges(node, data=True):
                edges.append((source, data["predicate"], node, data.get("context", "")))
                if source not in visited:
                    next_frontier.add(source)
                    visited.add(source)
        frontier = next_frontier

    return edges


def score_edges(edges, query_info):
    """Score edges by relevance to the query."""
    terms = query_info["terms"]
    bigrams = query_info["bigrams"]
    phrases = query_info["phrases"]

    scored = []
    for subj, pred, obj, ctx in edges:
        text = f"{subj} {pred} {obj} {ctx}".lower()
        score = 0

        for phrase in phrases:
            if phrase in text:
                score += 5
        for bigram in bigrams:
            if bigram in text:
                score += 3
        for term in terms:
            if term in text:
                score += 1

        if score > 0:
            scored.append((score, subj, pred, obj, ctx))

    scored.sort(reverse=True)
    return scored


def query_kg(query, max_results=30, max_hops=2, kg_path=None):
    """Query the knowledge graph and return formatted context.

    Args:
        query: Natural language question
        max_results: Maximum number of relationships to return
        max_hops: How far to traverse from seed nodes
        kg_path: Override path to knowledge graph JSON

    Returns:
        List of formatted relationship strings suitable for LLM context
    """
    G = load_graph(kg_path)

    query_info = extract_query_terms(query)
    seed_nodes = find_matching_nodes(G, query_info)

    if not seed_nodes:
        return []

    edges = get_subgraph(G, seed_nodes, max_hops=max_hops)
    scored = score_edges(edges, query_info)

    # Deduplicate and format
    seen = set()
    results = []
    for score, subj, pred, obj, ctx in scored:
        key = (subj.lower(), pred.lower(), obj.lower())
        if key in seen:
            continue
        seen.add(key)

        line = f"{subj} → [{pred}] → {obj}"
        if ctx:
            line += f" ({ctx})"
        results.append(line)

        if len(results) >= max_results:
            break

    return results


def main():
    """Interactive demo of the query-aware KG retrieval."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?",
                        default="What status does an order have after acknowledgement, and how does a supplier send one?")
    parser.add_argument("--max-results", type=int, default=30)
    parser.add_argument("--max-hops", type=int, default=2)
    args = parser.parse_args()

    print(f"Query: {args.query}\n")

    results = query_kg(args.query, max_results=args.max_results, max_hops=args.max_hops)

    if not results:
        print("No relevant relationships found in the knowledge graph.")
        return

    print(f"Found {len(results)} relevant relationships:\n")
    for r in results:
        print(f"  • {r}")


if __name__ == "__main__":
    main()
