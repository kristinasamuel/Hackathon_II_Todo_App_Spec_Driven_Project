from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
import uuid

from ..database.database import get_sync_session
from ..models.user_model import User # Assuming User model is needed for user_id
from ..models.tag_model import Tag, TagCreate, TagRead, TagUpdate # Import Tag models
from .auth import get_user_id_from_header # CORRECTED: Import get_user_id_from_header from .auth

router = APIRouter() # No prefix here, will be added in main.py

@router.post("/tags", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_create: TagCreate,
    session: Session = Depends(get_sync_session),
    current_user_id: str = Depends(get_user_id_from_header) # CORRECTED: Use current_user_id
):
    """
    Create a new tag for the current user.
    """
    # Check for existing tag name for this user
    existing_tag = session.exec(
        select(Tag).where(Tag.user_id == current_user_id, Tag.name == tag_create.name)
    ).first()

    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag with this name already exists for the user."
        )

    db_tag = Tag(name=tag_create.name, user_id=current_user_id) # CORRECTED: Use current_user_id directly
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@router.get("/tags", response_model=List[TagRead])
def read_tags(
    session: Session = Depends(get_sync_session),
    current_user_id: str = Depends(get_user_id_from_header) # CORRECTED: Use current_user_id
):
    """
    Retrieve all tags for the current user.
    """
    tags = session.exec(
        select(Tag).where(Tag.user_id == current_user_id) # CORRECTED: Use current_user_id
    ).all()
    return tags

@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: str,
    session: Session = Depends(get_sync_session),
    current_user_id: str = Depends(get_user_id_from_header) # CORRECTED: Use current_user_id
):
    """
    Delete a tag by ID.
    """
    tag = session.exec(
        select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user_id) # CORRECTED: Use current_user_id
    ).first()

    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found or not owned by user.")

    session.delete(tag)
    session.commit()
    return