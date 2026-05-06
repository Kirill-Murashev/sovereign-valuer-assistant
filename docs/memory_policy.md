# Memory policy (current draft)

## Principles

Memory is **file-based**, **explicit**, and **user-controlled**. The assistant does not
silently promote chat or RAG text into long-term memory.

## Current behaviour

- **Read-only loading:** The application loads markdown files from `memory/` for prompting.
  Approved section files are not modified automatically by the assistant.
- **Proposals (v0.3 draft, proposal stage only):** Candidate memory may be recorded as
  Markdown files under `memory/proposals/` using
  `python -m app.main --propose-memory "..."` (optional `--memory-target-section`).
  This creates a **proposed** file only; merging into approved memory remains a separate,
  deliberate manual step (no merge/approval automation yet).
- **Approval required:** Permanent memory changes require explicit maintainer approval;
  proposals are not approved memory until merged manually.
- **No uncontrolled self-learning:** The system must not learn autonomously from
  conversations or retrieved documents without human oversight.

## RAG vs memory

- **Retrieved RAG context** is **source material** for the current request. It is **not**
  permanent memory and must not be conflated with approved rules or profile content.

## Privacy

Sensitive real-world client data must not be stored in the public repository. Use
local-only paths and `.gitignore` patterns for private materials.
