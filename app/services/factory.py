from app.core.config import settings
from app.services.gemini_client import GeminiClient

class LLMFactory:
    @staticmethod
    def create(provider: str | None = None):
        """
        Cria o cliente LLM baseado no provedor solicitado.
        Se nenhum provedor for informado, usa o do settings.
        """
        provider = provider or settings.LLM_PROVIDER
        provider = provider.lower()

        if provider == "gemini":
            return GeminiClient(
                api_key=settings.GEMINI_API_KEY,
                model=settings.MODEL_NAME,
            )

        raise ValueError(f"LLM provider '{provider}' não suportado.")
