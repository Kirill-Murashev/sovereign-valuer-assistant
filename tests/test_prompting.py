import pytest

from app.prompting import build_skill_prompt


def test_build_skill_prompt_with_report_text_placeholder():
    skill = {
        "system_prompt": "System base",
        "user_prompt_template": "Review this:\n{report_text}",
    }
    system_prompt, user_prompt = build_skill_prompt(
        skill=skill, memory_text="Memory block", user_input="Input text"
    )
    assert "System base" in system_prompt
    assert "Approved memory context" in system_prompt
    assert "Memory block" in system_prompt
    assert "Input text" in user_prompt


def test_build_skill_prompt_with_user_input_placeholder():
    skill = {
        "system_prompt": "System base",
        "user_prompt_template": "User says: {user_input}",
    }
    _, user_prompt = build_skill_prompt(skill=skill, memory_text="M", user_input="Hello")
    assert user_prompt == "User says: Hello"


def test_build_skill_prompt_with_retrieved_context():
    skill = {
        "system_prompt": "System base",
        "user_prompt_template": "User says: {user_input}",
    }
    system_prompt, _ = build_skill_prompt(
        skill=skill,
        memory_text="Memory block",
        user_input="Hello",
        retrieved_context="Source: x.md | Chunk: 0\nContext text",
    )
    assert "Retrieved knowledge context" in system_prompt
    assert "not approved memory" in system_prompt
    assert "Source: x.md | Chunk: 0" in system_prompt


def test_build_skill_prompt_unsupported_placeholder():
    skill = {
        "system_prompt": "System base",
        "user_prompt_template": "Bad placeholder {unknown}",
    }
    with pytest.raises(ValueError):
        build_skill_prompt(skill=skill, memory_text="M", user_input="Hello")
