"""Retriever interface wrapping ChromaDB for semantic search over Logicbroker docs."""

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path

import chromadb
import networkx as nx
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

CHROMA_DIR = Path("data/chroma_db")
COLLECTION_NAME = "logicbroker_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 5
KG_PATH = Path("data/knowledge_graph_v2.json")
KG_V1_PATH = Path("data/knowledge_graph.json")


@dataclass
class RetrievedChunk:
    """A retrieved document chunk with metadata and score."""

    text: str
    title: str
    source_url: str
    category: str
    doc_type: str
    chunk_index: int
    total_chunks: int
    score: float  # cosine similarity (higher = more similar)

    def __str__(self) -> str:
        return (
            f"[{self.score:.3f}] {self.title} (chunk {self.chunk_index + 1}/{self.total_chunks})\n"
            f"  Source: {self.source_url}\n"
            f"  Category: {self.category}\n"
            f"  {self.text[:200]}..."
        )


class LogicbrokerRetriever:
    """Semantic search over indexed Logicbroker documentation."""

    def __init__(
        self,
        chroma_dir: Path | None = None,
        collection_name: str = COLLECTION_NAME,
        embedding_model: str = EMBEDDING_MODEL,
    ):
        self._chroma_dir = chroma_dir or CHROMA_DIR
        self._collection_name = collection_name

        client = chromadb.PersistentClient(path=str(self._chroma_dir))
        self._collection = client.get_collection(collection_name)
        self._model = SentenceTransformer(embedding_model)

        logger.info(
            f"Retriever initialized: {self._collection.count()} chunks in "
            f"'{collection_name}'"
        )

    def query(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        doc_type_filter: str | None = None,
    ) -> list[RetrievedChunk]:
        """Search for chunks relevant to the query.

        Args:
            query: Search query text.
            top_k: Number of results to return.
            doc_type_filter: If set, only return chunks with this doc_type
                             (e.g. "api_doc", "kb_article").

        Returns top_k results ordered by relevance (highest first).
        """
        embedding = self._model.encode([query]).tolist()

        query_kwargs = {
            "query_embeddings": embedding,
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if doc_type_filter:
            query_kwargs["where"] = {"doc_type": doc_type_filter}

        results = self._collection.query(**query_kwargs)

        chunks = []
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            # ChromaDB returns cosine distance; convert to similarity
            distance = results["distances"][0][i]
            similarity = 1 - distance

            chunks.append(RetrievedChunk(
                text=results["documents"][0][i],
                title=meta.get("title", ""),
                source_url=meta.get("source_url", ""),
                category=meta.get("category", ""),
                doc_type=meta.get("doc_type", ""),
                chunk_index=meta.get("chunk_index", 0),
                total_chunks=meta.get("total_chunks", 1),
                score=similarity,
            ))

        return chunks

    @property
    def collection_size(self) -> int:
        return self._collection.count()


class KnowledgeGraphRetriever:
    """Query-aware knowledge graph retrieval for relationship/workflow questions."""

    _STOP_WORDS = {
        "what", "how", "does", "do", "is", "are", "the", "a", "an", "to",
        "and", "or", "in", "on", "at", "for", "of", "with", "from", "by",
        "can", "i", "my", "it", "this", "that", "when", "where", "which",
        "who", "after", "before", "into", "if", "then", "would", "should",
        "could", "will", "have", "has", "had", "be", "been", "being", "not",
        "about", "their", "there", "they", "them", "its", "also", "more",
        "some", "any", "all", "each", "every", "than", "other",
    }

    def __init__(self, kg_path: Path | None = None):
        path = kg_path or (KG_PATH if KG_PATH.exists() else KG_V1_PATH)
        if not path.exists():
            logger.warning(f"Knowledge graph not found at {path}")
            self._graph = nx.DiGraph()
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
        logger.info(f"KG loaded: {len(self._graph.nodes())} nodes, {len(self._graph.edges())} edges")

    def query(self, query: str, max_results: int = 25, max_hops: int = 2) -> list[str]:
        """Query the knowledge graph and return formatted relationship strings.

        Returns a list of strings like:
            "Order → [has_status] → 150 Ready to Acknowledge (initial status)"
        """
        if not self._graph.nodes():
            return []

        query_info = self._extract_query_terms(query)
        seed_nodes = self._find_matching_nodes(query_info)

        if not seed_nodes:
            return []

        edges = self._get_subgraph(seed_nodes, max_hops)
        scored = self._score_edges(edges, query_info)

        # Deduplicate and format
        seen = set()
        results = []
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

    @property
    def node_count(self) -> int:
        return len(self._graph.nodes())

    def _extract_query_terms(self, query: str) -> dict:
        text = query.lower().strip()
        phrases = re.findall(r'"([^"]+)"', text)
        words = re.findall(r'[a-z0-9/._-]+', text)
        terms = [w for w in words if w not in self._STOP_WORDS and len(w) > 1]
        bigrams = [f"{terms[i]} {terms[i+1]}" for i in range(len(terms) - 1)]
        return {"terms": terms, "bigrams": bigrams, "phrases": phrases}

    def _find_matching_nodes(self, query_info: dict, max_nodes: int = 50) -> list[str]:
        terms = query_info["terms"]
        bigrams = query_info["bigrams"]
        phrases = query_info["phrases"]

        scored_nodes = []
        for node in self._graph.nodes():
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
        return [node for _, node in scored_nodes[:max_nodes]]

    def _get_subgraph(self, seed_nodes: list[str], max_hops: int) -> list[tuple]:
        visited = set(seed_nodes)
        frontier = set(seed_nodes)
        edges = []

        for _ in range(max_hops):
            next_frontier = set()
            for node in frontier:
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

    def _score_edges(self, edges: list[tuple], query_info: dict) -> list[tuple]:
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


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "how do I set up EDI with Home Depot"
    print(f"\nQuery: {query}\n")

    retriever = LogicbrokerRetriever()
    results = retriever.query(query)

    for i, chunk in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(chunk)
