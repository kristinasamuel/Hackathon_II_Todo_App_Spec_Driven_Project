import pytest
from sqlmodel import Session
from src.models.task_model import Task, TaskCreate
from src.services.task_service import TaskService


def test_create_task(session: Session):
    """
    Test creating a new task
    """
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        user_id="user123"
    )

    created_task = TaskService.create_task(session, task_data)

    assert created_task.title == "Test Task"
    assert created_task.description == "This is a test task"
    assert created_task.user_id == "user123"
    assert created_task.completed is False


def test_get_tasks_by_user_id(session: Session):
    """
    Test getting tasks by user ID
    """
    # Create a test task first
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        user_id="user123"
    )
    TaskService.create_task(session, task_data)

    # Get tasks for the user
    tasks = TaskService.get_tasks_by_user_id(session, "user123")

    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"


def test_get_task_by_id_and_user_id(session: Session):
    """
    Test getting a specific task by ID and user ID
    """
    # Create a test task
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        user_id="user123"
    )
    created_task = TaskService.create_task(session, task_data)

    # Get the task by ID and user ID
    retrieved_task = TaskService.get_task_by_id_and_user_id(session, created_task.id, "user123")

    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Test Task"


def test_update_task(session: Session):
    """
    Test updating a task
    """
    # Create a test task
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        user_id="user123"
    )
    created_task = TaskService.create_task(session, task_data)

    # Update the task
    from src.models.task_model import TaskUpdate
    update_data = TaskUpdate(
        title="Updated Task",
        completed=True
    )
    updated_task = TaskService.update_task(session, created_task.id, "user123", update_data)

    assert updated_task is not None
    assert updated_task.title == "Updated Task"
    assert updated_task.completed is True


def test_delete_task(session: Session):
    """
    Test deleting a task
    """
    # Create a test task
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        user_id="user123"
    )
    created_task = TaskService.create_task(session, task_data)

    # Delete the task
    success = TaskService.delete_task(session, created_task.id, "user123")

    assert success is True

    # Verify the task is gone
    retrieved_task = TaskService.get_task_by_id_and_user_id(session, created_task.id, "user123")
    assert retrieved_task is None