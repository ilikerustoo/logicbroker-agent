"""Enhanced Knowledge Graph Retriever using OpenAI embeddings.

Drop-in replacement for EnhancedKnowledgeGraphRetriever that uses
text-embedding-3-small instead of all-MiniLM-L6-v2 for all embedding
operations (node lookup, edge scoring, community matching).
"""

import hashlib
import json
import logging
from pathlib import Path

import networkx as nx
import numpy as np
import openai
from networkx.algorithms.community import louvain_communities

logger = logging.getLogger(__name__)

KG_PATH = Path("data/knowledge_graph_v2.json")
KG_V1_PATH = Path("data/knowledge_graph.json")
CACHE_DIR = Path("data/kg_cache")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
BATCH_SIZE = 2048  # OpenAI allows up to 2048 inputs per request


def _batch_embed(texts: list[str], model: str = OPENAI_EMBEDDING_MODEL) -> np.ndarray:
    """Embed texts in batches using OpenAI API."""
    client = openai.OpenAI()
    all_embeddings = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        response = client.embeddings.create(input=batch, model=model)
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)

    return np.array(all_embeddings, dtype=np.float32)


class OpenAIKnowledgeGraphRetriever:
    """KG retriever using OpenAI embeddings for node lookup and community summaries."""

    def __init__(
        self,
        kg_path: Path | None = None,
        cache_dir: Path | None = None,
        embedding_model: str = OPENAI_EMBEDDING_MODEL,
    ):
        self._embedding_model = embedding_model
        path = kg_path or (KG_PATH if KG_PATH.exists() else KG_V1_PATH)
        self._cache_dir = cache_dir or CACHE_DIR
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            logger.warning(f"Knowledge graph not found at {path}")
            self._graph = nx.DiGraph()
            self._nodes = []
            self._node_embeddings = np.array([])
            self._communities = []
            self._community_summaries = []
            self._community_embeddings = np.array([])
            return

        data = json.loads(path.read_text())
        self._graph = nx.DiGraph()
        for node in data["nodes"]:
            self._graph.add_node(node)
        for edge in data["edges"]:
            self._graph.add_edge(
                edge["source"], edge["target"],
                predicate=edge.get("predicate", ""),
                context=edge.get("context", ""),
            )

        self._nodes = list(self._graph.nodes())

        # Build or load cached embeddings and communities
        kg_hash = hashlib.md5(path.read_bytes()).hexdigest()[:10]
        cache_prefix = f"openai_{embedding_model.replace('-', '_')}"
        self._node_embeddings = self._load_or_build_node_embeddings(kg_hash, cache_prefix)
        self._communities = self._detect_communities()
        self._community_summaries = self._load_or_build_community_summaries(kg_hash)
        self._community_embeddings = self._load_or_build_community_embeddings(kg_hash, cache_prefix)

        logger.info(
            f"OpenAI KG loaded: {len(self._nodes)} nodes, "
            f"{len(self._graph.edges())} edges, "
            f"{len(self._communities)} communities"
        )

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def community_count(self) -> int:
        return len(self._communities)

    _STOP_WORDS = {
        "what", "how", "does", "do", "is", "are", "the", "a", "an", "to",
        "and", "or", "in", "on", "at", "for", "of", "with", "from", "by",
        "can", "i", "my", "it", "this", "that", "when", "where", "which",
        "who", "after", "before", "into", "if", "then", "would", "should",
        "could", "will", "have", "has", "had", "be", "been", "being", "not",
        "about", "their", "there", "they", "them", "its", "also", "more",
        "some", "any", "all", "each", "every", "than", "other",
    }

    def query(self, query: str, max_results: int = 30, max_hops: int = 3) -> list[str]:
        """Query using hybrid node matching (keyword + OpenAI embedding RRF) + community summaries."""
        if not self._nodes:
            return []

        query_embedding = self._embed_query(query)

        # 1. Find seed nodes via hybrid: keyword + embedding with RRF
        seed_nodes = self._find_nodes_hybrid(query, query_embedding, top_k=20)

        # 2. Find relevant communities via summary embeddings
        community_context = self._find_relevant_communities(query_embedding, top_k=3)

        # 3. Expand subgraph from seed nodes
        edges = self._get_subgraph(seed_nodes, max_hops)

        # 4. Score edges by relevance to query embedding
        scored = self._score_edges_by_embedding(edges, query_embedding)

        # Format results — community summaries first, then edges
        results = []

        for summary in community_context:
            results.append(f"[Community] {summary}")

        seen = set()
        for _, subj, pred, obj, ctx in scored:
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

    def _embed_query(self, query: str) -> np.ndarray:
        """Embed a single query using OpenAI."""
        client = openai.OpenAI()
        response = client.embeddings.create(input=[query], model=self._embedding_model)
        return np.array(response.data[0].embedding, dtype=np.float32)

    def _find_nodes_hybrid(
        self, query: str, query_embedding: np.ndarray, top_k: int = 20
    ) -> list[str]:
        """Find seed nodes using Reciprocal Rank Fusion of keyword + embedding results."""
        k = 60  # RRF constant

        keyword_ranked = self._keyword_rank_nodes(query)
        embedding_ranked = self._embedding_rank_nodes(query_embedding)

        rrf_scores: dict[str, float] = {}
        for rank, node in enumerate(keyword_ranked):
            rrf_scores[node] = rrf_scores.get(node, 0) + 1.0 / (k + rank + 1)
        for rank, node in enumerate(embedding_ranked):
            rrf_scores[node] = rrf_scores.get(node, 0) + 1.0 / (k + rank + 1)

        sorted_nodes = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [node for node, _ in sorted_nodes[:top_k]]

    def _keyword_rank_nodes(self, query: str) -> list[str]:
        """Rank nodes by keyword overlap."""
        import re
        text = query.lower().strip()
        phrases = re.findall(r'"([^"]+)"', text)
        words = re.findall(r'[a-z0-9/._-]+', text)
        terms = [w for w in words if w not in self._STOP_WORDS and len(w) > 1]
        bigrams = [f"{terms[i]} {terms[i+1]}" for i in range(len(terms) - 1)]

        scored_nodes = []
        for node in self._nodes:
            node_lower = node.lower()
            score = 0
            for phrase in phrases:
                if phrase in node_lower:
                    score += 5
            for bigram in bigrams:
                if bigram in node_lower:
                    score += 3
            for term in terms:
                if term in node_lower:
                    score += 1
            if score > 0:
                scored_nodes.append((score, node))

        scored_nodes.sort(reverse=True)
        return [node for _, node in scored_nodes[:50]]

    def _embedding_rank_nodes(self, query_embedding: np.ndarray) -> list[str]:
        """Rank nodes by embedding cosine similarity."""
        if len(self._node_embeddings) == 0:
            return []

        query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-8)
        node_norms = self._node_embeddings / (
            np.linalg.norm(self._node_embeddings, axis=1, keepdims=True) + 1e-8
        )
        similarities = node_norms @ query_norm

        top_indices = np.argsort(similarities)[-50:][::-1]
        return [self._nodes[i] for i in top_indices]

    def _find_relevant_communities(self, query_embedding: np.ndarray, top_k: int = 3) -> list[str]:
        """Find community summaries most relevant to the query."""
        if len(self._community_embeddings) == 0 or not self._community_summaries:
            return []

        query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-8)
        comm_norms = self._community_embeddings / (
            np.linalg.norm(self._community_embeddings, axis=1, keepdims=True) + 1e-8
        )
        similarities = comm_norms @ query_norm

        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [
            self._community_summaries[i]
            for i in top_indices
            if similarities[i] > 0.2
        ]

    def _get_subgraph(self, seed_nodes: list[str], max_hops: int) -> list[tuple]:
        """Expand subgraph from seed nodes."""
        visited = set(seed_nodes)
        frontier = set(seed_nodes)
        edges = []

        for _ in range(max_hops):
            next_frontier = set()
            for node in frontier:
                if node not in self._graph:
                    continue
                for _, target, data in self._graph.out_edges(node, data=True):
                    edges.append((node, data["predicate"], target, data.get("context", "")))
                    if target not in visited:
                        next_frontier.add(target)
                        visited.add(target)
                for source, _, data in self._graph.in_edges(node, data=True):
                    edges.append((source, data["predicate"], node, data.get("context", "")))
                    if source not in visited:
                        next_frontier.add(source)
                        visited.add(source)
            frontier = next_frontier

        return edges

    def _score_edges_by_embedding(
        self, edges: list[tuple], query_embedding: np.ndarray
    ) -> list[tuple]:
        """Score edges by embedding similarity of their text representation."""
        if not edges:
            return []

        edge_texts = [
            f"{subj} {pred} {obj} {ctx}" for subj, pred, obj, ctx in edges
        ]

        # Batch embed edges with OpenAI
        edge_embeddings = _batch_embed(edge_texts, model=self._embedding_model)
        query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-8)
        edge_norms = edge_embeddings / (
            np.linalg.norm(edge_embeddings, axis=1, keepdims=True) + 1e-8
        )
        similarities = edge_norms @ query_norm

        scored = [
            (float(similarities[i]), edges[i][0], edges[i][1], edges[i][2], edges[i][3])
            for i in range(len(edges))
        ]
        scored.sort(reverse=True, key=lambda x: x[0])
        return scored

    # --- Caching and building ---

    def _load_or_build_node_embeddings(self, kg_hash: str, cache_prefix: str) -> np.ndarray:
        """Load cached node embeddings or build them with OpenAI."""
        cache_path = self._cache_dir / f"{cache_prefix}_node_embeddings_{kg_hash}.npy"
        if cache_path.exists():
            logger.info(f"Loading cached OpenAI node embeddings from {cache_path}")
            return np.load(cache_path)

        logger.info(f"Building OpenAI node embeddings for {len(self._nodes)} nodes...")
        embeddings = _batch_embed(self._nodes, model=self._embedding_model)
        np.save(cache_path, embeddings)
        return embeddings

    def _detect_communities(self) -> list[set]:
        """Detect communities using Louvain on the undirected version of the graph."""
        if len(self._graph.nodes()) < 5:
            return []

        undirected = self._graph.to_undirected()
        communities = louvain_communities(undirected, resolution=1.0, seed=42)
        communities = [c for c in communities if len(c) >= 3]
        communities.sort(key=len, reverse=True)
        logger.info(f"Detected {len(communities)} communities (min 3 nodes)")
        return communities

    def _load_or_build_community_summaries(self, kg_hash: str) -> list[str]:
        """Load cached community summaries (shared with MiniLM variant — same graph structure)."""
        cache_path = self._cache_dir / f"community_summaries_{kg_hash}.json"
        if cache_path.exists():
            logger.info(f"Loading cached community summaries from {cache_path}")
            return json.loads(cache_path.read_text())

        # Build template summaries (same logic as MiniLM variant)
        logger.info(f"Building community summaries for {len(self._communities)} communities...")
        summaries = []
        for community in self._communities:
            summary = self._summarize_community(community)
            summaries.append(summary)

        cache_path.write_text(json.dumps(summaries, indent=2))
        return summaries

    def _load_or_build_community_embeddings(self, kg_hash: str, cache_prefix: str) -> np.ndarray:
        """Load cached community embeddings or build them with OpenAI."""
        cache_path = self._cache_dir / f"{cache_prefix}_community_embeddings_{kg_hash}.npy"
        if cache_path.exists():
            return np.load(cache_path)

        if not self._community_summaries:
            return np.array([])

        embeddings = _batch_embed(self._community_summaries, model=self._embedding_model)
        np.save(cache_path, embeddings)
        return embeddings

    def _summarize_community(self, community: set) -> str:
        """Generate a text summary of a community."""
        nodes_in_community = list(community)

        internal_edges = []
        for source, target, data in self._graph.edges(data=True):
            if source in community and target in community:
                internal_edges.append(
                    (source, data["predicate"], target, data.get("context", ""))
                )

        if internal_edges:
            by_predicate: dict[str, list[tuple]] = {}
            for s, p, t, c in internal_edges:
                by_predicate.setdefault(p, []).append((s, t, c))

            parts = []
            sorted_preds = sorted(by_predicate.items(), key=lambda x: len(x[1]), reverse=True)
            for pred, triples in sorted_preds[:4]:
                examples = triples[:3]
                example_strs = [f"{s} → {t}" for s, t, _ in examples]
                parts.append(f"{pred}: {'; '.join(example_strs)}")

            key_nodes = nodes_in_community[:5]
            summary = (
                f"Cluster of {len(nodes_in_community)} entities including "
                f"{', '.join(key_nodes)}. "
                f"Relationships: {'. '.join(parts)}"
            )
        else:
            summary = f"Cluster of {len(nodes_in_community)} entities: {', '.join(nodes_in_community[:8])}"

        return summary

    def build_llm_community_summaries(self) -> list[str]:
        """Build LLM-generated community summaries (reuses cached if available)."""
        from langchain_anthropic import ChatAnthropic
        from langchain_core.messages import HumanMessage, SystemMessage

        llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, max_tokens=300)

        summaries = []
        for i, community in enumerate(self._communities):
            nodes_in_community = list(community)
            internal_edges = []
            for source, target, data in self._graph.edges(data=True):
                if source in community and target in community:
                    internal_edges.append(
                        f"{source} → [{data['predicate']}] → {target}"
                    )

            edge_sample = internal_edges[:20]
            node_sample = nodes_in_community[:15]

            prompt = (
                f"Summarize this knowledge graph cluster in 2-3 sentences. "
                f"Focus on what domain/topic it covers and the key relationships.\n\n"
                f"Nodes ({len(nodes_in_community)} total, showing {len(node_sample)}): "
                f"{', '.join(node_sample)}\n\n"
                f"Relationships ({len(internal_edges)} total, showing {len(edge_sample)}):\n"
                + "\n".join(f"• {e}" for e in edge_sample)
            )

            response = llm.invoke([
                SystemMessage(content="You are a knowledge graph analyst. Be concise and factual."),
                HumanMessage(content=prompt),
            ])
            summaries.append(response.content)

            if (i + 1) % 10 == 0:
                logger.info(f"  LLM-summarized {i+1}/{len(self._communities)} communities")

        # Cache summaries
        kg_hash = hashlib.md5(
            json.dumps(sorted(self._nodes)).encode()
        ).hexdigest()[:10]
        cache_path = self._cache_dir / f"community_summaries_{kg_hash}.json"
        cache_path.write_text(json.dumps(summaries, indent=2))
        self._community_summaries = summaries

        # Rebuild community embeddings with OpenAI
        cache_prefix = f"openai_{self._embedding_model.replace('-', '_')}"
        self._community_embeddings = _batch_embed(summaries, model=self._embedding_model)
        emb_cache = self._cache_dir / f"{cache_prefix}_community_embeddings_{kg_hash}.npy"
        np.save(emb_cache, self._community_embeddings)

        return summaries
