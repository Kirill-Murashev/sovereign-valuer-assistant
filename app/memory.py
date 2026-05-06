"""Memory file loading for approved local memory."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


MEMORY_FILES = {
    "user_profile": "user_profile.md",
    "approved_rules": "approved_rules.md",
    "rejected_patterns": "rejected_patterns.md",
    "project_notes": "project_notes.md",
}

PROPOSAL_TARGET_SECTIONS = frozenset(MEMORY_FILES.keys())


def create_memory_proposal(
    memory_dir: str | Path,
    candidate_text: str,
    target_section: str = "project_notes",
) -> Path:
    """Write a proposed memory entry under memory/proposals/ (does not edit approved files)."""
    if not candidate_text.strip():
        raise ValueError("candidate_text must not be empty.")
    if target_section not in PROPOSAL_TARGET_SECTIONS:
        allowed = ", ".join(sorted(PROPOSAL_TARGET_SECTIONS))
        raise ValueError(
            f"Unknown target_section '{target_section}'. Allowed: {allowed}"
        )

    base = Path(memory_dir)
    proposals_dir = base / "proposals"
    proposals_dir.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    out_path = proposals_dir / f"proposal_{stamp}.md"

    body = f"""# Memory proposal

**Status:** proposed
**Created at:** {created_at}
**Target section:** {target_section}

## Candidate memory

{candidate_text.strip()}

## Review checklist

- [ ] Fact-checked and aligned with professional standards
- [ ] No confidential client data or undisclosable material
- [ ] Explicit maintainer approval before merging into approved memory files
"""

    out_path.write_text(body, encoding="utf-8", newline="\n")
    return out_path


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

