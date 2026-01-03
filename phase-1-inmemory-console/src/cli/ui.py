"""
User interface functions for console I/O operations.
"""
from typing import Optional
import sys
import os
# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.todo_service import TodoService


def display_menu():
    """
    Display the main menu options to the user.
    """
    print("\nWelcome to the Todo Console App")
    print("\n1. Add Todo")
    print("2. View Todos")
    print("3. Update Todo")
    print("4. Delete Todo")
    print("5. Mark Todo Complete / Incomplete")
    print("6. Exit")


def get_user_choice() -> Optional[int]:
    """
    Get and validate user's menu choice.

    Returns:
        Optional[int]: The user's choice (1-6) or None if invalid input
    """
    try:
        choice = input("\nSelect an option: ").strip()
        return int(choice)
    except ValueError:
        print("Invalid input. Please enter a number between 1-6.")
        return None


def display_success_message(message: str):
    """
    Display a success message to the user.

    Args:
        message (str): The success message to display
    """
    print(f"\n{message}")


def display_error_message(message: str):
    """
    Display an error message to the user.

    Args:
        message (str): The error message to display
    """
    print(f"\nError: {message}")


def display_todos_table(todos: list):
    """
    Display todos in a structured table format.

    Args:
        todos (list): List of todo dictionaries to display
    """
    if not todos:
        print("\nNo todos to show.")
        return

    # Print table header
    print("\nID | Status     | Title         | Description")
    print("---|------------|---------------|------------")

    # Print each todo
    for todo in todos:
        status = "Complete" if todo["status"] else "Incomplete"
        # Truncate title and description to fit in the table
        title = todo["title"][:13] + "..." if len(todo["title"]) > 13 else todo["title"]
        description = todo["description"][:11] + "..." if len(todo["description"]) > 11 else todo["description"]
        print(f"{todo['id']:2} | {status:10} | {title:13} | {description}")


def add_todo_ui(todo_service: TodoService):
    """
    Handle the UI flow for adding a new todo.

    Args:
        todo_service (TodoService): The todo service to use
    """
    title = input("Enter todo title: ").strip()
    if not title:
        display_error_message("Title cannot be empty.")
        return

    description = input("Enter todo description (optional): ").strip()

    try:
        todo = todo_service.add_todo(title, description)
        display_success_message(f"Todo added successfully with ID {todo.id}!")
    except ValueError as e:
        display_error_message(str(e))


def update_todo_ui(todo_service: TodoService):
    """
    Handle the UI flow for updating an existing todo.

    Args:
        todo_service (TodoService): The todo service to use
    """
    try:
        todo_id = int(input("Enter the ID of the todo to update: "))
    except ValueError:
        display_error_message("Invalid ID. Please enter a number.")
        return

    # Check if todo exists
    if not todo_service.validate_todo_id(todo_id):
        display_error_message(f"Todo with ID {todo_id} does not exist.")
        return

    title = input("Enter new title (or press Enter to keep current): ").strip()
    description = input("Enter new description (or press Enter to keep current): ").strip()

    # Prepare update parameters
    update_title = title if title else None
    update_description = description if description else None

    # If both are empty, it means user wants to keep both as is
    if update_title is None and update_description == "":
        update_description = None

    try:
        success = todo_service.update_todo(todo_id, update_title, update_description)
        if success:
            display_success_message(f"Todo ID {todo_id} updated successfully!")
        else:
            display_error_message("Failed to update todo.")
    except ValueError as e:
        display_error_message(str(e))


def delete_todo_ui(todo_service: TodoService):
    """
    Handle the UI flow for deleting a todo.

    Args:
        todo_service (TodoService): The todo service to use
    """
    try:
        todo_id = int(input("Enter the ID of the todo to delete: "))
    except ValueError:
        display_error_message("Invalid ID. Please enter a number.")
        return

    # Check if todo exists
    if not todo_service.validate_todo_id(todo_id):
        display_error_message(f"Todo with ID {todo_id} does not exist.")
        return

    success = todo_service.delete_todo(todo_id)
    if success:
        display_success_message(f"Todo ID {todo_id} deleted successfully!")
    else:
        display_error_message("Failed to delete todo.")


def mark_todo_ui(todo_service: TodoService):
    """
    Handle the UI flow for marking a todo as complete/incomplete.

    Args:
        todo_service (TodoService): The todo service to use
    """
    try:
        todo_id = int(input("Enter the ID of the todo to mark complete/incomplete: "))
    except ValueError:
        display_error_message("Invalid ID. Please enter a number.")
        return

    # Check if todo exists
    if not todo_service.validate_todo_id(todo_id):
        display_error_message(f"Todo with ID {todo_id} does not exist.")
        return

    success = todo_service.toggle_todo_status(todo_id)
    if success:
        # Get the current status to display the appropriate message
        todo = todo_service.get_todo_by_id(todo_id)
        status = "Complete" if todo["status"] else "Incomplete"
        display_success_message(f"Todo ID {todo_id} marked as {status}!")
    else:
        display_error_message("Failed to update todo status.")