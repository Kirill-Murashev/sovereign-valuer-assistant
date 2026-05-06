from types import SimpleNamespace

import pytest

from app.llm import LLMClient, LLMConfigurationError


def test_llm_client_missing_credentials_raises():
    with pytest.raises(LLMConfigurationError):
        LLMClient(provider="gigachat", credentials="")


def test_llm_client_unsupported_provider_raises():
    with pytest.raises(LLMConfigurationError):
        LLMClient(provider="openai", credentials="token")


def test_generate_returns_mocked_assistant_content(monkeypatch):
    class FakeGigaChat:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return None

        def chat(self, messages):
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(content="SVA LLM smoke test passed.")
                    )
                ]
            )

    monkeypatch.setattr("app.llm.GigaChat", FakeGigaChat)

    client = LLMClient(
        provider="gigachat",
        credentials="fake-token",
        scope="GIGACHAT_API_PERS",
        model="GigaChat",
        verify_ssl_certs=False,
    )

    result = client.generate(
        system_prompt="You are a concise assistant.",
        user_prompt="Reply with one short sentence: SVA LLM smoke test passed.",
    )
    assert result == "SVA LLM smoke test passed."

