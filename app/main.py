"""CLI entry point for Sovereign Valuer Assistant v0.1 skeleton."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from app.config import get_settings
from app.memory import load_memory
from app.skills import load_skills


def main() -> None:
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
    table.add_row("LLM Calls", "disabled in this skeleton")

    console.print(table)
    console.print("CLI skeleton is ready. LLM integration will be added in app/llm.py.")


if __name__ == "__main__":
    main()

