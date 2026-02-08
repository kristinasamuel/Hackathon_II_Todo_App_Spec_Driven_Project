from sqlmodel import Session
from typing import List, Optional
from ..models.conversation_model import Conversation, Message, ConversationCreate, MessageCreate
from ..services.conversation_repository import ConversationRepository


class ConversationService:
    @staticmethod
    def get_or_create_conversation(session: Session, user_id: str, conversation_id: Optional[str] = None) -> Conversation:
        if conversation_id:
            # Try to get existing conversation
            conversation = ConversationRepository.get_conversation_by_id(session, conversation_id)
            if conversation:
                return conversation

        # Create new conversation
        conversation_data = ConversationCreate(user_id=user_id)
        return ConversationRepository.create_conversation(session, conversation_data)

    @staticmethod
    def add_message_to_conversation(session: Session, conversation_id: str, role: str, content: str,
                                   tool_calls_json: Optional[str] = None,
                                   tool_responses_json: Optional[str] = None) -> Message:
        message_data = MessageCreate(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls_json=tool_calls_json,
            tool_responses_json=tool_responses_json
        )
        return ConversationRepository.create_message(session, message_data)

    @staticmethod
    def get_conversation_history(session: Session, conversation_id: str, limit: int = 50) -> List[Message]:
        return ConversationRepository.get_messages_chronological(session, conversation_id, limit)

    @staticmethod
    def get_user_conversations(session: Session, user_id: str) -> List[Conversation]:
        return ConversationRepository.get_conversations_by_user_id(session, user_id)

    @staticmethod
    def save_chat_interaction(session: Session, user_id: str, user_message: str, ai_response: str,
                             conversation_id: Optional[str] = None) -> tuple[Conversation, Message, Message]:
        # Get or create conversation
        conversation = ConversationService.get_or_create_conversation(session, user_id, conversation_id)

        # Add user message
        user_msg = ConversationService.add_message_to_conversation(
            session,
            conversation.conversation_id,
            "user",
            user_message
        )

        # Add AI response message
        ai_msg = ConversationService.add_message_to_conversation(
            session,
            conversation.conversation_id,
            "assistant",
            ai_response
        )

        return conversation, user_msg, ai_msg