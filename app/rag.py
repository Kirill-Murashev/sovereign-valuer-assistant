"""Simple deterministic placeholders for local RAG pipeline."""

from __future__ import annotations

from pathlib import Path


def load_documents(knowledge_base_dir: str | Path) -> list[dict[str, str]]:
    """Load plain text and markdown documents from the knowledge base."""
    base_path = Path(knowledge_base_dir)
    if not base_path.exists():
        return []

    documents: list[dict[str, str]] = []
    for ext in ("*.txt", "*.md"):
        for file_path in sorted(base_path.rglob(ext)):
            documents.append(
                {
                    "source": str(file_path),
                    "text": file_path.read_text(encoding="utf-8"),
                }
            )
    return documents


def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 100) -> list[str]:
    """Create deterministic overlapping chunks from plain text."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    if not text:
        return []

    chunks: list[str] = []
    step = chunk_size - chunk_overlap
    for start in range(0, len(text), step):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
    return chunks


def retrieve(query: str, chunks: list[str], top_k: int = 5) -> list[str]:
    """Return top chunks by simple keyword overlap score."""
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")
    if not query or not chunks:
        return []

    query_terms = {term.lower() for term in query.split() if term.strip()}
    scored: list[tuple[int, str]] = []
    for chunk in chunks:
        terms = set(chunk.lower().split())
        score = len(query_terms & terms)
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in scored if score > 0][:top_k]

