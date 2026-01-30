# MCP Tool Contracts: AI-Powered Todo Chatbot

## Overview
This document defines the MCP (Model Context Protocol) tool contracts for the AI-powered Todo chatbot.

## Tool: add_task

### Purpose
Create a new task for the authenticated user

### Parameters
```json
{
  "user_id": {
    "type": "string",
    "description": "Unique identifier of the user",
    "required": true
  },
  "title": {
    "type": "string",
    "description": "Title of the new task",
    "required": true
  },
  "description": {
    "type": "string",
    "description": "Detailed description of the task",
    "required": false,
    "default": ""
  }
}
```

### Response
```json
{
  "task_id": {
    "type": "string",
    "description": "Unique identifier of the created task"
  },
  "message": {
    "type": "string",
    "description": "Confirmation message"
  }
}
```

### Database Interaction
- Inserts a new record into the tasks table
- Sets initial status to 'pending'
- Associates the task with the provided user_id

### Expected Behavior
- Creates a new task with the given title and description
- Returns the new task ID and a confirmation message
- Validates that the user exists and can create tasks

### Error Handling
- Returns error if user_id is invalid or doesn't exist
- Returns error if title is empty
- Returns error if database insertion fails

### Example Input
```json
{
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Need to buy milk and bread"
}
```

### Example Output
```json
{
  "task_id": "task456",
  "message": "Task 'Buy groceries' has been added to your list"
}
```

## Tool: list_tasks

### Purpose
Retrieve all tasks for the authenticated user

### Parameters
```json
{
  "user_id": {
    "type": "string",
    "description": "Unique identifier of the user",
    "required": true
  },
  "status_filter": {
    "type": "string",
    "description": "Filter tasks by status",
    "required": false,
    "enum": ["all", "pending", "completed"],
    "default": "all"
  }
}
```

### Response
```json
{
  "tasks": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "task_id": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "completed": {"type": "boolean"}
      }
    },
    "description": "Array of task objects"
  }
}
```

### Database Interaction
- Queries the tasks table filtered by user_id
- Optionally filters by completion status based on status_filter parameter

### Expected Behavior
- Returns all tasks associated with the user
- Applies status filter if specified
- Returns empty array if no tasks match criteria

### Error Handling
- Returns error if user_id is invalid or doesn't exist
- Returns error if status_filter is not one of the allowed values

### Example Input
```json
{
  "user_id": "user123",
  "status_filter": "pending"
}
```

### Example Output
```json
{
  "tasks": [
    {
      "task_id": "task456",
      "title": "Buy groceries",
      "description": "Need to buy milk and bread",
      "completed": false
    }
  ]
}
```

## Tool: update_task

### Purpose
Modify an existing task's title or description

### Parameters
```json
{
  "user_id": {
    "type": "string",
    "description": "Unique identifier of the user",
    "required": true
  },
  "task_id": {
    "type": "string",
    "description": "Unique identifier of the task to update",
    "required": true
  },
  "title": {
    "type": "string",
    "description": "New title for the task",
    "required": false
  },
  "description": {
    "type": "string",
    "description": "New description for the task",
    "required": false
  }
}
```

### Response
```json
{
  "message": {
    "type": "string",
    "description": "Confirmation message"
  }
}
```

### Database Interaction
- Updates the specified task record in the tasks table
- Only updates fields that are provided in the parameters

### Expected Behavior
- Updates the specified task with provided fields
- Validates that the user owns the task
- Returns confirmation message

### Error Handling
- Returns error if user_id or task_id is invalid
- Returns error if user doesn't own the specified task
- Returns error if neither title nor description is provided
- Returns error if database update fails

### Example Input
```json
{
  "user_id": "user123",
  "task_id": "task456",
  "title": "Buy organic groceries"
}
```

### Example Output
```json
{
  "message": "Task 'Buy organic groceries' has been updated successfully"
}
```

## Tool: complete_task

### Purpose
Mark a task as completed

### Parameters
```json
{
  "user_id": {
    "type": "string",
    "description": "Unique identifier of the user",
    "required": true
  },
  "task_id": {
    "type": "string",
    "description": "Unique identifier of the task to complete",
    "required": true
  },
  "completed": {
    "type": "boolean",
    "description": "Whether to mark task as completed or not",
    "required": false,
    "default": true
  }
}
```

### Response
```json
{
  "message": {
    "type": "string",
    "description": "Confirmation message"
  }
}
```

### Database Interaction
- Updates the completion status of the specified task in the tasks table

### Expected Behavior
- Updates the completion status of the specified task
- Validates that the user owns the task
- Returns confirmation message

### Error Handling
- Returns error if user_id or task_id is invalid
- Returns error if user doesn't own the specified task
- Returns error if database update fails

### Example Input
```json
{
  "user_id": "user123",
  "task_id": "task456",
  "completed": true
}
```

### Example Output
```json
{
  "message": "Task 'Buy organic groceries' has been marked as completed"
}
```

## Tool: delete_task

### Purpose
Remove a task from the user's list

### Parameters
```json
{
  "user_id": {
    "type": "string",
    "description": "Unique identifier of the user",
    "required": true
  },
  "task_id": {
    "type": "string",
    "description": "Unique identifier of the task to delete",
    "required": true
  }
}
```

### Response
```json
{
  "message": {
    "type": "string",
    "description": "Confirmation message"
  }
}
```

### Database Interaction
- Deletes the specified task record from the tasks table

### Expected Behavior
- Removes the specified task from the user's list
- Validates that the user owns the task
- Returns confirmation message

### Error Handling
- Returns error if user_id or task_id is invalid
- Returns error if user doesn't own the specified task
- Returns error if database deletion fails

### Example Input
```json
{
  "user_id": "user123",
  "task_id": "task456"
}
```

### Example Output
```json
{
  "message": "Task 'Buy organic groceries' has been deleted from your list"
}
```