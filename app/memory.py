"""Memory file loading for approved local memory."""

from __future__ import annotations

from pathlib import Path


MEMORY_FILES = {
    "user_profile": "user_profile.md",
    "approved_rules": "approved_rules.md",
    "rejected_patterns": "rejected_patterns.md",
    "project_notes": "project_notes.md",
}


def load_memory(memory_dir: str | Path) -> dict[str, str]:
    """Load required memory markdown sections from disk."""
    base_path = Path(memory_dir)
    if not base_path.exists():
        raise FileNotFoundError(f"Memory directory does not exist: {base_path}")
    if not base_path.is_dir():
        raise NotADirectoryError(f"Memory path is not a directory: {base_path}")

    data: dict[str, str] = {}
    for section_name, filename in MEMORY_FILES.items():
        file_path = base_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Required memory file is missing: {file_path}")
        data[section_name] = file_path.read_text(encoding="utf-8")

    return data


def format_memory_for_prompt(memory: dict[str, str]) -> str:
    """Format loaded memory sections as readable prompt context."""
    parts: list[str] = []
    for section_name, content in memory.items():
        title = section_name.replace("_", " ").title()
        parts.append(f"## {title}\n{content.strip()}")
    return "\n\n".join(parts).strip()

