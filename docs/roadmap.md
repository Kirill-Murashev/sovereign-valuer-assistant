# Roadmap (current draft)

This file summarizes release-oriented milestones. The project keeps a **simple
local-first architecture** first; heavier storage, embeddings, and orchestration
frameworks are out of scope until explicitly needed.

## Implemented (main branch)

| Milestone | Summary |
|-----------|---------|
| **v0.1** | Repository skeleton: app layout, config, skill and memory loading, tests, CI, documentation. |
| **v0.1.1** | GigaChat smoke path: `--smoke-llm` with the official SDK. |
| **v0.1.2** | `report_review` skill runner: `--run-skill` with prompts built from YAML + read-only memory. |
| **v0.2 (draft)** | Local deterministic RAG for skill runs: `--use-rag` over `.md`/`.txt` in `knowledge_base/`. |
| **v0.2.1** | Transparent RAG source output in the CLI (concise sources; `--show-rag-context` for full retrieved context). |

Also in place: read-only loading of approved memory from `memory/`.

## Next

| Milestone | Summary |
|-----------|---------|
| **v0.3** *(next)* | Approved memory **proposal** workflow: candidate entries require explicit user approval before persisting. |
| **v0.4** *(later)* | First **Data Layer** tool (e.g. `get_risk_free_rate(date, maturity_years)`) with metadata-rich responses. |

## Later

- Additional valuation skills (beyond `report_review`).
- Incremental improvements to deterministic local RAG (still inspectable; no mandatory migration to embeddings or vector databases).
