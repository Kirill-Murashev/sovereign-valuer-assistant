"""Simple deterministic local RAG helpers."""

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


def chunk_documents(
    documents: list[dict[str, str]], chunk_size: int = 800, chunk_overlap: int = 100
) -> list[dict[str, str | int]]:
    """Create deterministic overlapping chunks with source metadata."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    chunks: list[dict[str, str | int]] = []
    step = chunk_size - chunk_overlap
    for document in documents:
        text = document.get("text", "")
        source = str(document.get("source", "unknown"))
        if not isinstance(text, str) or not text:
            continue
        chunk_id = 0
        for start in range(0, len(text), step):
            end = start + chunk_size
            chunk_text = text[start:end]
            if chunk_text:
                chunks.append(
                    {
                        "source": source,
                        "chunk_id": chunk_id,
                        "text": chunk_text,
                    }
                )
                chunk_id += 1
            if end >= len(text):
                break
    return chunks


def retrieve(
    query: str, chunks: list[dict[str, str | int]], top_k: int = 5
) -> list[dict[str, str | int]]:
    """Return top chunks by deterministic keyword overlap."""
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")
    if not query or not chunks:
        return []

    query_terms = {term.lower() for term in query.split() if term.strip()}
    scored: list[tuple[int, dict[str, str | int]]] = []
    for chunk in chunks:
        text = chunk.get("text", "")
        if not isinstance(text, str):
            continue
        terms = set(text.lower().split())
        score = len(query_terms & terms)
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in scored if score > 0][:top_k]


def format_retrieved_context(chunks: list[dict[str, str | int]]) -> str:
    """Format retrieved chunks into a readable source-aware block."""
    if not chunks:
        return ""
    lines: list[str] = []
    for chunk in chunks:
        source = chunk.get("source", "unknown")
        chunk_id = chunk.get("chunk_id", "unknown")
        text = str(chunk.get("text", "")).strip()
        lines.append(f"Source: {source} | Chunk: {chunk_id}\n{text}")
    return "\n\n".join(lines)

