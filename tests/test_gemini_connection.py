import pytest
import os
from app.core.config import settings
from app.services.factory import LLMFactory

# O teste só deve rodar em ambientes onde GEMINI_API_KEY está configurada
@pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"),
    reason="Este teste requer que GEMINI_API_KEY esteja configurada como variável de ambiente."
)
def test_gemini_connection():
    """
    Testa se a conexão com o Gemini é possível usando a chave API.
    """
    # Arrange
    if not settings.GEMINI_API_KEY:
        pytest.skip("GEMINI_API_KEY não configurada")
    
    llm = LLMFactory.create(provider="gemini")

    # Act
    # Usamos uma consulta simples e barata
    response = llm.generate("Olá, isso é um teste de conexão. Responda apenas: OK.")

    # Assert
    assert "OK" in response.upper()
    print("\nTeste de conexão Gemini: Funcionou!")