# Skill Format (v0.1 Draft)

Skills are stored as YAML files under `skills/`.

Required fields:
- `name`
- `description`
- `system_prompt`
- `user_prompt_template`

Optional fields:
- `required_tools` (list)

Validation is performed by `app/skills.py`. Invalid files raise clear exceptions.
