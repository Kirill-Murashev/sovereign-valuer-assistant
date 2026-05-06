# Skill format (current draft)

Skills are stored as YAML files under `skills/`. They should remain human-readable and versionable.

## Required fields

| Field | Purpose |
|-------|---------|
| `name` | Stable identifier for the skill. |
| `description` | Short human-readable summary. |
| `system_prompt` | Instructions and role for the model. |
| `user_prompt_template` | Template for the user turn; may include placeholders (see below). |

## Optional fields

| Field | Purpose |
|-------|---------|
| `required_tools` | List of tool names the skill expects (for future Data Layer or other integrations). |

## Validation

`app/skills.py` validates required fields and raises clear exceptions for invalid files.

## First implemented skill

- `skills/report_review.yaml` — valuation report review workflow.

## Template variables

In `user_prompt_template`, the following placeholders are supported:

- `{report_text}` — filled with the input text for report-style skills (same value as the user input).
- `{user_input}` — generic placeholder for the user-provided input text.
