"""Skill loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


REQUIRED_SKILL_FIELDS = {
    "name",
    "description",
    "system_prompt",
    "user_prompt_template",
}


class SkillValidationError(ValueError):
    """Raised when a skill file is malformed."""


def _validate_skill(payload: dict[str, Any], source_path: Path) -> dict[str, Any]:
    missing = REQUIRED_SKILL_FIELDS - payload.keys()
    if missing:
        missing_fields = ", ".join(sorted(missing))
        raise SkillValidationError(
            f"Skill file '{source_path}' is missing required fields: {missing_fields}"
        )

    required_tools = payload.get("required_tools")
    if required_tools is not None and not isinstance(required_tools, list):
        raise SkillValidationError(
            f"Skill file '{source_path}' has invalid 'required_tools': expected a list"
        )

    return payload


def load_skills(skills_dir: str | Path) -> list[dict[str, Any]]:
    """Load and validate YAML skills from a directory."""
    skills_path = Path(skills_dir)
    if not skills_path.exists():
        raise FileNotFoundError(f"Skills directory does not exist: {skills_path}")
    if not skills_path.is_dir():
        raise NotADirectoryError(f"Skills path is not a directory: {skills_path}")

    loaded: list[dict[str, Any]] = []
    for file_path in sorted(skills_path.glob("*.yaml")):
        try:
            raw = yaml.safe_load(file_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise SkillValidationError(f"Invalid YAML in '{file_path}': {exc}") from exc

        if not isinstance(raw, dict):
            raise SkillValidationError(
                f"Skill file '{file_path}' must contain a YAML object at top level"
            )

        loaded.append(_validate_skill(raw, file_path))

    return loaded


def get_skill_by_name(skills: list[dict], name: str) -> dict:
    """Return a loaded skill by name."""
    for skill in skills:
        if skill.get("name") == name:
            return skill
    raise ValueError(f"Skill '{name}' was not found in loaded skills.")

