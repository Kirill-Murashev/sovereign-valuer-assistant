"""CLI entry point for Sovereign Valuer Assistant v0.1 skeleton."""

from __future__ import annotations

import argparse

from rich.console import Console
from rich.table import Table

from app.config import get_settings
from app.llm import LLMClient, LLMConfigurationError
from app.memory import load_memory
from app.skills import load_skills


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--smoke-llm",
        action="store_true",
        help="Run a minimal LLM smoke test with configured provider.",
    )
    args = parser.parse_args()

    console = Console()
    settings = get_settings()

    memory = load_memory(settings.memory_dir)
    skills = load_skills(settings.skills_dir)

    table = Table(title="Sovereign Valuer Assistant v0.1 Status")
    table.add_column("Component")
    table.add_column("Status")
    table.add_row("Environment", settings.sva_env)
    table.add_row("LLM Provider", settings.sva_llm_provider)
    table.add_row("Skills Loaded", str(len(skills)))
    table.add_row("Memory Sections Loaded", str(len(memory)))
    table.add_row("Knowledge Base Dir", settings.knowledge_base_dir)
    table.add_row("Data Hub Dir", settings.data_hub_dir)
    table.add_row("LLM Calls", "enabled only with --smoke-llm")

    console.print(table)
    if not args.smoke_llm:
        console.print("CLI is ready. Use --smoke-llm to test GigaChat integration.")
        return

    try:
        llm_client = LLMClient(
            provider=settings.sva_llm_provider,
            credentials=settings.gigachat_credentials,
            scope=settings.gigachat_scope or "GIGACHAT_API_PERS",
            model=settings.gigachat_model,
            verify_ssl_certs=settings.gigachat_verify_ssl_certs,
        )
    except LLMConfigurationError as exc:
        console.print(f"[red]LLM configuration error:[/red] {exc}")
        return

    try:
        response = llm_client.generate(
            system_prompt="You are a concise assistant.",
            user_prompt="Reply with one short sentence: SVA LLM smoke test passed.",
        )
    except Exception as exc:  # pragma: no cover - runtime/API failure path
        console.print(f"[red]LLM smoke test failed:[/red] {exc}")
        return

    console.print("[green]LLM smoke test response:[/green]")
    console.print(response)


if __name__ == "__main__":
    main()

