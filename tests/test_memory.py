import pytest

from app.memory import load_memory


def test_load_memory_success(tmp_path):
    (tmp_path / "user_profile.md").write_text("profile", encoding="utf-8")
    (tmp_path / "approved_rules.md").write_text("rules", encoding="utf-8")
    (tmp_path / "rejected_patterns.md").write_text("rejected", encoding="utf-8")
    (tmp_path / "project_notes.md").write_text("notes", encoding="utf-8")

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
