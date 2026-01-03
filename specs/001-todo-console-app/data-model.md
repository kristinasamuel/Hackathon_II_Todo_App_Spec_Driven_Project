# Data Model: Todo In-Memory Python Console Application

## Todo Entity

### Attributes
- **id**: `int` - Unique identifier assigned automatically when the todo is created (incremental counter starting from 1)
- **title**: `str` - Required text field representing the name or subject of the todo (non-empty string)
- **description**: `str` - Optional text field providing additional details about the todo (can be empty string)
- **status**: `bool` - Boolean field indicating whether the todo is Complete (True) or Incomplete (False), defaults to False

### Data Structure
The todos will be stored in memory as a list of dictionaries, where each dictionary represents a todo item:
```python
todos = [
    {
        "id": 1,
        "title": "Sample todo title",
        "description": "Sample description",
        "status": False  # False = Incomplete, True = Complete
    },
    # ... more todo items
]
```

### Validation Rules
- ID must be a positive integer
- Title must be a non-empty string (after stripping whitespace)
- Description can be any string (including empty)
- Status must be a boolean value
- No two todos can have the same ID

### State Transitions
- **Incomplete to Complete**: When user marks a todo as complete using option 5
- **Complete to Incomplete**: When user marks a completed todo as incomplete using option 5

## In-Memory Storage
- The entire todo list exists only in memory during the application session
- No persistence between application runs
- Data is lost when the application exits