# Data Model: AI-Powered Todo Chatbot

## Overview
This document defines the data models required for the AI-powered Todo chatbot, extending the existing Todo application schema.

## Entity Relationships

```
User (1) -----> (Many) Conversation
Conversation (1) -----> (Many) Message
User (1) -----> (Many) Task
```

## Detailed Entity Definitions

### User Entity
*Note: This entity is assumed to exist from the base Todo application*

- **user_id**: UUID (Primary Key)
  - Unique identifier for each user
  - Used across all related entities for access control

- **username**: String
  - User's display name or login identifier

- **email**: String
  - User's email address for authentication

- **created_at**: DateTime
  - Timestamp when user account was created

- **updated_at**: DateTime
  - Timestamp when user account was last updated

### Conversation Entity

- **conversation_id**: UUID (Primary Key)
  - Unique identifier for each conversation
  - Auto-generated using gen_random_uuid()

- **user_id**: UUID (Foreign Key: User.user_id)
  - Links conversation to the owning user
  - Ensures users can only access their own conversations

- **created_at**: DateTime
  - Timestamp when conversation was initiated
  - Default: NOW()

- **updated_at**: DateTime
  - Timestamp of last activity in conversation
  - Updated whenever a new message is added

- **metadata**: JSONB
  - Additional context for the conversation
  - May include: topic, language preference, etc.

### Message Entity

- **message_id**: UUID (Primary Key)
  - Unique identifier for each message
  - Auto-generated using gen_random_uuid()

- **conversation_id**: UUID (Foreign Key: Conversation.conversation_id)
  - Links message to its conversation thread
  - Enables conversation history retrieval

- **role**: VARCHAR(20)
  - Role of the message sender
  - Values: 'user', 'assistant', 'system'

- **content**: TEXT
  - The actual content of the message
  - May contain natural language or structured data

- **timestamp**: DateTime
  - When the message was created
  - Default: NOW()

- **tool_calls**: JSONB
  - Details of any tools called by the AI
  - Format: [{"name": "tool_name", "arguments": {...}}, ...]

- **tool_responses**: JSONB
  - Results from executed tools
  - Format: [{"tool_call_id": "...", "output": {...}}, ...]

### Task Entity
*Note: This entity extends the existing Task entity from the base Todo application*

- **task_id**: UUID (Primary Key)
  - Unique identifier for each task
  - Existing field from base application

- **user_id**: UUID (Foreign Key: User.user_id)
  - Links task to the owning user
  - Existing field from base application

- **title**: STRING
  - The title of the task
  - Existing field from base application

- **description**: TEXT
  - Detailed description of the task
  - Existing field from base application

- **completed**: BOOLEAN
  - Completion status of the task
  - Existing field from base application

- **created_at**: DateTime
  - When the task was created
  - Existing field from base application

- **updated_at**: DateTime
  - When the task was last modified
  - Existing field from base application

## Indexes for Performance

### Conversation Entity
- Index on (user_id) - for quick user-specific queries
- Index on (created_at DESC) - for chronological ordering
- Composite index on (user_id, created_at DESC) - for user timeline queries

### Message Entity
- Index on (conversation_id, timestamp ASC) - for chronological conversation history
- Index on (timestamp DESC) - for global message queries
- Index on (role) - for role-based filtering

### Task Entity
- Index on (user_id, completed) - for user task status queries
- Index on (user_id, created_at DESC) - for user task timeline

## Validation Rules

### Conversation Entity
- user_id must exist in Users table (foreign key constraint)
- created_at must not be in the future
- updated_at must be >= created_at

### Message Entity
- conversation_id must exist in Conversations table (foreign key constraint)
- role must be one of 'user', 'assistant', 'system'
- content must not exceed 10,000 characters
- timestamp must not be in the future
- tool_calls must be valid JSON if present
- tool_responses must be valid JSON if present

### Task Entity
- user_id must exist in Users table (foreign key constraint)
- title must not be empty
- completed must be boolean

## State Transitions

### Task State Transitions
- pending → completed (via complete_task tool)
- completed → pending (via update_task tool with completed=False)

### Message Role Transitions
- user → assistant (AI responds to user message)
- system → assistant (AI acts on system instruction)

## Sample Data

### Sample Conversation
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",
  "user_id": "z9y8x7w6-v5u4-3210-fedc-ba9876543210",
  "created_at": "2026-01-28T10:00:00Z",
  "updated_at": "2026-01-28T10:05:00Z",
  "metadata": {
    "topic": "grocery planning",
    "language": "en"
  }
}
```

### Sample Message
```json
{
  "message_id": "h5j4k3l2-m1n0-9876-fedc-ba5432109876",
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",
  "role": "user",
  "content": "Add a task to buy milk and bread",
  "timestamp": "2026-01-28T10:01:00Z",
  "tool_calls": null,
  "tool_responses": null
}
```

### Sample Tool Call Response
```json
{
  "message_id": "p9q8r7s6-t5u4-3210-fedc-ba9876543210",
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",
  "role": "assistant",
  "content": "I've added the task 'buy milk and bread' to your list.",
  "timestamp": "2026-01-28T10:01:30Z",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "z9y8x7w6-v5u4-3210-fedc-ba9876543210",
        "title": "buy milk and bread",
        "description": ""
      }
    }
  ],
  "tool_responses": [
    {
      "tool_call_id": "call_abc123def456",
      "output": {
        "task_id": "task_123456789",
        "message": "Task 'buy milk and bread' has been added to your list"
      }
    }
  ]
}
```