"""CLI entry point for Sovereign Valuer Assistant v0.3.1 draft."""

from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from app.config import get_settings
from app.llm import LLMClient, LLMConfigurationError
from app.memory import (
    PROPOSAL_TARGET_SECTIONS,
    create_memory_proposal,
    format_memory_for_prompt,
    list_memory_proposals,
    load_memory,
    read_memory_proposal,
)
from app.prompting import build_skill_prompt
from app.rag import (
    chunk_documents,
    format_retrieved_context,
    format_retrieved_sources,
    load_documents,
    retrieve,
)
from app.skills import get_skill_by_name, load_skills


APP_VERSION = "v0.3.1 draft"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--smoke-llm",
        action="store_true",
        help="Run a minimal LLM smoke test with configured provider.",
    )
    parser.add_argument("--run-skill", type=str, help="Run a loaded skill by name.")
    parser.add_argument("--input-file", type=str, help="Path to UTF-8 input file.")
    parser.add_argument(
        "--use-rag",
        action="store_true",
        help="Include simple local RAG context from knowledge_base.",
    )
    parser.add_argument(
        "--show-rag-context",
        action="store_true",
        help="Print full retrieved RAG context when used with --use-rag.",
    )
    parser.add_argument(
        "--propose-memory",
        type=str,
        default=None,
        metavar="TEXT",
        help="Write a proposal file under memory/proposals/ (does not modify approved memory).",
    )
    parser.add_argument(
        "--memory-target-section",
        type=str,
        default="project_notes",
        choices=sorted(PROPOSAL_TARGET_SECTIONS),
        help="Approved-memory section name for --propose-memory.",
    )
    parser.add_argument(
        "--list-memory-proposals",
        action="store_true",
        help="List proposal files from memory/proposals/.",
    )
    parser.add_argument(
        "--show-memory-proposal",
        type=str,
        default=None,
        metavar="PATH",
        help="Show one proposal file from memory/proposals/.",
    )
    args = parser.parse_args()

    console = Console()
    settings = get_settings()

    if args.propose_memory is not None:
        try:
            proposal_path = create_memory_proposal(
                settings.memory_dir,
                args.propose_memory,
                target_section=args.memory_target_section,
            )
        except ValueError as exc:
            console.print(f"[red]Proposal error:[/red] {exc}")
            return
        console.print(f"[green]Memory proposal written:[/green] {proposal_path}")
        return

    if args.list_memory_proposals:
        proposals = list_memory_proposals(settings.memory_dir)
        if not proposals:
            console.print("No memory proposals found in memory/proposals/.")
            return
        console.print("[cyan]Memory proposals:[/cyan]")
        for proposal in proposals:
            console.print(f"- {proposal}")
        return

    if args.show_memory_proposal is not None:
        try:
            proposal_text = read_memory_proposal(
                settings.memory_dir, args.show_memory_proposal
            )
        except ValueError as exc:
            console.print(f"[red]Proposal error:[/red] {exc}")
            return
        except FileNotFoundError as exc:
            console.print(f"[red]Proposal error:[/red] {exc}")
            return
        console.print(proposal_text)
        return

    memory = load_memory(settings.memory_dir)
    skills = load_skills(settings.skills_dir)

    table = Table(title=f"Sovereign Valuer Assistant {APP_VERSION} Status")
    table.add_column("Component")
    table.add_column("Status")
    table.add_row("Environment", settings.sva_env)
    table.add_row("LLM Provider", settings.sva_llm_provider)
    table.add_row("Skills Loaded", str(len(skills)))
    table.add_row("Memory Sections Loaded", str(len(memory)))
    table.add_row("Knowledge Base Dir", settings.knowledge_base_dir)
    table.add_row("Data Hub Dir", settings.data_hub_dir)
    table.add_row("LLM Calls", "enabled with --smoke-llm or --run-skill")

    console.print(table)
    if not args.smoke_llm and not args.run_skill:
        console.print(
            "CLI is ready. Use --smoke-llm, --run-skill, --propose-memory, "
            "--list-memory-proposals, or --show-memory-proposal as needed."
        )
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

    if args.run_skill:
        if args.show_rag_context and not args.use_rag:
            console.print(
                "[yellow]RAG warning:[/yellow] --show-rag-context has no effect without --use-rag."
            )
        if not args.input_file:
            console.print("[red]Input error:[/red] --input-file is required with --run-skill.")
            return
        input_path = Path(args.input_file)
        if not input_path.exists():
            console.print(f"[red]Input error:[/red] Input file not found: {input_path}")
            return
        try:
            user_input = input_path.read_text(encoding="utf-8")
        except Exception as exc:
            console.print(f"[red]Input error:[/red] Failed to read input file: {exc}")
            return

        try:
            selected_skill = get_skill_by_name(skills, args.run_skill)
            memory_text = format_memory_for_prompt(memory)
            retrieved_context = ""
            retrieved_chunks: list[dict[str, str | int]] = []
            if args.use_rag:
                documents = load_documents(settings.knowledge_base_dir)
                chunks = chunk_documents(
                    documents,
                    chunk_size=settings.chunk_size,
                    chunk_overlap=settings.chunk_overlap,
                )
                retrieved_chunks = retrieve(user_input, chunks, top_k=settings.top_k)
                if not retrieved_chunks:
                    console.print(
                        "[yellow]RAG warning:[/yellow] No retrieved context found in knowledge base."
                    )
                else:
                    retrieved_context = format_retrieved_context(retrieved_chunks)
                    console.print("[cyan]Retrieved sources:[/cyan]")
                    console.print(format_retrieved_sources(retrieved_chunks))
                    if args.show_rag_context:
                        console.print("[cyan]Retrieved context:[/cyan]")
                        console.print(retrieved_context)
            system_prompt, user_prompt = build_skill_prompt(
                selected_skill,
                memory_text,
                user_input,
                retrieved_context=retrieved_context,
            )
            result = llm_client.generate(system_prompt=system_prompt, user_prompt=user_prompt)
        except ValueError as exc:
            console.print(f"[red]Skill error:[/red] {exc}")
            return
        except Exception as exc:  # pragma: no cover - runtime/API failure path
            console.print(f"[red]Skill run failed:[/red] {exc}")
            return

        console.print(f"[green]Skill '{args.run_skill}' response:[/green]")
        console.print(result)
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
