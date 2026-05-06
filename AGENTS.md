# AGENTS.md

## Purpose

This repository contains **Sovereign Valuer Assistant**.

Codename: **Elessar**.

Sovereign Valuer Assistant is an open-source, local-first pet project for building
a personal LLM assistant for valuation professionals. The assistant is intended to
support valuation work, report review, standards checking, calculation checking,
knowledge retrieval, structured data access, and controlled professional memory.

The project must remain simple, inspectable, reproducible, and suitable for deployment on a local PC or VPS.

## Roles

The human user is the **product owner**, **domain expert**, and **methodological decision-maker**.

ChatGPT acts as the **project lead**, **architect**, **supervisor**, and **reviewer**.

Cursor and other coding agents act only as **implementation executors**.

Coding agents must not make major architectural, methodological, or product decisions without explicit instruction.

## Core Architectural Decisions

These decisions are currently fixed unless the product owner explicitly changes them.

- Canonical project name: `Sovereign Valuer Assistant`.
- Repository name: `sovereign-valuer-assistant`.
- Internal short name: `SVA`.
- Codename: `Elessar`.
- Default LLM provider: `GigaChat`.
- Initial implementation language: `Python`.
- Initial deployment target: local PC or VPS.
- Initial interface: CLI or simple local UI.
- Knowledge base: local files in `knowledge_base/`.
- Skills: Markdown/YAML files in `skills/`.
- Memory: explicit, inspectable, editable, and approved by the user.
- Structured valuation data: handled through a separate Data Layer.
- Project type: small open-source pet project, not an enterprise platform.

## Development Principles

Prefer simple, readable code.

Prefer small modules over complex abstractions.

Prefer explicit configuration over hidden defaults.

Prefer local-first operation.

Prefer deterministic behaviour where possible.

Keep every change small and reviewable.

Do not introduce unnecessary frameworks.

Do not optimize prematurely.

Do not hide errors behind silent fallbacks.

Do not implement autonomous behaviour unless explicitly requested.

Do not implement uncontrolled self-learning.

Do not treat LLM output as verified knowledge unless it has been approved by the user or supported by a reliable source.

## Initial Repository Structure

Use the following initial structure unless explicitly instructed otherwise:

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
│   ├── standards/
│   ├── templates/
│   ├── reports_examples/
│   └── methods/
├── skills/
│   ├── report_review.yaml
│   ├── fso_check.yaml
│   ├── market_analysis.yaml
│   ├── calculation_check.yaml
│   └── court_opinion.yaml
├── memory/
│   ├── user_profile.md
│   ├── approved_rules.md
│   ├── rejected_patterns.md
│   └── project_notes.md
├── data_hub/
│   ├── connectors/
│   ├── services/
│   └── tools/
├── docs/
│   ├── architecture.md
│   ├── memory_policy.md
│   ├── skill_format.md
│   └── data_layer.md
├── examples/
├── tests/
├── PROJECT_CONTEXT.md
├── AGENTS.md
├── README.md
├── .env.example
├── .gitignore
└── requirements.txt
```

Do not create a more complex structure unless the task explicitly requires it.

## Coding Rules

Write clear Python code with explicit names.

Use type hints where they improve readability.

Keep functions short and focused.

Avoid large god modules.

Avoid global mutable state unless there is a specific reason.

Do not hard-code local absolute paths.

Do not hard-code API keys, tokens, credentials, or personal data.

Use environment variables and `.env.example` for configuration.

When adding dependencies, choose stable and widely used packages.

Do not add heavy dependencies unless explicitly requested.

Do not introduce large frameworks merely because they are popular.

## LLM Integration Rules

The default LLM provider is **GigaChat**.

Do not replace GigaChat with OpenAI, Anthropic, Google, local models, or other providers unless explicitly requested.

If an LLM abstraction layer is needed, keep it minimal and isolated in `app/llm.py`.

If LiteLLM is introduced, it must be used as an LLM gateway or compatibility layer, not as the core agent system.

Do not implement provider-specific logic across the whole codebase. Keep provider-specific details isolated.

Do not make live LLM calls in deterministic unit tests.

Do not silently fall back to another provider if GigaChat fails. Return a clear error.

## Orchestration Rules

Do not introduce LangChain, LangGraph, GigaChain, Hermes, OpenClaw, CrewAI, AutoGen, or similar orchestration frameworks unless the task explicitly asks for it.

The first version should remain simple.

If orchestration is required, propose a short plan first.

Any future workflow engine must preserve:

- source tracking;
- explicit memory writes;
- user approval for permanent memory;
- clear logs;
- testability;
- local-first deployment.

## Memory Rules

Do not implement uncontrolled self-learning.

Permanent memory must be:

- explicit;
- inspectable;
- editable;
- approved by the user;
- removable;
- separated from raw chat history;
- separated from retrieved knowledge;
- separated from structured data.

The first implementation should use plain files, for example:

```text
memory/user_profile.md
memory/approved_rules.md
memory/rejected_patterns.md
memory/project_notes.md
```

Do not automatically treat previous LLM outputs as verified memory.

Do not save confidential client data to permanent memory.

Do not save sensitive personal data unless the user explicitly requests it and the storage location is appropriate.

Memory writes must be deliberate and visible.

If the assistant proposes a memory entry, it should be represented as a proposed entry requiring user approval.

## RAG and Knowledge Base Rules

The knowledge base contains documents such as valuation standards, valuation methods, templates, books, anonymized example reports, and methodological materials.

The RAG system must preserve source references.

Do not invent citations.

If a source is missing, say that the source is missing.

Do not mix retrieved document content with permanent memory.

Do not store structured valuation datasets only as vector chunks if they require exact numeric retrieval.

Document ingestion should preserve useful metadata where possible:

- file name;
- document type;
- source;
- date, if available;
- section or page, if available;
- chunk id.

## Data Layer Rules

Structured valuation data must be handled through the Data Layer, not only through RAG.

Examples of structured valuation data:

- OFZ yield curve;
- key rate;
- inflation;
- currency exchange rates;
- market data;
- comparable transactions;
- financial ratios;
- company reporting data;
- cadastral or geographic data;
- macroeconomic indicators;
- industry multipliers.

Data tools must return metadata, not just raw values.

A good Data Layer response should include:

- value;
- unit;
- date;
- source;
- source URL or source identifier, if available;
- updated_at;
- method, if applicable;
- freshness or staleness flag;
- limitations, if applicable.

Do not let the LLM invent market data when a data tool is required.

If a data tool cannot provide the requested value, return a clear structured error.

Do not silently substitute outdated data.

## Skills Rules

Skills are professional task definitions stored as Markdown or YAML files.

Initial skill files should be simple and inspectable.

A YAML skill should normally contain:

```yaml
name: example_skill
description: Short description of the skill.
version: 0.1.0
inputs:
  - name: user_request
    required: true
instructions: |
  Clear instructions for the assistant.
output_format: |
  Expected output format.
```

Do not embed secrets or private data in skills.

Do not make skills self-modifying.

Do not make skills write to permanent memory without explicit user approval.

## Security and Privacy Rules

Do not commit:

- API keys;
- tokens;
- passwords;
- credentials;
- confidential valuation reports;
- client data;
- personal data;
- non-anonymized legal documents;
- local database dumps with real sensitive data;
- private logs.

Use `.gitignore` for:

- `.env`;
- local databases;
- vector indexes;
- logs;
- temporary files;
- uploaded documents;
- private knowledge bases.

Example reports must be anonymized or synthetic.

Do not add telemetry that sends user data to third parties unless explicitly requested.

## Testing Rules

Add deterministic tests for critical non-LLM functionality.

Important test targets:

- configuration loading;
- skill loading;
- skill validation;
- memory loading;
- memory writing proposal logic;
- document chunking;
- source metadata preservation;
- Data Layer tools;
- error handling.

Avoid tests that require live LLM calls unless explicitly requested.

Do not make tests depend on private local files.

Use small fixtures.

## Documentation Rules

Update documentation when behaviour changes.

Important documentation files:

- `README.md`;
- `PROJECT_CONTEXT.md`;
- `AGENTS.md`;
- `docs/architecture.md`;
- `docs/memory_policy.md`;
- `docs/skill_format.md`;
- `docs/data_layer.md`.

Documentation should be practical, concise, and implementation-oriented.

Do not write marketing-style documentation unless explicitly requested.

## Prohibited Changes

Do not:

- redesign the whole project without approval;
- introduce a full multi-agent framework without instruction;
- introduce Hermes or OpenClaw as the core system;
- replace GigaChat as the default LLM;
- add cloud-only dependencies;
- commit secrets;
- implement autonomous self-modifying behaviour;
- implement uncontrolled memory writes;
- store private user data in the public repository;
- remove source tracking from RAG;
- merge structured Data Layer into unstructured RAG without explicit instruction;
- hide failures behind silent fallbacks;
- add unnecessary abstractions;
- turn the pet project into an enterprise platform prematurely.

## Larger Changes

For larger changes, propose a short plan first.

The plan must include:

1. What problem is being solved.
2. Which files will change.
3. Which dependencies will be added.
4. Why the change is necessary.
5. What risks it introduces.
6. How to test it.

Do not implement large architectural changes without approval.

## Current First Milestone

The current first milestone is:

```text
v0.1: local valuation assistant that can answer questions using a local document folder and apply one skill: report review.
```

Minimum v0.1 scope:

- GigaChat connection;
- simple CLI chat;
- local `knowledge_base/` folder;
- simple RAG over local documents;
- `skills/report_review.yaml`;
- `memory/approved_rules.md`;
- basic README;
- one-command local launch.

Keep all work aligned with this milestone unless explicitly instructed otherwise.
