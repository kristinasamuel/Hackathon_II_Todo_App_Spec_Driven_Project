# Research Document: AI-Powered Todo Chatbot Implementation

## Overview
This document consolidates research findings for implementing the AI-powered Todo chatbot according to the feature specification.

## Database Schema Analysis

### Existing Schema Understanding
The existing Todo application likely has a task table with basic fields like:
- task_id (primary key)
- user_id (foreign key for user association)
- title (task title)
- description (task details)
- completed (boolean status)
- created_at (timestamp)
- updated_at (timestamp)

### Proposed Extensions
For the chatbot functionality, we need to add:

#### Conversations Table
```sql
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);
```

#### Messages Table
```sql
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id),
    role VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    tool_calls JSONB,
    tool_responses JSONB
);
```

## MCP Server Configuration

### Recommended Approach
- Use the official MCP SDK to create a Python-based MCP server
- Register the five required tools: add_task, list_tasks, update_task, complete_task, delete_task
- Keep the MCP server lightweight and focused only on tool execution
- Ensure tools connect to the existing database through the established connection pool

### Sample MCP Tool Registration
```python
from mcp.server import Server
import asyncio

server = Server("todo-mcp-server")

@server.handler("todo/add_task")
async def handle_add_task(params):
    # Implementation that connects to existing DB
    pass

# Similar handlers for other tools...
```

## Frontend Integration with ChatKit

### Integration Strategy
- Use OpenAI's ChatKit components to create a chat interface
- Integrate into existing frontend layout without disrupting current functionality
- Maintain consistent styling with existing UI
- Add a toggle or separate section for chat functionality

### API Connection
- Connect ChatKit to the new `/api/{user_id}/chat` endpoint
- Handle authentication token passing securely
- Implement loading states and error handling

## Authentication Context in Chat

### Recommended Flow
1. User accesses chat through existing authenticated session
2. Frontend extracts JWT token from existing auth context
3. Token is sent with each chat request in Authorization header
4. Backend validates token and extracts user_id
5. User_id is passed to MCP tools to ensure proper data access

### Security Measures
- Validate JWT tokens on each request
- Verify user_id in token matches requested user_id in endpoint
- Prevent cross-user data access
- Implement proper error responses for authentication failures

## Error Handling and Confirmation Strategy

### AI Confirmation Patterns
- For destructive operations (delete, complete): "I'm about to delete task 'X'. Is that correct?"
- For creation: "I've added task 'X' to your list."
- For updates: "I've updated task 'X' as requested."

### Error Recovery
- Graceful handling of MCP tool failures
- Inform users of system limitations
- Provide alternative phrasing suggestions when input is unclear

## Performance Considerations

### Caching Strategy
- Cache frequently accessed user data
- Implement conversation history pagination
- Consider Redis for temporary conversation context

### Rate Limiting
- Implement API rate limiting to prevent abuse
- Consider token-based rate limiting for AI API calls
- Monitor and log performance metrics

## Deployment Architecture

### Service Separation
- MCP server as a separate service (possibly containerized)
- Main FastAPI app handling chat endpoint
- Database connection pooling for concurrent access
- CDN for static assets if needed

### Environment Variables Needed
- OPENAI_API_KEY: Access key for OpenAI services
- DATABASE_URL: Connection string for PostgreSQL
- JWT_SECRET: Secret for token validation
- MCP_SERVER_URL: URL for MCP server connection