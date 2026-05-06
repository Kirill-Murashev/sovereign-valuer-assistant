from app.config import get_settings


def test_get_settings_from_env(monkeypatch):
    get_settings.cache_clear()
    monkeypatch.setenv("SVA_ENV", "test")
    monkeypatch.setenv("SVA_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("SVA_LLM_PROVIDER", "gigachat")
    monkeypatch.setenv("GIGACHAT_VERIFY_SSL", "false")
    monkeypatch.setenv("CHUNK_SIZE", "600")
    monkeypatch.setenv("CHUNK_OVERLAP", "120")
    monkeypatch.setenv("TOP_K", "3")
    monkeypatch.setenv("ALLOW_MEMORY_WRITE", "true")

    settings = get_settings()

    assert settings.sva_env == "test"
    assert settings.sva_log_level == "DEBUG"
    assert settings.sva_llm_provider == "gigachat"
    assert settings.gigachat_verify_ssl is False
    assert settings.chunk_size == 600
    assert settings.chunk_overlap == 120
    assert settings.top_k == 3
    assert settings.allow_memory_write is True
