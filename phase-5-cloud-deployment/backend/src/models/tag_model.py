from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

# Many-to-many relationship table between Task and Tag
class TaskTagLink(SQLModel, table=True):
    task_id: Optional[str] = Field(default=None, foreign_key="task.id", primary_key=True)
    tag_id: Optional[str] = Field(default=None, foreign_key="tag.id", primary_key=True)

class TagBase(SQLModel):
    name: str = Field(index=True, unique=False) # Tag names should be unique per user, not globally unique
                                                # For now, allow duplicates, uniqueness check will be in service layer
                                                # or a composite unique constraint (user_id, name)
                                                # Changed to unique=False temporarily, as globally unique might be too strict

class Tag(TagBase, table=True):
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id") # Link tag to a user

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id: str
    user_id: str

class TagUpdate(SQLModel):
    name: Optional[str] = None
