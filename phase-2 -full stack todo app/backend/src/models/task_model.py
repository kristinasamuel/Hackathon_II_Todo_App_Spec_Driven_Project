from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class TaskBase(SQLModel):
    """
    Base model for Task with shared attributes
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    """
    Task model for the database
    """
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})


class TaskCreate(TaskBase):
    """
    Model for creating a new task
    """
    title: str
    user_id: str


class TaskRead(TaskBase):
    """
    Model for reading task data
    """
    id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """
    Model for updating a task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskUpdateCompletion(SQLModel):
    """
    Model for updating task completion status
    """
    completed: bool