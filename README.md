# Sovereign Valuer Assistant

**Codename:** Elessar  
**Short name:** SVA  
**Repository:** `sovereign-valuer-assistant`

Sovereign Valuer Assistant is an open-source, local-first LLM assistant for valuation professionals.

The project is designed as a practical pet project for building a controlled digital
assistant that can work with valuation standards, professional knowledge bases,
report templates, structured valuation data, and approved long-term memory.

The default target LLM is **GigaChat**.

Architecture stays **simple and local-first**: inspectable modules, explicit configuration, no heavy agent frameworks in the current codebase.

---

## Project status

### Release milestones

Implemented on `main`:

Current implemented status is **v0.3.1 draft**.

| Milestone | Description |
|-----------|-------------|
| **v0.1** | Repository skeleton (structure, configuration, skill and memory loading, tests, CI, documentation). |
| **v0.1.1** | GigaChat smoke path (`--smoke-llm`). |
| **v0.1.2** | `report_review` skill runner (`--run-skill`). |
| **v0.2 (draft)** | Local deterministic RAG for skill runs (`--use-rag`) over `.md`/`.txt` in `knowledge_base/`. |
| **v0.2.1** | Transparent retrieved-source output in the CLI: concise sources are printed when `--use-rag` is enabled; full retrieved context is printed only with `--show-rag-context`. |
| **v0.3 (draft)** | Minimal approved memory proposal workflow: `--propose-memory TEXT` with optional `--memory-target-section` writes proposal Markdown files under `memory/proposals/` and does not modify approved memory files automatically. |
| **v0.3.1 (draft)** | Proposal review helpers are implemented: `--list-memory-proposals` lists proposal files and `--show-memory-proposal PATH` prints a selected proposal, while proposals remain under `memory/proposals/` and no automatic approval/merge is performed. |

Additional hygiene and tooling:

- GitHub Actions test workflow  
- Apache License 2.0 (`LICENSE`)  
- Contribution guidelines (`CONTRIBUTING.md`)  
- Deterministic unit tests  

Approved memory remains controlled: section files in `memory/` are still loaded read-only by default, and proposal creation does not merge or auto-write approved memory.

Planned next steps:

| Milestone | Description |
|-----------|-------------|
| **v0.3.2** *(next)* | Explicit manual approval design for proposals (still no automatic uncontrolled memory writes). |
| **v0.4** *(later)* | First Data Layer tool (structured valuation data with metadata-rich responses). |

Further improvements after that include more valuation skills and incremental improvements to deterministic local RAG while keeping behaviour inspectable.

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

## Core idea

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

## Why local-first?

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

## Initial scope

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

## Non-goals for the first version

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

## Planned repository structure

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

## Main components

### 1. LLM layer

The default LLM provider is **GigaChat**.

LLM-provider-specific logic should be isolated in one module, for example:

```text
app/llm.py
```

The rest of the application should not depend directly on provider-specific implementation details.

---

### 2. Knowledge layer

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

### 3. Skills layer

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

### 4. Memory layer

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

### 5. Data layer

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

## Roadmap (high level)

### Completed (current branch)

- **v0.1** — Local assistant skeleton (structure, config, CLI, skills, read-only memory, tests).
- **v0.1.1** — GigaChat smoke path.
- **v0.1.2** — `report_review` skill runner.
- **v0.2 (draft)** — Local deterministic RAG for `--run-skill` (`--use-rag`).
- **v0.2.1** — Transparent RAG source output in the CLI.

### Planned

- **v0.3.2** — Explicit manual approval design for proposals (still no automatic uncontrolled memory writes).
- **v0.4** — First Data Layer tool (candidate: `get_risk_free_rate(date, maturity_years)`).
- **v0.5** — Broader practical valuation workflows (report review depth, standards checks, market analysis support, and similar).

---

## Development model

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

## Rules for coding agents

Important rules are documented in `AGENTS.md`.

Core rules:

- do not redesign the architecture without explicit instruction;
- do not introduce unnecessary frameworks;
- do not replace GigaChat as the default LLM;
- do not add OpenAI/Anthropic fallback paths as implicit defaults;
- do not implement silent provider fallback if GigaChat is unavailable;
- do not introduce LangChain, LangGraph, GigaChain, LiteLLM, Hermes, OpenClaw, CrewAI, or AutoGen in current scope;
- do not introduce embeddings, vector databases, or BM25 in current scope;
- do not implement uncontrolled self-learning;
- do not commit secrets;
- do not commit confidential valuation data;
- keep changes small and reviewable;
- prefer simple Python modules first.

---

## Security and privacy

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

Local setup:

```bash
git clone https://github.com/Kirill-Murashev/sovereign-valuer-assistant.git
cd sovereign-valuer-assistant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install dependencies and run `python -m app.main` as above.

---

## Configuration

Configuration is loaded from environment variables (see `.env.example`).

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

Optional (show full retrieved context):

```bash
python -m app.main --run-skill report_review --input-file examples/sample_report_fragment.md --use-rag --show-rag-context
```

Retrieved sources are shown before the LLM response to support verification.  
Current RAG is simple deterministic keyword retrieval over local `.md`/`.txt` files.  
Vector search and embeddings are intentionally postponed.

`.env.example` may include:

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
