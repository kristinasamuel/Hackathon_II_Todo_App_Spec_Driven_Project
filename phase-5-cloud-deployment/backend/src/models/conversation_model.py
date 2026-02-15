from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class ConversationBase(SQLModel):
    """
    Base model for Conversation with shared attributes
    """
    user_id: str = Field(foreign_key="user.id")


class Conversation(ConversationBase, table=True):
    """
    Conversation model for the database
    """
    conversation_id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    metadata_json: Optional[str] = Field(default=None)  # JSON string for additional context


class ConversationCreate(SQLModel):
    """
    Model for creating a new conversation
    """
    user_id: str


class ConversationRead(ConversationBase):
    """
    Model for reading conversation data
    """
    conversation_id: str
    created_at: datetime
    updated_at: datetime
    metadata_json: Optional[str]


class MessageBase(SQLModel):
    """
    Base model for Message with shared attributes
    """
    conversation_id: str = Field(foreign_key="conversation.conversation_id")
    role: str = Field(max_length=20)  # 'user', 'assistant', 'system'
    content: str


class Message(MessageBase, table=True):
    """
    Message model for the database
    """
    message_id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls_json: Optional[str] = Field(default=None)  # JSON string for tool calls
    tool_responses_json: Optional[str] = Field(default=None)  # JSON string for tool responses


class MessageCreate(SQLModel):
    """
    Model for creating a new message
    """
    conversation_id: str
    role: str
    content: str
    tool_calls_json: Optional[str] = None
    tool_responses_json: Optional[str] = None


class MessageRead(MessageBase):
    """
    Model for reading message data
    """
    message_id: str
    timestamp: datetime
    tool_calls_json: Optional[str]
    tool_responses_json: Optional[str]