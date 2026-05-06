"""LLM provider integration module.

Provider-specific integration should stay isolated in this file.
"""

from __future__ import annotations

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole


class LLMConfigurationError(ValueError):
    """Raised when LLM client configuration is invalid."""


class LLMClient:
    """Minimal LLM client abstraction with GigaChat support."""

    def __init__(
        self,
        provider: str = "gigachat",
        credentials: str = "",
        scope: str = "GIGACHAT_API_PERS",
        model: str = "GigaChat",
        verify_ssl_certs: bool = False,
    ) -> None:
        if provider != "gigachat":
            raise LLMConfigurationError(
                f"Unsupported provider '{provider}'. Only 'gigachat' is supported."
            )
        if not credentials.strip():
            raise LLMConfigurationError(
                "Missing GigaChat credentials. Set GIGACHAT_CREDENTIALS in your environment."
            )
        self.provider = provider
        self.credentials = credentials
        self.scope = scope
        self.model = model
        self.verify_ssl_certs = verify_ssl_certs

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate assistant text from GigaChat."""
        chat = Chat(
            messages=[
                Messages(role=MessagesRole.SYSTEM, content=system_prompt),
                Messages(role=MessagesRole.USER, content=user_prompt),
            ]
        )

        with GigaChat(
            credentials=self.credentials,
            scope=self.scope,
            model=self.model,
            verify_ssl_certs=self.verify_ssl_certs,
        ) as client:
            response = client.chat(chat)

        content = response.choices[0].message.content
        if not isinstance(content, str):
            raise RuntimeError("GigaChat response content is not a string.")
        return content

