from fastapi import APIRouter, Depends

from app.services.deps import get_chat_service
from app.services.chat_service import ChatService
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    """
    Endpoint de chat.
    - Recebe uma mensagem do usuário.
    - Envia para o ChatService (que usa o LLM configurado no container).
    - Retorna a resposta gerada pelo modelo.

    """
    response_text = await chat_service.get_response(request.message)
    return ChatResponse(response=response_text)
