from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlmodel import Session
from .auth import get_current_user, get_user_id_from_header
from .chat_controller import ChatRequest, ChatResponse, process_chat_request
from ..database.database import get_sync_session


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Chat endpoint that processes natural language input and returns AI-generated responses
    """
    # Since process_chat_request is synchronous, run it in a thread pool to avoid blocking
    import asyncio
    import concurrent.futures

    loop = asyncio.get_event_loop()

    def run_sync_process():
        return process_chat_request(user_id, request, session)

    # Run the synchronous function in a thread pool to avoid blocking the event loop
    response = await loop.run_in_executor(None, run_sync_process)
    return response