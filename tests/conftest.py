"""Configurações e fixtures para testes."""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_settings():
    """Fornece uma instância mock de Settings para testes que usam app.main."""
    mock = MagicMock()
    mock.CORS_ORIGINS = ["*"]
    mock.ENV = "local"
    mock.GEMINI_API_KEY = "test-key"
    mock.LLM_PROVIDER = "gemini"
    mock.MODEL_NAME = "models/gemini-1.5-flash-001"
    return mock
