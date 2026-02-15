from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session, select
from ..database.database import get_sync_session
from ..models.task_model import Task, TaskCreate, TaskRead, TaskUpdate, TaskUpdateCompletion, Priority
from ..models.user_model import User
from ..services.task_service import TaskService
from ..services.auth_service import AuthService
from .auth import get_current_user, get_user_id_from_header
from uuid import UUID

router = APIRouter()

@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session),
    search: Optional[str] = Query(None, description="Search tasks by title or description"),
    status: Optional[str] = Query(None, description="Filter tasks by completion status (completed, pending)"),
    priority: Optional[Priority] = Query(None, description="Filter tasks by priority (low, medium, high)"),
    tags: Optional[str] = Query(None, description="Filter tasks by comma-separated tag IDs"),
    sort_by: Optional[str] = Query(None, description="Sort tasks by field (due_date, priority, created_at)"),
    order: Optional[str] = Query(None, description="Sort order (asc, desc)", regex="^(asc|desc)$")
):
    """
    Get all tasks for the specified user, with optional search, filter, and sort.
    """
    # Validate that the user exists
    user_exists = AuthService.validate_user_exists(session, user_id)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Convert comma-separated tag IDs string to a list
    tag_ids_list = [tag_id.strip() for tag_id in tags.split(',')] if tags else None

    tasks = TaskService.get_tasks_by_user_id_with_filters(
        session, user_id, search, status, priority, tag_ids_list, sort_by, order
    )
    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Create a new task for the specified user, including priority and tags.
    """
    # Validate that the user exists
    user_exists = AuthService.validate_user_exists(session, user_id)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    task = TaskService.create_task(session, task_data, user_id)
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
    Update a specific task by ID for the specified user, including priority and tags.
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
    user_id: str = Depends(get_user_id_from_header),
    session: Session = Depends(get_sync_session)
):
    """
    Toggle the completion status of a specific task by ID for the specified user
    """
    # Get the current task to check its completion status
    current_task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)

    if not current_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    # Create a TaskUpdateCompletion with the opposite of current status
    from ..models.task_model import TaskUpdateCompletion
    completion_update = TaskUpdateCompletion(completed=not current_task.completed)

    updated_task = TaskService.update_task_completion(session, task_id, user_id, completion_update)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return updated_task