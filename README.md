# Sovereign Valuer Assistant

**Codename:** Elessar  
**Short name:** SVA  
**Repository:** `sovereign-valuer-assistant`

Sovereign Valuer Assistant is an open-source, local-first LLM assistant for valuation professionals.

The project is designed as a practical pet project for building a controlled digital assistant that can work with valuation standards, professional knowledge bases, report templates, structured valuation data, and approved long-term memory.

The default target LLM is **GigaChat**.

---

## Project Status

Current Status

The initial repository skeleton is implemented.

Implemented:

- project documentation;
- basic Python app structure;
- configuration loading;
- skill loading;
- memory loading;
- minimal GigaChat SDK client;
- optional LLM smoke test;
- CLI skill runner for report_review;
- placeholder RAG module;
- deterministic tests.
- GitHub Actions test workflow;
- Apache License 2.0 (`LICENSE`);
- contribution guidelines (`CONTRIBUTING.md`).

## Next Steps

1. Add first local RAG workflow.
2. Add approved memory proposal workflow.
3. Add first Data Layer tool.
4. Add more valuation skills.

---

## Purpose

The purpose of Sovereign Valuer Assistant is to help valuation professionals with:

- searching and reasoning over local professional documents;
- reviewing valuation reports;
- checking consistency of assumptions, dates, sources, and calculations;
- working with valuation standards and methodological materials;
- drafting valuation-related text fragments;
- using structured valuation data from trusted APIs and local databases;
- maintaining explicit, approved professional memory;
- reducing unnecessary LLM token usage by relying on direct data tools where possible.

The assistant is intended to support professional judgement, not replace it.

---

## Core Idea

The project combines five layers:

```text
LLM Layer
    GigaChat or another explicitly configured model

Knowledge Layer
    local standards, methods, templates, books, and anonymized examples

Skills Layer
    Markdown/YAML-based domain workflows and prompt packages

Memory Layer
    explicit, inspectable, user-approved memory

Data Layer
    verified structured data from APIs and local databases
```

The key design principle is:

```text
Do not make the LLM search, guess, or remember everything.
Give it controlled access to verified knowledge, approved memory, and structured data tools.
```

---

## Why Local-First?

The project is intended for professionals who need:

- control over their working environment;
- transparent data handling;
- local or private deployment;
- reduced dependency on foreign cloud infrastructure;
- inspectable prompts, memory, skills, and data sources;
- reproducible professional workflows.

Target deployment options:

- local personal computer;
- private VPS;
- small private server.

---

## Initial Scope

The first version should be intentionally simple.

The initial assistant should be able to:

- start locally;
- connect to GigaChat;
- load configuration from environment variables;
- read approved memory files;
- load skills from Markdown or YAML files;
- search over local knowledge documents;
- answer with source awareness;
- avoid uncontrolled self-learning;
- keep LLM integration isolated.

---

## Non-Goals for the First Version

The first version should **not** try to implement:

- a fully autonomous self-improving agent;
- uncontrolled permanent memory;
- automatic modification of its own prompts;
- a complex multi-agent framework;
- enterprise-grade infrastructure;
- cloud-only deployment;
- hidden or non-inspectable behaviour;
- storage of confidential valuation reports in the public repository.

Frameworks such as Hermes, OpenClaw, LangGraph, GigaChain, LiteLLM, Qdrant, PostgreSQL, or Langfuse may be considered later if they solve a concrete problem.

The initial implementation should remain simple.

---

## Planned Repository Structure

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

---

## Main Components

### 1. LLM Layer

The default LLM provider is **GigaChat**.

LLM-provider-specific logic should be isolated in one module, for example:

```text
app/llm.py
```

The rest of the application should not depend directly on provider-specific implementation details.

---

### 2. Knowledge Layer

The Knowledge Layer stores professional materials such as:

- valuation standards;
- methodological documents;
- templates;
- books;
- anonymized report examples;
- legal and regulatory materials;
- checklists.

Initial folder:

```text
knowledge_base/
```

The Knowledge Layer is intended for RAG-style search and source-grounded answers.

---

### 3. Skills Layer

Skills are explicit valuation workflows or reusable prompt packages.

Initial folder:

```text
skills/
```

Possible skills:

- valuation report review;
- valuation standards compliance check;
- market analysis support;
- comparable selection support;
- calculation consistency check;
- court or expert opinion drafting;
- discount rate support;
- structured data source verification.

Skills should be human-readable and inspectable.

Preferred initial formats:

```text
Markdown
YAML
```

---

### 4. Memory Layer

The Memory Layer stores approved long-term memory.

Initial folder:

```text
memory/
```

Possible initial files:

```text
memory/user_profile.md
memory/approved_rules.md
memory/rejected_patterns.md
memory/project_notes.md
```

Memory must be:

- explicit;
- inspectable;
- editable;
- approved by the user;
- separated from raw chat logs;
- separated from retrieved document content.

The project must not implement uncontrolled self-learning.

---

### 5. Data Layer

The Data Layer provides structured valuation data from trusted APIs and local databases.

Initial folder:

```text
data_hub/
```

Possible data sources and tools:

- OFZ yield curve;
- key rate;
- inflation;
- exchange rates;
- market data;
- comparable transactions;
- financial ratios;
- industry multiples;
- cadastral or geographic data;
- data from other valuation-related projects.

Data tools should return metadata, not only raw numbers.

Example response shape:

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

---

## Roadmap

### v0.1 — Local Assistant Skeleton

Goal: create a minimal local assistant skeleton.

Planned scope:

- repository structure;
- configuration loading;
- isolated LLM wrapper;
- basic CLI entry point;
- skill loading;
- approved memory loading;
- first example skill;
- minimal tests.

---

### v0.2 — Local RAG

Goal: answer questions using local documents.

Planned scope:

- document ingestion from `knowledge_base/`;
- support for `.md` and `.txt`;
- chunking;
- simple retrieval;
- source references;
- RAG prompt template.

---

### v0.3 — Approved Memory Workflow

Goal: make memory controlled and inspectable.

Planned scope:

- read approved memory;
- propose candidate memory;
- save only after explicit user approval;
- support simple remember/forget workflow.

---

### v0.4 — First Data Layer Tool

Goal: add one structured valuation data tool.

Candidate first tool:

```text
get_risk_free_rate(date, maturity_years)
```

Planned scope:

- connector to an API or local mock database;
- metadata-rich response;
- freshness check;
- valuation-friendly explanation.

---

### v0.5 — First Practical Valuation Workflow

Goal: implement one useful professional workflow.

Candidate workflows:

- valuation report review;
- valuation standards compliance check;
- discount rate support;
- market analysis support;
- calculation consistency check.

---

## Development Model

The project follows this working model:

```text
Human user = product owner, valuation domain expert, and strategic decision-maker.
ChatGPT = project lead, architect, supervisor, and reviewer.
Cursor = implementation executor for small coding tasks.
```

Cursor and other coding agents must follow:

```text
AGENTS.md
```

Before making changes, coding agents should read:

```text
AGENTS.md
PROJECT_CONTEXT.md
README.md
```

---

## Rules for Coding Agents

Important rules are documented in `AGENTS.md`.

Core rules:

- do not redesign the architecture without explicit instruction;
- do not introduce unnecessary frameworks;
- do not replace GigaChat as the default LLM;
- do not implement uncontrolled self-learning;
- do not commit secrets;
- do not commit confidential valuation data;
- keep changes small and reviewable;
- prefer simple Python modules first.

---

## Security and Privacy

Do not commit:

- API keys;
- tokens;
- credentials;
- confidential valuation reports;
- client data;
- personal data;
- private databases;
- non-public case materials.

Use:

```text
.env.example
.gitignore
synthetic examples
anonymized samples
```

---

## Installation

Installation instructions will be added when the first runnable version is implemented.

Expected future local setup:

```bash
git clone <repository-url>
cd sovereign-valuer-assistant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

On Windows PowerShell, activation will likely be:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Configuration

Configuration will be loaded from environment variables.

### LLM smoke test

1. Copy `.env.example` to `.env`.
2. Set `GIGACHAT_CREDENTIALS` in `.env`.
3. Run:

```bash
python -m app.main --smoke-llm
```

Do not commit `.env`.

### Run a skill

Example:

```bash
python -m app.main --run-skill report_review --input-file examples/sample_report_fragment.md
```

This requires `GIGACHAT_CREDENTIALS` in `.env`.
Use only synthetic or anonymized input examples.

### Run a skill with local RAG

Example:

```bash
python -m app.main --run-skill report_review --input-file examples/sample_report_fragment.md --use-rag
```

Current RAG is simple deterministic keyword retrieval over local `.md`/`.txt` files.
Vector search and embeddings are intentionally postponed.

A future `.env.example` may include:

```env
GIGACHAT_CREDENTIALS=
GIGACHAT_SCOPE=
GIGACHAT_MODEL=GigaChat
GIGACHAT_VERIFY_SSL=false
GIGACHAT_VERIFY_SSL_CERTS=false
SVA_ENV=local
```

Do not commit real `.env` files.

---

## License

This project is licensed under the Apache License 2.0.
See [LICENSE](LICENSE).

---

## Disclaimer

This project is a professional assistant tool.

It does not provide legal, valuation, financial, or expert conclusions by itself.

All outputs must be reviewed and approved by a qualified professional before use in valuation reports, expert opinions, court submissions, or client-facing documents.

---

## Current Next Steps

Recommended immediate next steps:

The initial repository skeleton has already been created.

1. Add first local RAG workflow.
2. Add approved memory proposal workflow.
3. Add first Data Layer tool.
4. Add more valuation skills.
