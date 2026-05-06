# Architecture (Current Draft)

Current implemented pipeline:

`CLI`
→ `settings` (`app/config.py`)
→ `memory loader` (`app/memory.py`)
→ `skill loader` (`app/skills.py`)
→ `optional local RAG` (`app/rag.py`, enabled with `--use-rag`)
→ `prompt builder` (`app/prompting.py`)
→ `GigaChat LLM client` (`app/llm.py`)

Current limitations:

- no embeddings;
- no vector database;
- no memory writes (read-only memory flow);
- no Data Layer tool implemented yet.

The architecture remains simple, local-first, and inspectable.
