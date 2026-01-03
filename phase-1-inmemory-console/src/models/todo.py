"""
Todo model representing a task that needs to be completed.
"""
from typing import Dict, Any


class Todo:
    """
    Represents a todo item with ID, Title, Description, and Status attributes.
    """

    def __init__(self, id: int, title: str, description: str = "", status: bool = False):
        """
        Initialize a Todo object.

        Args:
            id (int): Unique identifier for the todo
            title (str): Required title of the todo (non-empty after stripping)
            description (str): Optional description of the todo
            status (bool): Status of the todo (False = Incomplete, True = Complete)
        """
        if not title or not title.strip():
            raise ValueError("Title must be a non-empty string")

        self.id = id
        self.title = title.strip()
        self.description = description
        self.status = status  # False = Incomplete, True = Complete

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Todo object to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary representation of the Todo
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create a Todo object from a dictionary representation.

        Args:
            data (Dict[str, Any]): Dictionary containing todo data

        Returns:
            Todo: Todo object created from the dictionary
        """
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", False)
        )

    def __str__(self) -> str:
        """
        String representation of the Todo.

        Returns:
            str: Formatted string representation
        """
        status_str = "Complete" if self.status else "Incomplete"
        return f"[{self.id}] {self.title} - {status_str}"

    def __repr__(self) -> str:
        """
        Detailed string representation of the Todo.

        Returns:
            str: Detailed string representation
        """
        return f"Todo(id={self.id}, title='{self.title}', description='{self.description}', status={self.status})"