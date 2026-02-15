from sqlmodel import SQLModel, Field, Relationship # Import Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from enum import Enum # Import Enum

from .tag_model import Tag, TaskTagLink, TagRead # Import Tag and TaskTagLink and TagRead

def generate_uuid():
    return str(uuid.uuid4())

# Define the Priority Enum
class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(SQLModel):
    """
    Base model for Task with shared attributes
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    # Add priority and due_date
    priority: Priority = Field(default=Priority.medium) # Default to medium
    due_date: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """
    Task model for the database
    """
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Add relationship to Tag
    tags: List[Tag] = Relationship(back_populates="tasks", link_model=TaskTagLink)


class TaskCreate(SQLModel):
    """
    Model for creating a new task
    """
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[Priority] = Priority.medium # Allow setting priority on creation
    due_date: Optional[datetime] = None # Allow setting due_date on creation
    tag_ids: List[str] = [] # Allow associating tags by ID


class TaskRead(TaskBase):
    """
    Model for reading task data
    """
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead] = [] # Include tags when reading


class TaskUpdate(SQLModel):
    """
    Model for updating a task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None # Allow updating priority
    due_date: Optional[datetime] = None # Allow updating due_date
    tag_ids: Optional[List[str]] = None # Allow updating associated tags by ID


class TaskUpdateCompletion(SQLModel):
    """
    Model for updating task completion status
    """
    completed: bool