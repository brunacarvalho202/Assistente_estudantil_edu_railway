"""Testes simples de configuração - apenas validam o fluxo básico."""

import pytest
from unittest.mock import patch, MagicMock
from app.core.config import Settings


def test_settings_loads_defaults():
    """Testa se Settings carrega os valores padrão."""
    settings = Settings()
    assert settings.APP_NAME == "Edu Assistente"
    assert settings.ENV == "local"
    assert settings.LLM_PROVIDER == "gemini"
    assert settings.CORS_ORIGINS == ["*"]


def test_settings_accepts_custom_values():
    """Testa se Settings aceita valores customizados."""
    settings = Settings(
        ENV="production",
        LLM_PROVIDER="openai",
        GEMINI_API_KEY="test-key-123"
    )
    assert settings.ENV == "production"
    assert settings.LLM_PROVIDER == "openai"
    assert settings.GEMINI_API_KEY == "test-key-123"


def test_settings_from_environment():
    """Testa se Settings lê valores de variáveis de ambiente."""
    with patch.dict("os.environ", {
        "ENV": "staging",
        "LLM_PROVIDER": "anthropic",
        "GEMINI_API_KEY": "env-key"
    }):
        settings = Settings()
        assert settings.ENV == "staging"
        assert settings.LLM_PROVIDER == "anthropic"
        assert settings.GEMINI_API_KEY == "env-key"


def test_settings_gemini_api_key_optional():
    """Testa se GEMINI_API_KEY é opcional."""
    settings = Settings(ENV="local")
    assert settings.GEMINI_API_KEY is None or isinstance(settings.GEMINI_API_KEY, str)

