# Quickstart Guide: Todo In-Memory Python Console Application

## Prerequisites
- Python 3.13+ installed
- UV package manager installed

## Setup
1. Clone or navigate to the project directory
2. Install dependencies using UV:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

## Running the Application
1. Navigate to the project directory
2. Run the main application file:
   ```bash
   python main.py
   ```

## Using the Application
1. The application will display a welcome message and the main menu
2. Select an option by entering the corresponding number (1-6)
3. Follow the prompts for each operation
4. The application will return to the main menu after each operation
5. Select option 6 to exit the application

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
Enter todo description (optional): Need to buy milk and bread
Todo added successfully with ID 1!

Select an option: 2
ID | Status     | Title         | Description
---|------------|---------------|--------------------
1  | Incomplete | Buy groceries | Need to buy milk and bread

Select an option: 5
Enter the ID of the todo to mark complete/incomplete: 1
Todo ID 1 marked as Complete!
```

## Troubleshooting
- If you get an "invalid option" error, ensure you're entering a number between 1-6
- If you get an "invalid ID" error, ensure the todo ID exists in the list
- If the application crashes, check that you're entering valid input when prompted