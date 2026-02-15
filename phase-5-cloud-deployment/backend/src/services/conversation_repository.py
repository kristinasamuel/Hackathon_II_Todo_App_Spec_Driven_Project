from sqlmodel import Session, select
from typing import List, Optional
from ..models.conversation_model import Conversation, Message, ConversationCreate, MessageCreate


class ConversationRepository:
    @staticmethod
    def create_conversation(session: Session, conversation_data: ConversationCreate) -> Conversation:
        conversation = Conversation.from_orm(conversation_data)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: str) -> Optional[Conversation]:
        statement = select(Conversation).where(Conversation.conversation_id == conversation_id)
        return session.exec(statement).first()

    @staticmethod
    def get_conversations_by_user_id(session: Session, user_id: str) -> List[Conversation]:
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def update_conversation(session: Session, conversation_id: str, metadata_json: str) -> Optional[Conversation]:
        conversation = ConversationRepository.get_conversation_by_id(session, conversation_id)
        if conversation:
            conversation.metadata_json = metadata_json
            conversation.updated_at = conversation.__class__.updated_at.default.arg()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    @staticmethod
    def create_message(session: Session, message_data: MessageCreate) -> Message:
        message = Message.from_orm(message_data)
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_messages_by_conversation_id(session: Session, conversation_id: str) -> List[Message]:
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc())
        return session.exec(statement).all()

    @staticmethod
    def get_latest_messages(session: Session, conversation_id: str, limit: int = 10) -> List[Message]:
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.desc()).limit(limit)
        messages = session.exec(statement).all()
        # Reverse to get chronological order
        return list(reversed(messages))

    @staticmethod
    def get_message_by_id(session: Session, message_id: str) -> Optional[Message]:
        statement = select(Message).where(Message.message_id == message_id)
        return session.exec(statement).first()