from typing import Dict, Any, List, Optional
from sqlmodel import Session, select

# Using absolute imports for the backend structure
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.task_model import TaskCreate, TaskUpdate, TaskUpdateCompletion
from src.services.task_service import TaskService
from src.services.auth_service import AuthService
from src.database.database import get_sync_session
from src.models.task_model import Task
import json


def get_db_session():
    """Get a database session - using the same connection as the main application"""
    # We'll get the session from the main application's database module
    # This ensures we're using the same database connection as the rest of the app
    session_generator = get_sync_session()
    return next(session_generator)


def _get_actual_task_id_by_display_number(user_id: str, display_number: int) -> Optional[str]:
    """
    Convert a display number (1-indexed) to the actual task ID
    """
    with get_db_session() as session:
        # Get all tasks for the user, ordered by creation date to match display order
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.asc())
        tasks = session.exec(statement).all()
        
        # Display numbers are 1-indexed, so subtract 1 to get 0-indexed position
        if 1 <= display_number <= len(tasks):
            return tasks[display_number - 1].id
        else:
            return None


# Functions for task operations that can be called from the AI agent
def execute_add_task(params: Dict[str, Any]) -> str:
    """
    Create a new task for the user
    """
    try:
        user_id = params.get("user_id")
        title = params.get("title")
        description = params.get("description", "")

        if not user_id or not title:
            return f"Error: Missing required parameters: user_id and title"

        # Validate user exists
        with get_db_session() as session:
            user_exists = AuthService.validate_user_exists(session, user_id)
            if not user_exists:
                return f"Error: User {user_id} does not exist"

            # Create the task
            task_data = TaskCreate(title=title, description=description, completed=False)
            task = TaskService.create_task(session, task_data, user_id)

            return f"Task '{task.title}' (ID: {task.id}) has been added to your list"
    except Exception as e:
        return f"Error adding task: {str(e)}"


def execute_list_tasks(params: Dict[str, Any]) -> str:
    """
    Retrieve tasks for the user
    """
    try:
        user_id = params.get("user_id")
        status_filter = params.get("status_filter", "all")  # all, pending, completed

        if not user_id:
            return "Error: Missing required parameter: user_id"

        # Validate user exists
        with get_db_session() as session:
            user_exists = AuthService.validate_user_exists(session, user_id)
            if not user_exists:
                return f"Error: User {user_id} does not exist"

            # Get tasks
            tasks = TaskService.get_tasks_by_user_id(session, user_id)

            # Filter based on status
            if status_filter == "pending":
                tasks = [task for task in tasks if not task.completed]
            elif status_filter == "completed":
                tasks = [task for task in tasks if task.completed]

            if not tasks:
                return "You have no tasks in your list"

            task_list = []
            for i, task in enumerate(tasks, 1):
                status = "X" if task.completed else "O"
                task_str = f"{i}. [{status}] {task.title}"
                if task.description:
                    task_str += f" - {task.description}"
                task_list.append(task_str)

            return "Your tasks:\n" + "\n".join(task_list)
    except Exception as e:
        return f"Error listing tasks: {str(e)}"


def execute_update_task(params: Dict[str, Any]) -> str:
    """
    Update an existing task
    """
    try:
        user_id = params.get("user_id")
        task_id = params.get("task_id")
        title = params.get("title")
        description = params.get("description")

        if not user_id or not task_id:
            return "Error: Missing required parameters: user_id and task_id"

        if not title and not description:
            return "Error: At least one of title or description must be provided"

        # Check if task_id is a display number (integer) and convert to actual task ID
        actual_task_id = task_id
        if isinstance(task_id, int) or (isinstance(task_id, str) and task_id.isdigit()):
            display_number = int(task_id)
            actual_task_id = _get_actual_task_id_by_display_number(user_id, display_number)
            if not actual_task_id:
                return f"Error: Task #{display_number} not found in your task list"

        with get_db_session() as session:
            # Validate user exists
            user_exists = AuthService.validate_user_exists(session, user_id)
            if not user_exists:
                return f"Error: User {user_id} does not exist"

            # Prepare update data
            update_data = {}
            if title is not None:
                update_data['title'] = title
            if description is not None:
                update_data['description'] = description

            task_update = TaskUpdate(**update_data)

            # Update the task
            updated_task = TaskService.update_task(session, actual_task_id, user_id, task_update)

            if not updated_task:
                return f"Error: Task {actual_task_id} not found or doesn't belong to user"

            return f"Task '{updated_task.title}' has been updated successfully"
    except Exception as e:
        return f"Error updating task: {str(e)}"


def execute_complete_task(params: Dict[str, Any]) -> str:
    """
    Mark a task as completed
    """
    try:
        user_id = params.get("user_id")
        task_id = params.get("task_id")
        completed = params.get("completed", True)

        if not user_id or not task_id:
            return "Error: Missing required parameters: user_id and task_id"

        # Check if task_id is a display number (integer) and convert to actual task ID
        actual_task_id = task_id
        if isinstance(task_id, int) or (isinstance(task_id, str) and task_id.isdigit()):
            display_number = int(task_id)
            actual_task_id = _get_actual_task_id_by_display_number(user_id, display_number)
            if not actual_task_id:
                return f"Error: Task #{display_number} not found in your task list"

        with get_db_session() as session:
            # Validate user exists
            user_exists = AuthService.validate_user_exists(session, user_id)
            if not user_exists:
                return f"Error: User {user_id} does not exist"

            # Get current task to determine status text
            current_task = TaskService.get_task_by_id_and_user_id(session, actual_task_id, user_id)
            if not current_task:
                return f"Error: Task {actual_task_id} not found or doesn't belong to user"

            # Create completion update
            completion_update = TaskUpdateCompletion(completed=completed)

            # Update the task completion status
            updated_task = TaskService.update_task_completion(session, actual_task_id, user_id, completion_update)

            if not updated_task:
                return f"Error: Failed to update task completion status"

            status_text = "completed" if completed else "marked as pending"
            return f"Task '{updated_task.title}' has been {status_text}"
    except Exception as e:
        return f"Error completing task: {str(e)}"


def execute_delete_task(params: Dict[str, Any]) -> str:
    """
    Delete a task
    """
    try:
        user_id = params.get("user_id")
        task_id = params.get("task_id")

        if not user_id or not task_id:
            return "Error: Missing required parameters: user_id and task_id"

        # Check if task_id is a display number (integer) and convert to actual task ID
        actual_task_id = task_id
        if isinstance(task_id, int) or (isinstance(task_id, str) and task_id.isdigit()):
            display_number = int(task_id)
            actual_task_id = _get_actual_task_id_by_display_number(user_id, display_number)
            if not actual_task_id:
                return f"Error: Task #{display_number} not found in your task list"

        with get_db_session() as session:
            # Validate user exists
            user_exists = AuthService.validate_user_exists(session, user_id)
            if not user_exists:
                return f"Error: User {user_id} does not exist"

            # Get task title for confirmation message
            task = TaskService.get_task_by_id_and_user_id(session, actual_task_id, user_id)
            if not task:
                return f"Error: Task {actual_task_id} not found or doesn't belong to user"

            # Delete the task
            success = TaskService.delete_task(session, actual_task_id, user_id)

            if not success:
                return f"Error: Failed to delete task"

            return f"Task '{task.title}' has been deleted from your list"
    except Exception as e:
        return f"Error deleting task: {str(e)}"


def execute_get_user_info(params: Dict[str, Any]) -> str:
    """
    Get user information
    """
    try:
        user_id = params.get("user_id")

        if not user_id:
            return "Error: Missing required parameter: user_id"

        with get_db_session() as session:
            # Validate user exists
            user_exists = AuthService.validate_user_exists(session, user_id)
            if not user_exists:
                return f"Error: User {user_id} does not exist"

            # Get user from database
            from src.models.user_model import User
            from sqlmodel import select

            statement = select(User).where(User.id == user_id)
            user = session.exec(statement).first()

            if not user:
                return f"Error: User {user_id} not found in database"

            return f"You are logged in as {user.email}. Your user ID is {user.id}."
    except Exception as e:
        return f"Error retrieving user information: {str(e)}"