"""
Todo service handling business logic for todo operations.
Uses in-memory storage (list of dictionaries) as specified in the research.
"""
from typing import List, Dict, Optional
import sys
import os
# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.todo import Todo


class TodoService:
    """
    Service class handling all todo-related operations with in-memory storage.
    """

    def __init__(self):
        """
        Initialize the TodoService with an empty list for storage.
        """
        self.todos: List[Dict] = []
        self.next_id = 1

    def add_todo(self, title: str, description: str = "") -> Todo:
        """
        Add a new todo to the in-memory list.

        Args:
            title (str): Title of the todo (required)
            description (str): Description of the todo (optional)

        Returns:
            Todo: The created Todo object
        """
        if not title or not title.strip():
            raise ValueError("Title must be a non-empty string")

        # Create the todo dictionary with the next available ID
        todo_dict = {
            "id": self.next_id,
            "title": title.strip(),
            "description": description,
            "status": False  # Default to incomplete
        }

        # Add to the list
        self.todos.append(todo_dict)

        # Create and return a Todo object
        todo = Todo.from_dict(todo_dict)

        # Increment the ID for the next todo
        self.next_id += 1

        return todo

    def get_all_todos(self) -> List[Dict]:
        """
        Get all todos from the in-memory list.

        Returns:
            List[Dict]: List of all todos as dictionaries
        """
        return self.todos

    def get_todo_by_id(self, todo_id: int) -> Optional[Dict]:
        """
        Get a specific todo by its ID.

        Args:
            todo_id (int): ID of the todo to retrieve

        Returns:
            Optional[Dict]: The todo dictionary if found, None otherwise
        """
        for todo in self.todos:
            if todo["id"] == todo_id:
                return todo
        return None

    def update_todo(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing todo by its ID.

        Args:
            todo_id (int): ID of the todo to update
            title (Optional[str]): New title for the todo (optional)
            description (Optional[str]): New description for the todo (optional)

        Returns:
            bool: True if the todo was updated, False if not found
        """
        for todo in self.todos:
            if todo["id"] == todo_id:
                # Update title if provided
                if title is not None:
                    if not title or not title.strip():
                        raise ValueError("Title must be a non-empty string")
                    todo["title"] = title.strip()

                # Update description if provided
                if description is not None:
                    todo["description"] = description

                return True
        return False

    def toggle_todo_status(self, todo_id: int) -> bool:
        """
        Toggle the status of a todo (Complete/Incomplete).

        Args:
            todo_id (int): ID of the todo to toggle

        Returns:
            bool: True if the status was toggled, False if not found
        """
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["status"] = not todo["status"]  # Toggle the status
                return True
        return False

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo by its ID.

        Args:
            todo_id (int): ID of the todo to delete

        Returns:
            bool: True if the todo was deleted, False if not found
        """
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                del self.todos[i]
                return True
        return False

    def validate_todo_id(self, todo_id: int) -> bool:
        """
        Check if a todo ID exists in the list.

        Args:
            todo_id (int): ID to validate

        Returns:
            bool: True if the ID exists, False otherwise
        """
        return self.get_todo_by_id(todo_id) is not None