from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List
from sqlmodel import Session
from .auth import get_current_user, get_user_id_from_header
from .chat_controller import ChatRequest, ChatResponse, process_chat_request
from ..database.database import get_sync_session
from ..models.conversation_model import Conversation, Message
from ..services.conversation_service import ConversationService
from pydantic import BaseModel


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    messages: List[dict]


class UserConversationsResponse(BaseModel):
    conversations: List[Conversation]


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


@router.get("/chat/history/{conversation_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    conversation_id: str,
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Get the history of messages for a specific conversation
    """
    # Verify user owns this conversation
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )

    # Get conversation history
    messages = ConversationService.get_conversation_history(session, conversation_id, limit=100)

    # Format messages for response
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
        })

    return ConversationHistoryResponse(
        conversation_id=conversation_id,
        messages=formatted_messages
    )


@router.get("/chat/conversations", response_model=UserConversationsResponse)
async def get_user_conversations(
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Get all conversations for the current user
    """
    conversations = ConversationService.get_user_conversations(session, user_id)
    return UserConversationsResponse(conversations=conversations)


@router.get("/chat/latest", response_model=ConversationHistoryResponse)
async def get_latest_conversation(
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Get the most recent conversation for the user, creating one if it doesn't exist
    """
    # Get user's conversations
    user_conversations = ConversationService.get_user_conversations(session, user_id)

    if user_conversations:
        # Get the most recent conversation
        latest_conversation = user_conversations[0]  # Assuming they're ordered by creation date
        conversation_id = latest_conversation.conversation_id
    else:
        # Create a new conversation if none exist
        new_conversation = ConversationService.get_or_create_conversation(session, user_id)
        conversation_id = new_conversation.conversation_id

    # Get conversation history
    messages = ConversationService.get_conversation_history(session, conversation_id, limit=100)

    # Format messages for response
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
        })

    return ConversationHistoryResponse(
        conversation_id=conversation_id,
        messages=formatted_messages
    )