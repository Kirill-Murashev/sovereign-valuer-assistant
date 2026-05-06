# Memory policy (current draft)

## Principles

Memory is **file-based**, **explicit**, and **user-controlled**. The assistant does not
silently promote chat or RAG text into long-term memory.

## Current behaviour

- **Read-only loading:** The application loads markdown files from `memory/` for prompting.
  It does not implement automatic writes in the current codebase.
- **Approval required:** Any future permanent memory change should follow an explicit
  user-approved workflow (planned as **v0.3**).
- **No uncontrolled self-learning:** The system must not learn autonomously from
  conversations or retrieved documents without human oversight.

## RAG vs memory

- **Retrieved RAG context** is **source material** for the current request. It is **not**
  permanent memory and must not be conflated with approved rules or profile content.

## Privacy

Sensitive real-world client data must not be stored in the public repository. Use
local-only paths and `.gitignore` patterns for private materials.
