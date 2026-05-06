from app.rag import chunk_documents, format_retrieved_context, load_documents, retrieve


def test_load_documents_reads_md_and_txt(tmp_path):
    (tmp_path / "a.md").write_text("alpha beta", encoding="utf-8")
    (tmp_path / "b.txt").write_text("gamma delta", encoding="utf-8")
    docs = load_documents(tmp_path)
    assert len(docs) == 2
    assert all("source" in doc and "text" in doc for doc in docs)


def test_chunk_documents_preserves_source_and_chunk_id():
    docs = [{"source": "doc.md", "text": "abcdefghij"}]
    chunks = chunk_documents(docs, chunk_size=4, chunk_overlap=1)
    assert len(chunks) >= 2
    assert chunks[0]["source"] == "doc.md"
    assert chunks[0]["chunk_id"] == 0
    assert "text" in chunks[0]


def test_retrieve_returns_source_aware_chunks():
    chunks = [
        {"source": "a.md", "chunk_id": 0, "text": "valuation date source"},
        {"source": "b.md", "chunk_id": 1, "text": "unrelated words"},
    ]
    result = retrieve("valuation source", chunks, top_k=5)
    assert len(result) == 1
    assert result[0]["source"] == "a.md"
    assert result[0]["chunk_id"] == 0


def test_format_retrieved_context():
    chunks = [{"source": "a.md", "chunk_id": 2, "text": "sample context"}]
    text = format_retrieved_context(chunks)
    assert "Source: a.md | Chunk: 2" in text
    assert "sample context" in text
