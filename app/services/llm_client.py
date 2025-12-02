from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    """
    Interface base para qualquer LLM que a aplicação suporte.
    Cada provedor (Gemini, OpenAI, Ollama...) implementará essa interface.
    """
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Gera um texto dado um prompt. Todos os provedores devem implementar isso.
        """
        pass
