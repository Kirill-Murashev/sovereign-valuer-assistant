"""LLM provider interface module.

Provider-specific integration should stay isolated in this file.
"""

from __future__ import annotations


class LLMClient:
    """Placeholder interface for future GigaChat integration."""

    def __init__(self, provider: str = "gigachat") -> None:
        self.provider = provider

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate text from an LLM provider.

        Real API integration is intentionally not implemented at v0.1 skeleton stage.
        """
        raise NotImplementedError(
            f"LLM provider '{self.provider}' is not implemented yet. "
            "Add GigaChat integration in app/llm.py."
        )

