import pytest

from app.skills import SkillValidationError, get_skill_by_name, load_skills


def test_load_skills_success(tmp_path):
    skill_file = tmp_path / "report_review.yaml"
    skill_file.write_text(
        """
name: report_review
description: Review valuation report.
system_prompt: You are a reviewer.
user_prompt_template: "Review: {report_text}"
required_tools:
  - rag_search
""".strip(),
        encoding="utf-8",
    )

    skills = load_skills(tmp_path)

    assert len(skills) == 1
    assert skills[0]["name"] == "report_review"


def test_load_skills_missing_required_field(tmp_path):
    invalid_file = tmp_path / "invalid.yaml"
    invalid_file.write_text(
        """
name: broken_skill
description: Missing prompts.
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(SkillValidationError):
        load_skills(tmp_path)


def test_get_skill_by_name_success():
    skills = [
        {"name": "report_review", "system_prompt": "a", "user_prompt_template": "b"},
        {"name": "other_skill", "system_prompt": "a", "user_prompt_template": "b"},
    ]
    selected = get_skill_by_name(skills, "report_review")
    assert selected["name"] == "report_review"


def test_get_skill_by_name_not_found():
    with pytest.raises(ValueError):
        get_skill_by_name([], "missing")
