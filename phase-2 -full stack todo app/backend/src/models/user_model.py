from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    """
    Base model for User with shared attributes
    """
    email: str = Field(unique=True, nullable=False)


class User(UserBase, table=True):
    """
    User model for the database
    """
    id: Optional[str] = Field(default=None, primary_key=True)  # Using string ID from Better Auth
    password: str = Field(nullable=False)  # Add password field
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})


class UserCreate(SQLModel):
    """
    Model for creating a new user
    """
    email: str
    password: str


class UserRead(UserBase):
    """
    Model for reading user data
    """
    id: str
    created_at: datetime
    updated_at: datetime