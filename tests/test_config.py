from app.config import get_settings


def test_get_settings_from_env(monkeypatch):
    get_settings.cache_clear()
    monkeypatch.setenv("SVA_ENV", "test")
    monkeypatch.setenv("SVA_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("SVA_LLM_PROVIDER", "gigachat")
    monkeypatch.setenv("GIGACHAT_VERIFY_SSL", "false")
    monkeypatch.setenv("SVA_KNOWLEDGE_BASE_DIR", "knowledge_base_custom")
    monkeypatch.setenv("SVA_SKILLS_DIR", "skills_custom")
    monkeypatch.setenv("SVA_MEMORY_DIR", "memory_custom")
    monkeypatch.setenv("SVA_DATA_HUB_DIR", "data_hub_custom")
    monkeypatch.setenv("SVA_CHUNK_SIZE", "600")
    monkeypatch.setenv("SVA_CHUNK_OVERLAP", "120")
    monkeypatch.setenv("SVA_TOP_K", "3")
    monkeypatch.setenv("SVA_ALLOW_MEMORY_WRITE", "true")
    monkeypatch.setenv("SVA_ALLOW_NETWORK_TOOLS", "true")

    settings = get_settings()

    assert settings.sva_env == "test"
    assert settings.sva_log_level == "DEBUG"
    assert settings.sva_llm_provider == "gigachat"
    assert settings.gigachat_verify_ssl is False
    assert settings.knowledge_base_dir == "knowledge_base_custom"
    assert settings.skills_dir == "skills_custom"
    assert settings.memory_dir == "memory_custom"
    assert settings.data_hub_dir == "data_hub_custom"
    assert settings.chunk_size == 600
    assert settings.chunk_overlap == 120
    assert settings.top_k == 3
    assert settings.allow_memory_write is True
    assert settings.allow_network_tools is True
