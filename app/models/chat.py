from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """
    Modelo de entrada do chat.
    Representa a mensagem enviada pelo usuário.
    """
    message: str = Field(..., description="Mensagem enviada pelo usuário")


class ChatResponse(BaseModel):
    """
    Modelo de resposta do chat.
    Representa o texto gerado pelo LLM como resposta.
    """
    response: str = Field(..., description="Resposta gerada pelo modelo LLM")
