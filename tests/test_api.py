import pytest
#AsyncMock para simular métodos assíncronos corretamente
from unittest.mock import patch, MagicMock, AsyncMock 
from fastapi.testclient import TestClient

from app.services.deps import get_chat_service 
from app.main import app

client = TestClient(app)

# Caminho para o objeto que será injetado/mockado no Depends

def test_chat_endpoint_success():
    """
    Testa se o endpoint POST /chat/ retorna 200 e a resposta formatada
    após simular a chamada ao ChatService.
    """
    expected_response_text = "Olá! Eu sou o assistente virtual."
    user_message = "Me diga quem você é."

    # 1. Simula o ChatService
    mock_chat_service = MagicMock()
    
    # 2. O método 'get_response' DEVE ser um AsyncMock, pois ele é 'awaitado' no endpoint.
    mock_chat_service.get_response = AsyncMock(return_value=expected_response_text)

    #  Configurando a Sobrescrita de Dependência (Override) ---
    def override_get_chat_service():
        """Função que o FastAPI usará no lugar da dependência real."""
        return mock_chat_service

    # Injeta a função de override no dicionário de sobrescritas do FastAPI
    app.dependency_overrides[get_chat_service] = override_get_chat_service

    try:
        # Act: Simula a requisição POST
        response = client.post(
            "/chat/",
            json={"message": user_message}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Verifica a estrutura de resposta e o texto
        assert data["response"] == expected_response_text
        
        # Verifica se o ChatService simulado foi chamado
        mock_chat_service.get_response.assert_called_once_with(user_message)

    finally:
        # Garante que a sobrescrita é removida após o teste, 
        # para não afetar outros testes.
        app.dependency_overrides.clear()


def test_chat_endpoint_invalid_input():
    """
    Testa se o endpoint retorna 422 (Unprocessable Entity) para JSON inválido.
    """
    response = client.post(
        "/chat/",
        json={"prompt": "Isso vai falhar"}
    )
    
    assert response.status_code == 422