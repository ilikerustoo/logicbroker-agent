"""Index scraped Logicbroker docs into ChromaDB with MiniLM embeddings."""

import logging
import re
from pathlib import Path

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

KB_DIR = Path("data/kb_articles")
API_DIR = Path("data/api_docs")
CHROMA_DIR = Path("data/chroma_db")
COLLECTION_NAME = "logicbroker_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
# Minimum content length to be worth indexing
MIN_CONTENT_LENGTH = 50


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file.

    Returns (metadata_dict, body_text).
    """
    if not text.startswith("---"):
        return {}, text

    end = text.find("---", 3)
    if end == -1:
        return {}, text

    front = text[3:end].strip()
    body = text[end + 3:].strip()

    metadata = {}
    for line in front.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip().strip('"').strip("'")
            metadata[key.strip()] = val

    return metadata, body


def _load_documents(directory: Path, doc_type: str) -> list[dict]:
    """Load markdown files from a directory.

    Returns list of dicts with keys: content, title, url, category, doc_type, source_path.
    """
    docs = []
    for path in sorted(directory.glob("*.md")):
        if path.name.startswith(".") or path.name.startswith("_"):
            continue

        text = path.read_text(encoding="utf-8")
        metadata, body = _parse_frontmatter(text)

        if len(body) < MIN_CONTENT_LENGTH:
            logger.debug(f"Skipping {path.name} — content too short ({len(body)} chars)")
            continue

        docs.append({
            "content": body,
            "title": metadata.get("title", path.stem),
            "url": metadata.get("url", metadata.get("source_url", "")),
            "category": metadata.get("category", doc_type),
            "doc_type": doc_type,
            "source_path": str(path),
        })

    return docs


def _chunk_documents(
    docs: list[dict],
) -> list[tuple[str, dict]]:
    """Split documents into chunks with metadata.

    Returns list of (chunk_text, metadata) tuples.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n#### ", "\n---\n", "\n\n", "\n", " "],
    )

    chunks = []
    for doc in docs:
        texts = splitter.split_text(doc["content"])
        for i, text in enumerate(texts):
            metadata = {
                "title": doc["title"],
                "source_url": doc["url"],
                "category": doc["category"],
                "doc_type": doc["doc_type"],
                "chunk_index": i,
                "total_chunks": len(texts),
            }
            chunks.append((text, metadata))

    return chunks


def index_all(
    kb_dir: Path | None = None,
    api_dir: Path | None = None,
    chroma_dir: Path | None = None,
    force_reindex: bool = False,
) -> dict:
    """Load, chunk, embed, and index all documents.

    Returns summary dict.
    """
    kb_dir = kb_dir or KB_DIR
    api_dir = api_dir or API_DIR
    chroma_dir = chroma_dir or CHROMA_DIR
    chroma_dir.mkdir(parents=True, exist_ok=True)

    # Load documents
    logger.info("Loading KB articles...")
    kb_docs = _load_documents(kb_dir, "kb_article")
    logger.info(f"  Loaded {len(kb_docs)} KB articles (skipped short/empty ones)")

    logger.info("Loading API docs...")
    api_docs = _load_documents(api_dir, "api_doc")
    logger.info(f"  Loaded {len(api_docs)} API doc files")

    all_docs = kb_docs + api_docs

    # Chunk documents
    logger.info("Chunking documents...")
    chunks = _chunk_documents(all_docs)
    logger.info(f"  Created {len(chunks)} chunks from {len(all_docs)} documents")

    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=str(chroma_dir))

    if force_reindex:
        try:
            client.delete_collection(COLLECTION_NAME)
            logger.info("  Deleted existing collection for reindex")
        except Exception:
            pass

    # Check if already indexed
    try:
        collection = client.get_collection(COLLECTION_NAME)
        if collection.count() > 0 and not force_reindex:
            logger.info(
                f"Collection '{COLLECTION_NAME}' already has {collection.count()} items. "
                "Use --force to reindex."
            )
            return {
                "status": "skipped",
                "existing_count": collection.count(),
                "reason": "already indexed",
            }
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # Load embedding model
    logger.info(f"Loading embedding model: {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Embed and store in batches
    batch_size = 100
    total_stored = 0

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c[0] for c in batch]
        metadatas = [c[1] for c in batch]
        ids = [f"chunk_{i + j}" for j in range(len(batch))]

        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )
        total_stored += len(batch)

        if total_stored % 500 == 0 or total_stored == len(chunks):
            logger.info(f"  Stored {total_stored}/{len(chunks)} chunks")

    summary = {
        "status": "indexed",
        "documents_loaded": len(all_docs),
        "kb_articles": len(kb_docs),
        "api_docs": len(api_docs),
        "chunks_created": len(chunks),
        "chunks_stored": total_stored,
        "chroma_dir": str(chroma_dir),
        "collection": COLLECTION_NAME,
    }
    logger.info(
        f"Indexing complete: {len(all_docs)} docs → {len(chunks)} chunks stored in "
        f"'{COLLECTION_NAME}'"
    )
    return summary


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    force = "--force" in sys.argv
    result = index_all(force_reindex=force)
    print(f"\nResult: {result}")
