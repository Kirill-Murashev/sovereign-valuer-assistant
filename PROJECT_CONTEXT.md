# PROJECT_CONTEXT.md

## 1. Project Name

**Canonical project name:** Sovereign Valuer Assistant  
**Repository name:** `sovereign-valuer-assistant`  
**Short name:** SVA  
**Codename:** Elessar

Sovereign Valuer Assistant is an open-source, local-first pet project for building a personal LLM assistant for valuation professionals.

The project is intended to help appraisers and valuation experts work with professional knowledge, valuation reports, standards, market data, calculations, and reusable domain-specific skills.

---

## 2. Project Purpose

The purpose of the project is to create a controlled digital assistant for valuation professionals.

The assistant should help with:

- working with valuation standards and methodological materials;
- reviewing valuation reports;
- drafting valuation-related text fragments;
- checking consistency of assumptions, dates, sources, and calculations;
- working with local knowledge bases;
- using structured valuation data from verified APIs and local databases;
- maintaining approved professional memory;
- reducing unnecessary token usage by relying on direct data tools instead of free-form web or LLM search.

The system is not intended to be an autonomous replacement for a valuation professional.

The system should support the expert, not substitute the expert's professional judgement.

---

## 3. Project Motivation

The project is designed as a practical open-source tool for valuation professionals who need a sovereign, inspectable, and locally deployable assistant.

The project should remain useful for people who cannot rely on expensive commercial AI ecosystems or foreign cloud infrastructure.

The system should be able to run on:

- a local personal computer;
- a private VPS;
- a small private server.

---

## 4. Current Working Model

The project uses the following working model:

```text
Human user = product owner, domain expert, and strategic decision-maker.
ChatGPT = project lead, architect, supervisor, and reviewer.
Cursor = implementation executor for small coding tasks.
```

The human user provides:

- ideas;
- strategic priorities;
- valuation methodology;
- professional constraints;
- approval of architectural decisions;
- final validation of outputs.

ChatGPT provides:

- architectural design;
- task decomposition;
- prompts for Cursor;
- code review guidance;
- documentation drafts;
- roadmap planning;
- risk control;
- quality control.

Cursor provides:

- implementation of concrete coding tasks;
- small file changes;
- module generation;
- refactoring under explicit instructions;
- local development assistance.

Cursor and other coding agents must follow `AGENTS.md`.

---

## 5. Development Constraints

The project is a pet project, not an enterprise-funded product.

Current constraints:

- available development time: approximately 2–8 hours per week;
- primary implementation tool: Cursor;
- target deployment: local PC or VPS;
- preferred approach: simple, controlled, inspectable architecture;
- initial implementation language: Python;
- default LLM provider: GigaChat;
- priority: practical usefulness over architectural perfection.

The project should avoid unnecessary complexity.

The first versions should be small, local-first, and easy to understand.

---

## 6. Core architectural decision

The initial architecture should not start with a heavy autonomous agent framework.

The project should start with a **simple, local-first, controlled** architecture:

```text
Python application
    ↓
GigaChat
    ↓
local knowledge base
    ↓
RAG search
    ↓
Markdown/YAML skills
    ↓
approved memory
    ↓
structured Data Layer tools
```

Future additions may include:

- FastAPI;
- Docker;
- Qdrant;
- PostgreSQL;
- LangGraph or GigaChain workflows;
- Langfuse observability;
- web interface;
- API integrations with external valuation-related services.

These additions should be introduced only when the simpler version is already working.

---

## 7. Initial Technical Stack

The initial stack should be intentionally simple.

### Required early components

- Python;
- GigaChat integration;
- local configuration through `.env`;
- CLI or simple local interface;
- local `knowledge_base/` folder;
- local `skills/` folder;
- local `memory/` folder;
- Markdown/YAML skill definitions;
- basic RAG over local documents;
- basic approved memory.

### Possible early dependencies

The exact dependency list may change, but the initial implementation should prefer lightweight libraries.

Possible components:

- `python-dotenv` for environment configuration;
- `pydantic` for config and schema validation;
- `pyyaml` for YAML skills;
- simple deterministic local retrieval first; vector storage only later if justified;
- simple document loaders for `.md`, `.txt`, and later `.pdf` / `.docx`.

### Components to postpone

Do not start with:

- full multi-agent orchestration;
- Hermes as the project core;
- OpenClaw as the project core;
- complex web frontend;
- PostgreSQL unless needed;
- Kubernetes or enterprise infrastructure;
- uncontrolled self-learning.

---

## 8. LLM Strategy

The default LLM is **GigaChat**.

The project should not assume OpenAI, Anthropic, Google, or other providers as defaults.

A future abstraction layer may be added, but the first implementation should keep LLM integration isolated and simple.

Preferred rule:

```text
All LLM-provider-specific code should be isolated in one module.
```

For example:

```text
app/llm.py
```

or later:

```text
sva/llm/
```

The rest of the application should call a small internal interface, not provider-specific code directly.

---

## 9. Knowledge Layer

The Knowledge Layer contains unstructured or semi-structured professional materials.

Examples:

- valuation standards;
- valuation methodology;
- books and articles;
- report templates;
- anonymized example reports;
- legal and regulatory materials;
- checklists;
- professional explanations.

Initial folder:

```text
knowledge_base/
```

The Knowledge Layer is used for RAG.

Important rules:

- source tracking is required;
- the assistant must not invent citations;
- missing sources must be reported as missing;
- retrieved content must not automatically become permanent memory;
- confidential client materials must not be committed to the public repository.

---

## 10. Skills Layer

Skills are explicit domain workflows or prompt packages.

Initial folder:

```text
skills/
```

Initial format:

```text
Markdown or YAML
```

A skill should be inspectable and editable by a human.

Possible early skills:

- valuation report review;
- FSO / valuation standards compliance check;
- market analysis support;
- comparable selection support;
- calculation check;
- court/expert opinion drafting;
- discount rate support;
- data source verification.

Example skill fields may include:

```yaml
name: report_review
description: Review a valuation report for material methodological issues.
system_prompt: |
  You are a strict valuation report reviewer.
user_prompt_template: |
  Review the following report fragment...
required_tools:
  - rag_search
  - memory_read
```

Skills should not be hidden in hard-coded prompts when a file-based definition is practical.

---

## 11. Memory Layer

The project must use controlled, approved memory.

Initial folder:

```text
memory/
```

Initial memory files may include:

```text
memory/user_profile.md
memory/approved_rules.md
memory/rejected_patterns.md
memory/project_notes.md
```

Permanent memory must be:

- explicit;
- inspectable;
- editable;
- approved by the user;
- removable;
- separated from raw chat history;
- separated from retrieved document content.

The system must not implement uncontrolled self-learning.

The system must not treat previous LLM outputs as verified professional knowledge unless approved.

Preferred memory workflow:

```text
Candidate memory → human review → approved memory
```

Not:

```text
LLM output → automatic permanent memory
```

---

## 12. Data Layer

The Data Layer is a core advantage of the project.

The assistant should not rely only on LLM reasoning or RAG when structured valuation data is available.

The Data Layer should provide verified structured data from local databases and APIs.

Examples:

- OFZ yield curve;
- key rate;
- inflation;
- exchange rates;
- market data;
- comparable transactions;
- financial ratios;
- industry multiples;
- cadastral or geographic data;
- data from the user's other projects.

Initial folder:

```text
data_hub/
```

Possible structure:

```text
data_hub/
├── connectors/
├── services/
├── tools/
└── db/
```

Data tools should return metadata, not only raw values.

A typical Data Layer response should include:

```json
{
  "value": 14.2,
  "unit": "% per annum",
  "date": "2026-05-06",
  "source": "verified API or local database",
  "updated_at": "2026-05-06T09:00:00",
  "method": "documented calculation or direct source",
  "is_stale": false
}
```

The assistant must not invent market data when a data tool is required.

---

## 13. Initial Repository Structure

The initial repository should remain simple.

Recommended first structure:

```text
sovereign-valuer-assistant/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── llm.py
│   ├── rag.py
│   ├── memory.py
│   └── skills.py
├── knowledge_base/
├── skills/
├── memory/
├── data_hub/
├── docs/
├── examples/
├── tests/
├── AGENTS.md
├── PROJECT_CONTEXT.md
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

This structure may evolve, but only through explicit architectural decisions.

---

## 14. Initial roadmap

Milestone labels below match the current repository status wording.

### Implemented (reference)

- **v0.1** — Local assistant skeleton: repository structure, configuration, CLI, skill loading, read-only memory loading, tests, documentation.
- **v0.1.1** — GigaChat smoke path (`--smoke-llm`) using the official SDK.
- **v0.1.2** — `report_review` skill runner (`--run-skill`) end-to-end through GigaChat.
- **v0.2 (draft)** — Local deterministic RAG for skill runs (`--use-rag`): chunking and keyword-overlap retrieval over `knowledge_base/` (`.md`/`.txt`).
- **v0.2.1** — Transparent RAG source output in the CLI (concise sources; `--show-rag-context` for full retrieved context).

### v0.3 — approved memory workflow *(next)*

Goal: make memory changes controlled and inspectable.

Scope:

- continue read-only loading of approved memory;
- propose candidate memory entries;
- persist only after explicit user approval;
- support a simple remember/forget-style workflow or CLI equivalent.

### v0.4 — first Data Layer tool *(later)*

Goal: integrate one structured valuation data source.

Suggested first tool:

```text
get_risk_free_rate(date, maturity_years)
```

Scope:

- connector to API or local mock database;
- metadata-rich response;
- freshness check;
- valuation-friendly explanation.

### v0.5 — broader practical valuation workflows

Goal: deepen useful workflows for valuation professionals.

Possible workflows:

- valuation report review;
- FSO compliance check;
- discount rate support;
- market analysis support;
- calculation consistency check.

---

## 15. Quality Principles

The project should prioritize:

- correctness;
- transparency;
- source traceability;
- simplicity;
- local-first operation;
- human approval for risky actions;
- clear separation between facts, assumptions, and opinions;
- small reviewable changes;
- reproducible behaviour where possible.

The assistant should clearly distinguish:

- verified facts;
- retrieved source content;
- structured data values;
- expert assumptions;
- draft text;
- uncertain conclusions.

---

## 16. Security and Privacy Principles

The public repository must not contain:

- real confidential valuation reports;
- client data;
- personal data;
- API keys;
- credentials;
- private market databases;
- non-public legal materials;
- raw working files from real cases.

Use:

```text
.env.example
.gitignore
synthetic examples
anonymized samples
```

Any real data should remain local or private.

---

## 17. Relationship to Hermes, OpenClaw, LiteLLM, and LangGraph

Current decision:

- do not use Hermes as the initial project core;
- do not use OpenClaw as the initial project core;
- do not start with a heavy multi-agent framework;
- LiteLLM may be useful later as an LLM gateway;
- LangGraph or GigaChain may be useful later for workflows;
- Qdrant and PostgreSQL may be useful later for more mature memory/RAG/data storage.

The first version should be simpler.

Preferred initial approach:

```text
plain Python modules first;
frameworks later only when justified.
```

---

## 18. Cursor Workflow

Cursor should receive small, concrete tasks.

Bad task:

```text
Build the whole Sovereign Valuer Assistant.
```

Good task:

```text
Create app/skills.py that loads YAML files from the skills/ folder, validates required fields, and returns a list of available skills.
```

Each Cursor task should specify:

- target files;
- expected behaviour;
- constraints;
- tests if applicable;
- what not to change.

Cursor must read `AGENTS.md` before making changes.

---

## 19. First milestone

The first milestone was:

```text
v0.1: local assistant skeleton
```

That milestone is **implemented**. Minimum expectations that were met include
repository structure, core documentation, `.env.example`, a starting CLI,
configuration loading, YAML skill loading, read-only memory loading, isolated LLM
integration in `app/llm.py`, and no committed secrets.

Subsequent shipped increments on `main` include **v0.1.1** (GigaChat smoke path),
**v0.1.2** (`report_review` skill runner), **v0.2 (draft)** (local deterministic RAG
for `--run-skill`), and **v0.2.1** (transparent RAG source output in the CLI).

---

## 20. Current status

As of the current `main` branch:

- **v0.1** repository skeleton is implemented.
- **v0.1.1** GigaChat smoke path (`--smoke-llm`) is implemented (requires valid credentials and network access).
- **v0.1.2** `report_review` skill runner is implemented.
- **v0.2 (draft)** local deterministic RAG for skill runs is implemented (`--use-rag`); retrieval is keyword overlap over local `.md`/`.txt` files, not vector search.
- **v0.2.1** transparent retrieved-source listing (and optional full context via `--show-rag-context`) is implemented in the CLI.
- Approved memory is **read-only** in code paths today; **v0.3** will add an explicit proposal and approval workflow before writes.
- The **Data Layer** is **planned** under `data_hub/`; **v0.4** targets a first tool such as `get_risk_free_rate(date, maturity_years)`.

The project remains a **non-production**, **local-first** draft: favour simple modules and inspectable behaviour over premature platform complexity.

**Next recommended implementation focus:** **v0.3** approved memory proposal workflow, then **v0.4** first Data Layer tool, alongside additional valuation skills as needed.

---

## 21. Working Rule

When in doubt, choose the simpler controlled solution.

The project should grow by small useful increments.

The goal is not to build a spectacular autonomous agent.

The goal is to build a trustworthy professional assistant for valuation work.
