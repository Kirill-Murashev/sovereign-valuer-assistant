# Architecture (current draft)

Sovereign Valuer Assistant keeps a **simple, local-first** pipeline: one CLI entry point, explicit configuration, and provider-specific LLM code isolated in `app/llm.py`.

## Implemented flow

1. **CLI** (`app/main.py`) — parses flags (`--smoke-llm`, `--run-skill`, `--use-rag`, `--show-rag-context`, etc.).
2. **Settings** (`app/config.py`) — loads environment-based configuration.
3. **Memory loader** (`app/memory.py`) — reads approved markdown from `memory/` (read-only in the current implementation).
4. **Skill loader** (`app/skills.py`) — loads and validates YAML skills from `skills/`.
5. **Optional local RAG** (`app/rag.py`) — when `--use-rag` is used with `--run-skill`, loads and chunks `knowledge_base/` documents, retrieves chunks by deterministic keyword overlap, and formats context for the prompt.
6. **Prompt builder** (`app/prompting.py`) — combines skill prompts, formatted memory, optional retrieved context, and user input.
7. **GigaChat LLM client** (`app/llm.py`) — sends system and user messages via the official GigaChat SDK.

Retrieved knowledge is labeled as source material in prompts; it is not treated as approved permanent memory.

## Current limitations

- No embeddings and no vector database; retrieval is deterministic keyword overlap.
- No automatic memory writes; approved memory files are loaded only.
- No Data Layer tool is implemented yet (`data_hub/` remains structural placeholder).

The architecture is intended to stay inspectable and suitable for local PC or VPS deployment.
