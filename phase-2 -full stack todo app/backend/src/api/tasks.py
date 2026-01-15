from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from ..database.database import get_sync_session
from ..models.task_model import Task, TaskCreate, TaskRead, TaskUpdate, TaskUpdateCompletion
from ..models.user_model import User
from ..services.task_service import TaskService
from ..services.auth_service import AuthService
from .auth import get_current_user, get_user_id_from_header
from uuid import UUID

router = APIRouter()

@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Get all tasks for the specified user
    """
    # Validate that the user exists
    user_exists = AuthService.validate_user_exists(session, user_id)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    tasks = TaskService.get_tasks_by_user_id(session, user_id)
    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Create a new task for the specified user
    """
    # Validate that the user exists
    user_exists = AuthService.validate_user_exists(session, user_id)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Override the user_id in the task data with the authenticated user's ID
    # This prevents users from creating tasks for other users
    task_data_dict = task_data.model_dump()
    task_data_dict['user_id'] = user_id
    validated_task_data = TaskCreate(**task_data_dict)

    task = TaskService.create_task(session, validated_task_data)
    return task


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: str,
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Get a specific task by ID for the specified user
    """
    task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Update a specific task by ID for the specified user
    """
    updated_task = TaskService.update_task(session, task_id, user_id, task_update)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Delete a specific task by ID for the specified user
    """
    success = TaskService.delete_task(session, task_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def update_task_completion(
    task_id: str,
    completion_update: TaskUpdateCompletion,
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Update the completion status of a specific task by ID for the specified user
    """
    updated_task = TaskService.update_task_completion(session, task_id, user_id, completion_update)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return updated_task