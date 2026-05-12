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
| **v0.3 (draft)** | Approved memory proposal workflow: `--propose-memory` writes proposal files under `memory/proposals/` without modifying approved memory. |
| **v0.3.1** | Proposal review helpers (implemented): `--list-memory-proposals` lists proposals and `--show-memory-proposal PATH` displays one proposal file (no automatic approval/merge). |
| **v0.3.2 (design)** | Explicit manual memory approval workflow documented in [`docs/memory_approval_workflow.md`](memory_approval_workflow.md) (policy and steps only; no approval/merge CLI). |

Also in place: read-only loading of approved memory from `memory/`.

## Next

| Milestone | Summary |
|-----------|---------|
| **v0.4** *(next)* | First **Data Layer** tool: `get_risk_free_rate(date, maturity_years)` — design in [`docs/data_layer_risk_free_rate.md`](data_layer_risk_free_rate.md); **code not implemented yet**. |

## Later

- Additional valuation skills (beyond `report_review`).
- Incremental improvements to deterministic local RAG (still inspectable; no mandatory migration to embeddings or vector databases).
- Structured Data Layer integrations after the memory proposal flow remains controlled and test-covered.
