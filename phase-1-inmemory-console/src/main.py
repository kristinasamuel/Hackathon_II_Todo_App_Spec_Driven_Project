"""
Main application entry point with menu loop.
Implements the main application flow with welcome message and menu structure.
"""
import sys
import os
# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from services.todo_service import TodoService
from cli.ui import (
    display_menu,
    get_user_choice,
    display_success_message,
    display_error_message,
    display_todos_table,
    add_todo_ui,
    update_todo_ui,
    delete_todo_ui,
    mark_todo_ui
)


def main():
    """
    Main application loop implementing the menu system.
    """
    # Initialize the todo service
    todo_service = TodoService()


    while True:
        display_menu()
        choice = get_user_choice()

        if choice is None:
            # Invalid input was already handled in get_user_choice
            continue

        if choice == 1:
            # Add Todo
            add_todo_ui(todo_service)

        elif choice == 2:
            # View Todos
            todos = todo_service.get_all_todos()
            display_todos_table(todos)

        elif choice == 3:
            # Update Todo
            update_todo_ui(todo_service)

        elif choice == 4:
            # Delete Todo
            delete_todo_ui(todo_service)

        elif choice == 5:
            # Mark Todo Complete/Incomplete
            mark_todo_ui(todo_service)

        elif choice == 6:
            # Exit
            display_success_message("Thank you for using the Todo Console App. Goodbye! 👏")
            break

        else:
            # Invalid menu option
            display_error_message("Invalid option. Please select a number between 1-6.")


if __name__ == "__main__":
    main()