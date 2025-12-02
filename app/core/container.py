from typing import Dict, Type

from app.core.config import settings
from app.services.llm_client import BaseLLMClient
from app.services.gemini_client import GeminiClient
from app.services.factory import LLMFactory
from app.services.chat_service import ChatService


class Container:
    """
    Container simples de injeção de dependências, responsável por instanciar
    o LLM e o ChatService.
    """

    def __init__(self):
        self._registry: Dict[str, Type[BaseLLMClient]] = {}
        self._llm_client_instance: BaseLLMClient | None = None
        self._chat_service_instance: ChatService | None = None

    def register(self, name: str, client_cls: Type[BaseLLMClient]):
        """Registra uma classe de cliente LLM identificada por nome."""
        self._registry[name] = client_cls

    def resolve_llm_client(self) -> BaseLLMClient:
        """
        Retorna a instância do LLM configurado (singleton).
        """
        if self._llm_client_instance:
            return self._llm_client_instance

        provider = settings.LLM_PROVIDER.lower()

        if provider not in self._registry:
            raise ValueError(
                f"LLM provider '{provider}' não registrado no container. "
                f"Provedores disponíveis: {list(self._registry.keys())}"
            )

        self._llm_client_instance = LLMFactory.create(provider)

        return self._llm_client_instance

    @property
    def chat_service(self) -> ChatService:
        """
        Cria e retorna o ChatService já com LLM injetado.
        """
        if self._chat_service_instance:
            return self._chat_service_instance

        llm_client = self.resolve_llm_client()
        self._chat_service_instance = ChatService(llm_client)
        return self._chat_service_instance


# Instância global do container
_container = Container()

# Registrar provedores LLM disponíveis
_container.register("gemini", GeminiClient)


def get_container() -> Container:
    """Retorna o container (singleton)."""
    return _container
