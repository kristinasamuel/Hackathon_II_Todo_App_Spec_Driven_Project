from typing import List, Optional
from sqlmodel import select, Session, and_
from ..models.task_model import Task, TaskCreate, TaskUpdate, TaskUpdateCompletion
from ..models.user_model import User
from uuid import UUID


class TaskService:
    """
    Service class for handling task-related business logic
    """

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
        """
        Create a new task
        """
        task_data_dict = task_data.model_dump()
        task_data_dict['user_id'] = user_id
        task = Task.model_validate(task_data_dict)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_tasks_by_user_id(session: Session, user_id: str) -> List[Task]:
        """
        Get all tasks for a specific user
        """
        statement = select(Task).where(Task.user_id == user_id)
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
        Update a task with ownership validation
        """
        task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if not task:
            return None

        # Update only provided fields
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        session.add(task)
        session.commit()
        session.refresh(task)
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
        return task

    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a task with ownership validation
        """
        task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True