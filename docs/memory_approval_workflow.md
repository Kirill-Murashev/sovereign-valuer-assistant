# Manual memory approval workflow (v0.3.2 design)

This document defines a **controlled manual** process for turning memory **proposals** into **approved** memory. It is **design and policy only**: it does not implement approval, merge, or any automatic writes.

For general memory policy, see [memory_policy.md](memory_policy.md).

---

## 1. Purpose

The memory proposal path exists to:

- prevent **uncontrolled self-learning** (nothing is silently promoted from chat or RAG into long-term memory);
- prevent **accidental writes** into approved section files (`memory/*.md`);
- keep every durable memory change **explicit, inspectable, and human-approved**.

Proposals are staging files only. **Approved memory** lives in the four section files under `memory/` and is loaded read-only by the application today.

---

## 2. Current implemented state (v0.3 / v0.3.1)

The following CLI behaviour exists today:

| Action | Command | Notes |
|--------|---------|--------|
| Create proposal | `--propose-memory TEXT` | Writes a UTF-8 Markdown file under `memory/proposals/`. |
| Choose target section | `--memory-target-section` | One of: `user_profile`, `approved_rules`, `rejected_patterns`, `project_notes`. |
| List proposals | `--list-memory-proposals` | Lists `*.md` under `memory/proposals/`, or reports none. |
| Show one proposal | `--show-memory-proposal PATH` | Prints file content; path must resolve **inside** `memory/proposals/` (traversal outside is rejected). |

**Approved memory files are not modified automatically** by any of these commands. There is **no** `--approve-memory-proposal` or merge automation in the current codebase.

---

## 3. Approved memory sections

`--memory-target-section` must be one of:

| Section | File | Intended use |
|---------|------|----------------|
| `user_profile` | `memory/user_profile.md` | Stable preferences and context about how *you* want the assistant to behave (tone, jurisdiction notes, non-confidential defaults). |
| `approved_rules` | `memory/approved_rules.md` | Rules the assistant should follow consistently (methodology, citation habits, review checklist items). |
| `rejected_patterns` | `memory/rejected_patterns.md` | Patterns to avoid (bad phrasing, disallowed shortcuts, known failure modes). |
| `project_notes` | `memory/project_notes.md` | Project-specific, non-secret working notes (conventions, glossary, repo-specific reminders). |

Do not store **client-identifying** or **confidential** material in any section if the repository or backup could leave your trusted environment.

---

## 4. Manual review workflow (recommended)

1. **Create a proposal** with `--propose-memory` and `--memory-target-section`.
2. **List proposals** with `--list-memory-proposals`.
3. **Inspect** the candidate with `--show-memory-proposal PATH`.
4. **Review** the candidate text for:
   - correctness;
   - confidentiality (no client secrets, no report extracts, no credentials);
   - relevance and long-term value;
   - fit for the selected target section.
5. **If accepted:** open the corresponding approved file (e.g. `memory/approved_rules.md`) in your editor and **manually** add or edit text. Keep edits small and reviewable.
6. **If rejected:** **delete** the proposal file, or **move** it to a private archive outside the repo (no standard archive path is required yet).
7. **Commit** approved memory changes **explicitly** in git when you want that state shared (never commit real client data).

Until optional future CLI helpers exist, “merge” means **your edit** to the approved markdown file, not an automated tool.

---

## 5. Acceptance criteria for a memory proposal

A proposal may be merged manually into approved memory **only if** all of the following hold:

- It is **factually correct** (or clearly framed as a preference/rule, not a false fact).
- It is **useful** for repeatable future behaviour (not one-off noise).
- It contains **no confidential client data**, no undisclosable excerpts, and no real case identifiers.
- It contains **no secrets**: API keys, passwords, tokens, personal data, or private report content.
- It is **aligned** with valuation professional standards and with this project’s architecture (local-first, no silent fallbacks, no uncontrolled learning).
- It **belongs** in the selected `target_section` (if unsure, prefer `project_notes` or split into multiple proposals).

---

## 6. Rejection criteria

Reject (do not merge) a proposal if:

- it is **temporary** (“today only”, chat scratch);
- it is **vague** or untestable;
- it **duplicates** existing approved text without adding clarity;
- it embeds **unverified assumptions** as facts;
- it contains **confidential** or **sensitive** data;
- it would cause the assistant to **overstate certainty** or present opinion as verified knowledge;
- it would cause **architecture drift** (e.g. pushing for cloud-only flows, alternate LLM defaults, or frameworks forbidden by project policy).

---

## 7. Guardrails

- **No automatic approval** of proposals.
- **No automatic merge** into `memory/user_profile.md`, `memory/approved_rules.md`, etc.
- **No uncontrolled self-learning** from conversations or retrieved documents.
- **No LLM-only decision** to persist memory: the model may suggest text; a **human maintainer** remains the final approver for durable memory.
- **Maintainer/user** is responsible for what enters approved files and for git history.

---

## 8. Future possible CLI commands (not implemented)

The following are **design candidates only**. They **do not exist** in the current CLI and must not be documented as shipped features:

- `--approve-memory-proposal PATH` — hypothetical helper to record an approval marker or move a file; would still require explicit policy and no silent merge unless deliberately designed.
- `--reject-memory-proposal PATH` — hypothetical helper to delete or mark rejected.
- `--archive-memory-proposal PATH` — hypothetical helper to move proposals to an archive directory.

Any future implementation must preserve: explicit human control, no silent writes, and small reviewable changes.

---

## 9. Recommended file lifecycle (conceptual)

These are **logical states** for thinking about proposals. There is **no** enforced state machine or metadata schema in the repo yet:

- **proposed** — file exists under `memory/proposals/` with proposal template content.
- **accepted manually** — you copied or adapted the text into the correct `memory/*.md` file; the proposal file may be deleted or archived by you.
- **rejected** — you decided not to merge; delete the proposal or move it out of the repo.
- **archived** — optional; e.g. moved to a private folder outside git.

Do not rely on filenames alone for state; use your own discipline until a future version adds optional markers or commands.

---

## 10. Example commands

Create a proposal:

```bash
python -m app.main --propose-memory "Always distinguish market evidence from valuation assumptions." --memory-target-section approved_rules
```

List proposals:

```bash
python -m app.main --list-memory-proposals
```

Show one proposal (replace with the path printed by `--propose-memory` or `--list-memory-proposals`):

```bash
python -m app.main --show-memory-proposal memory/proposals/proposal_YYYYMMDD_HHMMSS_xxxxxx.md
```

---

## 11. Relationship to the roadmap

- **v0.3** and **v0.3.1** delivered proposal **creation** and **read-only review helpers** in code.
- **v0.3.2** includes this **documentation/design** milestone: explicit manual approval steps and guardrails **before** any implementation of approval/merge CLI.
- **v0.4** remains **later**: first structured **Data Layer** tool.

This document **does not** implement writes to approved memory; it prepares maintainers and contributors for a future controlled workflow.
