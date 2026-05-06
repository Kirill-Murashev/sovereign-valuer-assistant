"""Prompt construction helpers for skill execution."""

from __future__ import annotations


def build_skill_prompt(skill: dict, memory_text: str, user_input: str) -> tuple[str, str]:
    """Build system and user prompts for a skill run."""
    system_base = skill.get("system_prompt")
    template = skill.get("user_prompt_template")
    if not isinstance(system_base, str) or not isinstance(template, str):
        raise ValueError("Skill must contain string 'system_prompt' and 'user_prompt_template'.")

    system_prompt = (
        f"{system_base.strip()}\n\n"
        "Approved memory context:\n"
        f"{memory_text.strip()}"
    )

    normalized_template = template.replace("{report_text}", "{user_input}")
    try:
        user_prompt = normalized_template.format(user_input=user_input)
    except KeyError as exc:
        raise ValueError(
            f"Unsupported template variable in user_prompt_template: {exc.args[0]}"
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive formatting error path
        raise ValueError(f"Failed to build user prompt from template: {exc}") from exc

    return system_prompt, user_prompt

