# Quickstart Guide: AI-Powered Todo Chatbot

## Overview
This guide provides step-by-step instructions to set up and run the AI-powered Todo chatbot locally.

## Prerequisites

### System Requirements
- Python 3.9 or higher
- PostgreSQL 12 or higher
- Node.js 16+ (for frontend, if modifying)
- Git

### Environment Setup
1. Clone the repository (or ensure you have the existing Todo application code)
2. Install Python dependencies
3. Set up PostgreSQL database
4. Obtain API keys for required services

## Installation Steps

### 1. Environment Configuration
Create a `.env` file in your project root with the following variables:

```bash
# OpenAI API configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db

# JWT authentication
JWT_SECRET=your_jwt_secret_key

# MCP Server configuration
MCP_SERVER_URL=http://localhost:3000

# Application settings
CHAT_ENDPOINT_HOST=localhost
CHAT_ENDPOINT_PORT=8000
```

### 2. Python Dependencies Installation
```bash
pip install fastapi uvicorn openai python-multipart python-jose[cryptography] psycopg2-binary sqlalchemy pydantic
pip install mcp  # Official MCP SDK
```

### 3. Database Setup

#### 3.1. Run Existing Migrations
First, run any existing migrations for the Todo application:
```bash
# This assumes you have alembic or similar migration tool
alembic upgrade head
```

#### 3.2. Apply Chatbot-Specific Schema Changes
Add the new tables for conversations and messages:

```sql
-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id),
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    tool_calls JSONB,
    tool_responses JSONB
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_timestamp ON messages(conversation_id, timestamp ASC);
```

### 4. MCP Server Setup

#### 4.1. Create MCP Server Files
Create `mcp_server.py`:

```python
from mcp.server import Server
from mcp.shared.exceptions import McpError
import asyncio
import os
from typing import Dict, Any
import json

# Import your database connection/utils
from db_utils import get_db_connection  # Replace with your actual DB module

server = Server("todo-mcp-server")

@server.handler("todo/add_task")
async def handle_add_task(params: Dict[str, Any]):
    """Create a new task for the user"""
    try:
        user_id = params.get("user_id")
        title = params.get("title")
        description = params.get("description", "")

        if not user_id or not title:
            raise McpError("Missing required parameters: user_id and title")

        # Connect to database and add task
        task_id = await add_task_to_database(user_id, title, description)

        return {
            "task_id": task_id,
            "message": f"Task '{title}' has been added to your list"
        }
    except Exception as e:
        raise McpError(f"Failed to add task: {str(e)}")

@server.handler("todo/list_tasks")
async def handle_list_tasks(params: Dict[str, Any]):
    """Retrieve tasks for the user"""
    try:
        user_id = params.get("user_id")
        status_filter = params.get("status_filter", "all")

        if not user_id:
            raise McpError("Missing required parameter: user_id")

        tasks = await get_tasks_from_database(user_id, status_filter)

        return {"tasks": tasks}
    except Exception as e:
        raise McpError(f"Failed to list tasks: {str(e)}")

@server.handler("todo/update_task")
async def handle_update_task(params: Dict[str, Any]):
    """Update an existing task"""
    try:
        user_id = params.get("user_id")
        task_id = params.get("task_id")
        title = params.get("title")
        description = params.get("description")

        if not user_id or not task_id:
            raise McpError("Missing required parameters: user_id and task_id")

        if not title and not description:
            raise McpError("At least one of title or description must be provided")

        await update_task_in_database(user_id, task_id, title, description)

        # Get updated task title for confirmation
        updated_title = title or await get_task_title(task_id)

        return {
            "message": f"Task '{updated_title}' has been updated successfully"
        }
    except Exception as e:
        raise McpError(f"Failed to update task: {str(e)}")

@server.handler("todo/complete_task")
async def handle_complete_task(params: Dict[str, Any]):
    """Mark a task as completed"""
    try:
        user_id = params.get("user_id")
        task_id = params.get("task_id")
        completed = params.get("completed", True)

        if not user_id or not task_id:
            raise McpError("Missing required parameters: user_id and task_id")

        await update_task_completion_status(task_id, completed)

        status_text = "completed" if completed else "marked as pending"
        task_title = await get_task_title(task_id)

        return {
            "message": f"Task '{task_title}' has been {status_text}"
        }
    except Exception as e:
        raise McpError(f"Failed to update task completion: {str(e)}")

@server.handler("todo/delete_task")
async def handle_delete_task(params: Dict[str, Any]):
    """Delete a task"""
    try:
        user_id = params.get("user_id")
        task_id = params.get("task_id")

        if not user_id or not task_id:
            raise McpError("Missing required parameters: user_id and task_id")

        task_title = await get_task_title(task_id)
        await delete_task_from_database(task_id)

        return {
            "message": f"Task '{task_title}' has been deleted from your list"
        }
    except Exception as e:
        raise McpError(f"Failed to delete task: {str(e)}")

# Helper functions (implement based on your DB structure)
async def add_task_to_database(user_id: str, title: str, description: str) -> str:
    # Implementation depends on your existing DB structure
    pass

async def get_tasks_from_database(user_id: str, status_filter: str) -> list:
    # Implementation depends on your existing DB structure
    pass

async def update_task_in_database(user_id: str, task_id: str, title: str = None, description: str = None):
    # Implementation depends on your existing DB structure
    pass

async def update_task_completion_status(task_id: str, completed: bool):
    # Implementation depends on your existing DB structure
    pass

async def get_task_title(task_id: str) -> str:
    # Implementation depends on your existing DB structure
    pass

async def delete_task_from_database(task_id: str):
    # Implementation depends on your existing DB structure
    pass

if __name__ == "__main__":
    import uvicorn

    # Start the MCP server
    asyncio.run(server.run())
```

#### 4.2. Start MCP Server
```bash
python mcp_server.py
```

### 5. Chat API Server Setup

#### 5.1. Create FastAPI Application
Create `main.py`:

```python
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import jwt
from datetime import datetime
from openai import OpenAI
import os

app = FastAPI(title="AI Todo Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    action_taken: str

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# JWT verification function
def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    token_data: dict = Depends(verify_token)
):
    """
    Process natural language input and return AI-generated response
    """
    # Verify that the token user matches the requested user_id
    if token_data.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: Cannot access other user's data")

    # Create or retrieve conversation ID
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # Here you would typically:
    # 1. Store the user message in the conversation history
    # 2. Retrieve recent conversation history
    # 3. Send to OpenAI with MCP tools configured
    # 4. Process the response
    # 5. Store the AI response in the conversation history
    # 6. Return the response

    # Placeholder implementation
    response_text = f"I received your message: '{request.message}'. This is a placeholder response."

    return ChatResponse(
        response=response_text,
        conversation_id=conversation_id,
        action_taken="placeholder action"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("CHAT_ENDPOINT_HOST", "localhost"), port=int(os.getenv("CHAT_ENDPOINT_PORT", 8000)))
```

#### 5.2. Start Chat API Server
```bash
uvicorn main:app --reload
```

### 6. Frontend Integration

#### 6.1. Add Chat Interface to Existing Frontend
If your existing frontend is built with React, add a chat component:

```jsx
import { useEffect, useState, useRef } from 'react';
import { ChatKit } from '@openai/chatkit'; // Or appropriate ChatKit package

const ChatInterface = ({ userId, authToken }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Initialize ChatKit connection
    // This would connect to your backend chat API
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message to UI
    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    try {
      // Call your chat API
      const response = await fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: localStorage.getItem('conversationId') || null
        })
      });

      const data = await response.json();

      // Save conversation ID for continuity
      localStorage.setItem('conversationId', data.conversation_id);

      // Add AI response to UI
      const aiMessage = { id: Date.now() + 1, text: data.response, sender: 'ai' };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { id: Date.now() + 1, text: 'Sorry, I encountered an error. Please try again.', sender: 'system' };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-area">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask me to manage your tasks..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatInterface;
```

#### 6.2. Integrate with Existing App
Add the chat component to your existing Todo app layout, perhaps as a sidebar or separate tab.

### 7. Testing

#### 7.1. API Testing
Test the chat endpoint directly:
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token_here" \
  -d '{"message": "Add a task to buy groceries"}'
```

#### 7.2. Functional Testing
1. Start all services (database, MCP server, API server)
2. Authenticate in the frontend
3. Use the chat interface to perform task operations
4. Verify that tasks are created, updated, and managed correctly
5. Test conversation history persistence

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure JWT tokens are properly formatted and secret matches
2. **Database Connection**: Verify DATABASE_URL is correctly configured
3. **MCP Server Not Responding**: Check that MCP server is running and accessible
4. **OpenAI API Errors**: Verify OPENAI_API_KEY is valid and has sufficient quota

### Debugging Commands
```bash
# Check if services are running
netstat -tulpn | grep :8000  # API server
netstat -tulpn | grep :3000  # MCP server

# Check environment variables
printenv | grep -E "(OPENAI|DATABASE|JWT)"

# Test database connection
python -c "import psycopg2; conn = psycopg2.connect(os.getenv('DATABASE_URL')); print('DB connected')"
```

## Next Steps

1. Implement proper error handling and logging
2. Add rate limiting and security measures
3. Optimize database queries for performance
4. Implement comprehensive testing suite
5. Set up monitoring and observability