"""Application configuration loading."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_int(value: str | None, default: int) -> int:
    if value is None or value.strip() == "":
        return default
    return int(value)


class Settings(BaseModel):
    """Runtime settings loaded from environment variables."""

    sva_env: str = Field(default="local")
    sva_log_level: str = Field(default="INFO")
    sva_llm_provider: str = Field(default="gigachat")
    gigachat_credentials: str = Field(default="")
    gigachat_scope: str = Field(default="")
    gigachat_verify_ssl: bool = Field(default=True)
    knowledge_base_dir: str = Field(default="knowledge_base")
    skills_dir: str = Field(default="skills")
    memory_dir: str = Field(default="memory")
    data_hub_dir: str = Field(default="data_hub")
    chunk_size: int = Field(default=800, ge=50)
    chunk_overlap: int = Field(default=100, ge=0)
    top_k: int = Field(default=5, ge=1)
    allow_memory_write: bool = Field(default=False)
    allow_network_tools: bool = Field(default=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings from environment variables and cache the result."""
    load_dotenv()
    return Settings(
        sva_env=os.getenv("SVA_ENV", "local"),
        sva_log_level=os.getenv("SVA_LOG_LEVEL", "INFO"),
        sva_llm_provider=os.getenv("SVA_LLM_PROVIDER", "gigachat"),
        gigachat_credentials=os.getenv("GIGACHAT_CREDENTIALS", ""),
        gigachat_scope=os.getenv("GIGACHAT_SCOPE", ""),
        gigachat_verify_ssl=_as_bool(os.getenv("GIGACHAT_VERIFY_SSL"), True),
        knowledge_base_dir=os.getenv("KNOWLEDGE_BASE_DIR", "knowledge_base"),
        skills_dir=os.getenv("SKILLS_DIR", "skills"),
        memory_dir=os.getenv("MEMORY_DIR", "memory"),
        data_hub_dir=os.getenv("DATA_HUB_DIR", "data_hub"),
        chunk_size=_as_int(os.getenv("CHUNK_SIZE"), 800),
        chunk_overlap=_as_int(os.getenv("CHUNK_OVERLAP"), 100),
        top_k=_as_int(os.getenv("TOP_K"), 5),
        allow_memory_write=_as_bool(os.getenv("ALLOW_MEMORY_WRITE"), False),
        allow_network_tools=_as_bool(os.getenv("ALLOW_NETWORK_TOOLS"), False),
    )


def resolve_repo_path(path_value: str) -> Path:
    """Resolve a potentially relative path against the current working directory."""
    path = Path(path_value)
    return path if path.is_absolute() else Path.cwd() / path

