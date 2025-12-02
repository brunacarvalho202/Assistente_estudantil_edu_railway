from typing import Annotated
from fastapi import Depends

from app.core.container import get_container
from app.services.chat_service import ChatService


def get_chat_service() -> ChatService:
    """
    Resolve a instância do ChatService via container.
    """
    container = get_container()
    llm_client = container.resolve_llm_client()
    return ChatService(llm_client=llm_client)


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
