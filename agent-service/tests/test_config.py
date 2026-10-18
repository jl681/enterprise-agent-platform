import pytest
from pydantic import ValidationError

from app.config import Settings


@pytest.fixture(autouse=True)
def clear_deepseek_environment(monkeypatch):
    for name in (
        "DEEPSEEK_MODEL",
        "DEEPSEEK_API_KEY",
        "DEEPSEEK_BASE_URL",
    ):
        monkeypatch.delenv(name, raising=False)
        monkeypatch.delenv(name.lower(), raising=False)


def test_settings_reads_environment_variables(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_MODEL", "test-model")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-api-key")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://example.com/v1")

    settings = Settings(_env_file=None)

    assert settings.deepseek_model == "test-model"
    assert settings.deepseek_api_key.get_secret_value() == "test-api-key"
    assert settings.deepseek_base_url == "https://example.com/v1"


@pytest.mark.parametrize("api_key", [None, ""], ids=["missing", "empty"])
def test_settings_rejects_missing_or_empty_api_key(monkeypatch, api_key):
    if api_key is not None:
        monkeypatch.setenv("DEEPSEEK_API_KEY", api_key)

    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)

    assert any(
        error["loc"] == ("deepseek_api_key",)
        for error in exc_info.value.errors()
    )


def test_settings_uses_defaults_with_only_api_key(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-api-key")

    settings = Settings(_env_file=None)

    assert settings.deepseek_api_key.get_secret_value() == "test-api-key"
    assert settings.deepseek_model == "deepseek-flash"
    assert settings.deepseek_base_url == "https://api.deepseek.com"
