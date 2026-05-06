from pathlib import Path

import pytest

from app.memory import (
    MEMORY_FILES,
    create_memory_proposal,
    format_memory_for_prompt,
    load_memory,
)


def _write_four_memory_files(base: Path) -> None:
    (base / "user_profile.md").write_text("profile", encoding="utf-8")
    (base / "approved_rules.md").write_text("rules", encoding="utf-8")
    (base / "rejected_patterns.md").write_text("rejected", encoding="utf-8")
    (base / "project_notes.md").write_text("notes", encoding="utf-8")


def test_load_memory_success(tmp_path):
    _write_four_memory_files(tmp_path)

    data = load_memory(tmp_path)

    assert data["user_profile"] == "profile"
    assert data["approved_rules"] == "rules"
    assert data["rejected_patterns"] == "rejected"
    assert data["project_notes"] == "notes"


def test_load_memory_missing_file(tmp_path):
    (tmp_path / "user_profile.md").write_text("profile", encoding="utf-8")
    (tmp_path / "approved_rules.md").write_text("rules", encoding="utf-8")
    (tmp_path / "rejected_patterns.md").write_text("rejected", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        load_memory(tmp_path)


def test_create_memory_proposal_creates_proposals_directory(tmp_path):
    _write_four_memory_files(tmp_path)
    path = create_memory_proposal(
        tmp_path, "Candidate line one.", target_section="project_notes"
    )
    assert path.parent.name == "proposals"
    assert path.is_file()


def test_create_memory_proposal_contains_candidate_and_target(tmp_path):
    _write_four_memory_files(tmp_path)
    path = create_memory_proposal(
        tmp_path,
        "Always distinguish evidence from assumptions.",
        target_section="approved_rules",
    )
    text = path.read_text(encoding="utf-8")
    assert "Always distinguish evidence from assumptions." in text
    assert "approved_rules" in text
    assert "**Target section:** approved_rules" in text
    assert "**Status:** proposed" in text


def test_create_memory_proposal_rejects_empty_text(tmp_path):
    _write_four_memory_files(tmp_path)
    with pytest.raises(ValueError, match="empty"):
        create_memory_proposal(tmp_path, "   ", target_section="project_notes")


def test_create_memory_proposal_rejects_invalid_section(tmp_path):
    _write_four_memory_files(tmp_path)
    with pytest.raises(ValueError, match="Unknown target_section"):
        create_memory_proposal(tmp_path, "text", target_section="not_a_section")


def test_create_memory_proposal_does_not_modify_approved_files(tmp_path):
    before: dict[str, bytes] = {}
    _write_four_memory_files(tmp_path)
    for key, fname in MEMORY_FILES.items():
        before[fname] = (tmp_path / fname).read_bytes()

    create_memory_proposal(
        tmp_path,
        "New proposed rule text.",
        target_section="approved_rules",
    )

    for fname, content in before.items():
        assert (tmp_path / fname).read_bytes() == content


def test_format_memory_for_prompt():
    memory = {
        "approved_rules": "Rule A",
        "project_notes": "Note B",
    }
    rendered = format_memory_for_prompt(memory)
    assert "## Approved Rules" in rendered
    assert "Rule A" in rendered
    assert "## Project Notes" in rendered
    assert "Note B" in rendered
