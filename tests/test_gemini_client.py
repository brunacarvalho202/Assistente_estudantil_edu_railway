import pytest
from unittest.mock import patch, MagicMock
from app.services.gemini_client import GeminiClient

# Caminho para o módulo genai que será mockado
MOCK_GENAI_PATH = 'app.services.gemini_client.genai'

@pytest.fixture
def dummy_gemini_client():
    """Cria uma instância do GeminiClient com configurações dummy."""
    return GeminiClient(api_key="dummy-key", model="dummy-model")


def test_gemini_client_initialization_configures_api_key(dummy_gemini_client):
    """Verifica se a chave da API é configurada na inicialização."""
    # Como o genai.configure é chamado no __init__, precisamos simular a classe toda.
    with patch(MOCK_GENAI_PATH) as mock_genai:
        GeminiClient(api_key="TEST-API-KEY", model="dummy-model")
        mock_genai.configure.assert_called_once_with(api_key="TEST-API-KEY")


def test_generate_returns_response_text(dummy_gemini_client):
    """
    Testa se a função generate chama o modelo e retorna o texto da resposta.
    """
    expected_response_text = "Resposta simulada do LLM"
    test_prompt = "Qual a capital da França?"

    # 1. Simula o objeto de resposta do Google
    mock_response = MagicMock()
    mock_response.text = expected_response_text

    # 2. Simula o método generate_content do modelo
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response
    
    # 3. Substitui o modelo real pela simulação para o teste
    dummy_gemini_client.model = mock_model

    # Act
    response = dummy_gemini_client.generate(test_prompt)

    # Assert
    mock_model.generate_content.assert_called_once_with(test_prompt)
    assert response == expected_response_text


def test_generate_returns_empty_string_on_no_response_text(dummy_gemini_client):
    """
    Testa se a função retorna uma string vazia se o campo 'text' for None (erro do modelo).
    """
    # 1. Simula uma resposta onde o campo 'text' é None
    mock_response = MagicMock()
    mock_response.text = None 

    # 2. Substitui o modelo real pela simulação
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response
    dummy_gemini_client.model = mock_model

    # Act
    response = dummy_gemini_client.generate("Prompt Vazio")

    # Assert
    assert response == ""