"""Retriever interface wrapping ChromaDB for semantic search over Logicbroker docs."""

import logging
from dataclasses import dataclass
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

CHROMA_DIR = Path("data/chroma_db")
COLLECTION_NAME = "logicbroker_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 5


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

    def query(self, query: str, top_k: int = DEFAULT_TOP_K) -> list[RetrievedChunk]:
        """Search for chunks relevant to the query.

        Returns top_k results ordered by relevance (highest first).
        """
        embedding = self._model.encode([query]).tolist()

        results = self._collection.query(
            query_embeddings=embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

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
