from typing import List, Optional, Tuple
from sqlmodel import select, Session, and_, or_, col, desc
from ..models.task_model import Task, TaskCreate, TaskUpdate, TaskUpdateCompletion, Priority
from ..models.user_model import User
from ..models.tag_model import Tag, TaskTagLink
from fastapi import HTTPException, status # Import HTTPException for proper error handling
from uuid import UUID
from datetime import datetime
import json

# Import the DAPR helper with fallback
from ..utils.dapr_helper import publish_event


class TaskService:
    """
    Service class for handling task-related business logic
    """

    @staticmethod
    def _apply_tags_to_task(session: Session, task: Task, tag_ids: List[str], user_id: str):
        """Helper to manage tag associations for a task."""
        if not tag_ids:
            # If no tag_ids are provided, clear existing tags
            session.exec(
                TaskTagLink.delete().where(TaskTagLink.task_id == task.id)
            )
            task.tags.clear()
            session.flush()
            return

        # Fetch existing tags to validate ownership and existence
        valid_tags = session.exec(
            select(Tag).where(Tag.id.in_(tag_ids), Tag.user_id == user_id)
        ).all()

        if len(valid_tags) != len(tag_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more provided tag IDs are invalid or do not belong to the user."
            )

        # Clear existing associations for this task
        session.exec(
            TaskTagLink.delete().where(TaskTagLink.task_id == task.id)
        )
        session.flush()

        # Create new associations
        for tag in valid_tags:
            link = TaskTagLink(task_id=task.id, tag_id=tag.id)
            session.add(link)
        session.flush() # Flush to ensure relationships are updated before refresh

        # Reload tags relationship to reflect changes
        session.refresh(task, attribute_names=["tags"])


    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
        """
        Create a new task, including priority, due_date, and tags, and publish a TaskCreated event.
        """
        task_data_dict = task_data.model_dump(exclude_unset=True, exclude={'tag_ids'})
        task_data_dict['user_id'] = user_id
        task = Task.model_validate(task_data_dict)
        session.add(task)
        session.flush() # Flush to get task.id before linking tags

        if task_data.tag_ids:
            TaskService._apply_tags_to_task(session, task, task_data.tag_ids, user_id)

        session.commit()
        session.refresh(task)

        # Publish TaskCreated event
        event_payload = {
            "eventType": "TaskCreated",
            "taskId": str(task.id),
            "userId": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority.value if task.priority else None,
            "dueDate": task.due_date.isoformat() if task.due_date else None,
            "isRecurring": False, # Placeholder, will be updated in later tasks
            "recurrenceRule": None, # Placeholder
            "reminderAt": None, # Placeholder
            "tags": [{"id": str(tag.id), "name": tag.name} for tag in task.tags],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        publish_event("pubsub", "task-events", event_payload)

        return task

    @staticmethod
    def get_tasks_by_user_id(session: Session, user_id: str) -> List[Task]:
        """
        Get all tasks for a specific user. (Deprecated by get_tasks_by_user_id_with_filters)
        """
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at)
        results = session.exec(statement)
        return results.all()

    @staticmethod
    def get_task_by_id_and_user_id(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a specific task by its ID and user ID (for ownership validation)
        """
        statement = select(Task).where(
            and_(Task.id == task_id, Task.user_id == user_id)
        )
        result = session.exec(statement)
        return result.first()

    @staticmethod
    def update_task(session: Session, task_id: str, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update a task with ownership validation, including priority, due_date, and tags, and publish a TaskUpdated event.
        """
        task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if not task:
            return None

        update_data = task_update.model_dump(exclude_unset=True, exclude={'tag_ids'})
        for field, value in update_data.items():
            setattr(task, field, value)

        if task_update.tag_ids is not None: # Only update if tag_ids is explicitly provided
            TaskService._apply_tags_to_task(session, task, task_update.tag_ids, user_id)

        session.add(task)
        session.commit()
        session.refresh(task)

        # Publish TaskUpdated event
        event_payload = {
            "eventType": "TaskUpdated",
            "taskId": str(task.id),
            "userId": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority.value if task.priority else None,
            "dueDate": task.due_date.isoformat() if task.due_date else None,
            "isRecurring": False, # Placeholder, will be updated in later tasks
            "recurrenceRule": None, # Placeholder
            "reminderAt": None, # Placeholder
            "tags": [{"id": str(tag.id), "name": tag.name} for tag in task.tags],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        publish_event("pubsub", "task-events", event_payload)

        return task

    @staticmethod
    def update_task_completion(session: Session, task_id: str, user_id: str, completion_update: TaskUpdateCompletion) -> Optional[Task]:
        """
        Update a task's completion status with ownership validation
        """
        task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if not task:
            return None

        task.completed = completion_update.completed

        session.add(task)
        session.commit()
        session.refresh(task)

        # Publish TaskUpdated event for completion status change
        event_payload = {
            "eventType": "TaskUpdated", # Or TaskCompletionUpdated if a more specific event is desired
            "taskId": str(task.id),
            "userId": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority.value if task.priority else None,
            "dueDate": task.due_date.isoformat() if task.due_date else None,
            "isRecurring": False,
            "recurrenceRule": None,
            "reminderAt": None,
            "tags": [{"id": str(tag.id), "name": tag.name} for tag in task.tags],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        publish_event("pubsub", "task-events", event_payload)

        return task

    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a task with ownership validation
        """
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
        if not task:
            return False

        # Publish TaskDeleted event
        event_payload = {
            "eventType": "TaskDeleted",
            "taskId": str(task.id),
            "userId": str(task.user_id),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        publish_event("pubsub", "task-events", event_payload)

        # Delete associated TaskTagLinks first
        session.exec(
            TaskTagLink.delete().where(TaskTagLink.task_id == task.id)
        )
        session.delete(task)
        session.commit()
        return True
    
    @staticmethod
    def get_tasks_by_user_id_with_filters(
        session: Session,
        user_id: str,
        search: Optional[str] = None,
        status_filter: Optional[str] = None, # Renamed to avoid conflict with 'status' parameter from FastAPI
        priority_filter: Optional[Priority] = None, # Renamed
        tag_ids_filter: Optional[List[str]] = None, # Renamed
        sort_by: Optional[str] = None,
        order: Optional[str] = None
    ) -> List[Task]:
        """
        Get all tasks for a specific user with optional search, filter, and sort.
        """
        statement = select(Task).where(Task.user_id == user_id)

        # Apply search filter
        if search:
            search_pattern = f"%{search}%"
            statement = statement.where(
                or_(
                    Task.title.ilike(search_pattern),
                    Task.description.ilike(search_pattern)
                )
            )

        # Apply status filter
        if status_filter:
            if status_filter.lower() == "completed":
                statement = statement.where(Task.completed == True)
            elif status_filter.lower() == "pending":
                statement = statement.where(Task.completed == False)

        # Apply priority filter
        if priority_filter:
            statement = statement.where(Task.priority == priority_filter)

        # Apply tags filter
        if tag_ids_filter:
            # Join with TaskTagLink and Tag to filter by tag IDs
            statement = statement.join(TaskTagLink, Task.id == TaskTagLink.task_id)
            statement = statement.where(TaskTagLink.tag_id.in_(tag_ids_filter))

        # Apply sorting
        if sort_by:
            if sort_by == "due_date":
                order_col = Task.due_date
            elif sort_by == "priority":
                # Custom sorting for enum (e.g., high=0, medium=1, low=2)
                # This requires a more complex case statement or custom SQL.
                # For simplicity, we'll sort alphabetically, but a proper solution
                # would map enum values to integers for ordering.
                order_col = Task.priority
            elif sort_by == "created_at":
                order_col = Task.created_at
            else:
                order_col = Task.created_at # Default sort

            if order and order.lower() == "desc":
                statement = statement.order_by(desc(order_col))
            else:
                statement = statement.order_by(order_col)
        else:
            statement = statement.order_by(Task.created_at) # Default sort if none specified


        results = session.exec(statement.distinct()) # Use distinct to avoid duplicate tasks due to tag join
        return results.all()