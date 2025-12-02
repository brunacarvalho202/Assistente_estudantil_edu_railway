import pytest
from unittest.mock import patch, MagicMock
from app.services.factory import LLMFactory

# Nome do caminho para o objeto que queremos simular (mockar)
# Aqui, simulamos a classe GeminiClient dentro de app.services.factory
MOCK_GEMINI_CLIENT_PATH = 'app.services.factory.GeminiClient' 
MOCK_SETTINGS_PATH = 'app.services.factory.settings'

def test_factory_creates_gemini_client_with_gemini_provider():
    """
    Testa se a factory retorna uma instância de GeminiClient 
    quando o provedor 'gemini' é solicitado.
    """
    # 1. Simula as configurações (settings) para ter API_KEY e MODEL_NAME
    mock_settings = MagicMock()
    mock_settings.LLM_PROVIDER = "gemini"
    mock_settings.GEMINI_API_KEY = "dummy-api-key"
    mock_settings.MODEL_NAME = "test-model"

    # 2. Simula a classe GeminiClient para que a factory a crie
    with patch(MOCK_GEMINI_CLIENT_PATH) as MockGeminiClient:
        with patch(MOCK_SETTINGS_PATH, mock_settings):
            
            # Act
            client = LLMFactory.create(provider="gemini")
            
            # Assert 
            # Verifica se o construtor do GeminiClient foi chamado
            MockGeminiClient.assert_called_once_with(
                api_key="dummy-api-key",
                model="test-model"
            )

def test_factory_raises_error_for_unsupported_provider():
    """
    Testa se a factory levanta um ValueError para provedores não suportados.
    """
    with pytest.raises(ValueError, match="LLM provider 'openai' não suportado."):
        LLMFactory.create(provider="openai")