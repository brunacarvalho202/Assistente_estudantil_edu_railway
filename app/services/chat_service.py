from app.services.llm_client import BaseLLMClient

class ChatService:
    """
    Camada de negócio do chat.
    Isola toda a lógica antes de chamar o LLM.
    """

    def __init__(self, llm_client: BaseLLMClient):
        self.llm = llm_client

    async def get_response(self, user_message: str) -> str:
        """
        Processa o prompt do usuário e delega ao LLM.
        """
        prompt = f"""
        Você é EDU, um assistente estudantil especializado em ciência da computação.
        Seu papel é atuar como um professor paciente, didático e altamente claro.

        REGRAS DE RESPOSTA:
        - Explique os conceitos de forma simples, objetiva e estruturada.
        - Use exemplos curtos e diretamente aplicáveis ao tema.
        - Evite jargões desnecessários.
        - Se houver ambiguidade na pergunta, faça a interpretação mais útil possível.
        - Sempre entregue uma resposta que ajude o usuário a aprender o conceito.
        Usuário disse: "{user_message}"
        Responda de forma clara e direta, sendo didático e instrutitivo
        """

        return self.llm.generate(prompt)
