# Todo Console Application

A simple console-based todo application with in-memory storage, built with Python.

## Features

- Add, view, update, delete, and mark todos as complete/incomplete
- Simple menu-driven interface
- In-memory storage (no persistence between runs)
- Clean and intuitive console output

## Requirements

- Python 3.13 or higher

## Installation and Setup

1. Clone or download this repository
2. Navigate to the `phase-1-inmemory-console` directory
3. No additional dependencies needed - the application uses only Python standard library

## Usage

To run the application:

```bash
python src/main.py
```

## Functionality

The application provides the following menu options:

1. **Add Todo**: Add a new todo with a title and optional description
2. **View Todos**: Display all todos in a formatted table
3. **Update Todo**: Modify an existing todo's title or description
4. **Delete Todo**: Remove a todo by its ID
5. **Mark Todo Complete/Incomplete**: Toggle a todo's status
6. **Exit**: Quit the application

## Example Usage

```
Welcome to the Todo Console App

1. Add Todo
2. View Todos
3. Update Todo
4. Delete Todo
5. Mark Todo Complete / Incomplete
6. Exit

Select an option: 1
Enter todo title: Buy groceries
Enter todo description (optional): Need to buy milk, bread, and eggs
Todo added successfully with ID 1!

Select an option: 2

ID | Status     | Title         | Description
---|------------|---------------|------------
 1 | Incomplete | Buy groceries | Need to buy m...
```

## Project Structure

```
phase-1-inmemory-console/
├── src/
│   ├── main.py               # Main application entry point
│   ├── models/
│   │   └── todo.py          # Todo class definition
│   ├── services/
│   │   └── todo_service.py  # Business logic for todo operations
│   └── cli/
│       └── ui.py            # User interface functions
├── requirements.txt          # Dependencies (none required)
├── setup.py                 # Setup configuration
└── README.md               # This file
```

## Testing

The application is designed following the specifications in the original project. All functionality can be tested manually through the console interface."# Hackathon_II_Todo_App_Spec_Driven_project" 
