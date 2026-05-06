# Architecture (v0.1 Draft)

Sovereign Valuer Assistant v0.1 uses a simple local-first Python architecture:

1. `app/main.py` loads settings, memory, and skills.
2. `app/llm.py` isolates provider-specific LLM integration (placeholder now).
3. `app/rag.py` contains deterministic document loading/chunking placeholders.
4. `memory/` stores explicit approved memory files.
5. `skills/` stores human-readable YAML skill definitions.
6. `knowledge_base/` stores local source documents for future RAG.

No heavy orchestration framework is used at this stage.
