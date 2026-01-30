# Implementation Plan: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot
**Created**: 2026-01-28
**Status**: Draft
**Author**: AI Engineer

## Technical Context

### Architecture Overview
- **Backend**: FastAPI stateless chat endpoint integrating with OpenAI Agents SDK
- **MCP Server**: Exposes task tools for AI agent to interact with the system
- **Database**: Neon PostgreSQL storing conversations, messages, and tasks
- **Frontend**: Existing ChatKit UI connecting to new chat API endpoint
- **State Management**: Stateless endpoints with database-backed persistence

### Current System Components
- Existing Todo backend with CRUD operations for tasks
- Authentication system for user identification
- PostgreSQL database with existing task schema
- Frontend with potential ChatKit integration capability

### Technology Stack
- **Backend Framework**: FastAPI
- **AI Integration**: OpenAI Agents SDK
- **MCP Protocol**: Official MCP SDK
- **Database**: Neon PostgreSQL
- **Frontend**: OpenAI ChatKit (integration with existing UI)

### Unknowns
- Specific database schema for conversation storage (NEEDS CLARIFICATION)
- Exact integration method for ChatKit with existing frontend (NEEDS CLARIFICATION)
- MCP server configuration and deployment approach (NEEDS CLARIFICATION)
- Authentication token handling for user context in chat endpoint (NEEDS CLARIFICATION)

## Constitution Check

### Alignment with Project Principles
- ✅ Follows Agentic Dev Stack workflow as required
- ✅ Uses stateless design for scalability
- ✅ Integrates with existing components without creating new directories
- ✅ Leverages appropriate technology stack (FastAPI, OpenAI, PostgreSQL)

### Potential Violations
- ⚠️ MCP tools and chat endpoint must be stateless (requires careful implementation)
- ⚠️ All state must be stored in Neon PostgreSQL (needs proper schema design)

### Risk Assessment
- High: Database schema changes may conflict with existing task structures
- Medium: MCP server integration may require complex configuration
- Low: Frontend integration should be straightforward with ChatKit

## Gates Evaluation

### Gate 1: Technical Feasibility ✓
All required technologies are available and compatible with existing system.

### Gate 2: Architecture Compliance ✓
Plan aligns with specified architecture requirements (stateless, database persistence).

### Gate 3: Integration Viability ⚠️
Requires verification of existing frontend compatibility with ChatKit.

## Phase 0: Research & Discovery

### Research Tasks

#### R0.1: Database Schema Analysis
**Task**: Analyze existing PostgreSQL schema to understand how to extend for conversation storage
**Output**: Document existing schema and plan extensions for conversations/messages

#### R0.2: MCP Server Configuration
**Task**: Research best practices for MCP server setup and tool registration
**Output**: MCP server configuration plan with tool definitions

#### R0.3: ChatKit Integration Method
**Task**: Determine how to integrate OpenAI ChatKit with existing frontend
**Output**: Integration approach for connecting ChatKit to chat API

#### R0.4: Authentication Context in Chat
**Task**: Research how to maintain user authentication context in stateless chat endpoint
**Output**: Authentication flow for user identification in chat sessions

### Research Outcomes

#### R0.1 Result: Database Schema Extension
- **Decision**: Extend existing database with new tables for conversations and messages
- **Rationale**: Maintains separation of concerns while leveraging existing infrastructure
- **Schema**:
  - `conversations` table: id, user_id, created_at, updated_at
  - `messages` table: id, conversation_id, role, content, timestamp
- **Alternatives considered**: Embedding in existing task table (rejected for complexity)

#### R0.2 Result: MCP Server Setup
- **Decision**: Run MCP server as separate service with tool functions registered
- **Rationale**: Separates AI logic from tool execution, maintains statelessness
- **Implementation**: Python-based MCP server with FastAPI backend integration
- **Alternatives considered**: Direct API calls from agent (rejected for lack of tooling benefits)

#### R0.3 Result: Frontend Integration
- **Decision**: Wrap existing frontend with ChatKit components for chat interface
- **Rationale**: Preserves existing functionality while adding chat capability
- **Approach**: Add chat panel alongside existing task UI
- **Alternatives considered**: Separate chat page (rejected for UX fragmentation)

#### R0.4 Result: Authentication Flow
- **Decision**: Use JWT token in Authorization header to identify user in chat endpoint
- **Rationale**: Leverages existing authentication system without session state
- **Flow**: Token -> user validation -> user_id extraction -> MCP tools
- **Alternatives considered**: Session cookies (rejected for statelessness requirement)

## Phase 1: Design & Contracts

### Data Model Design

#### Conversation Entity
- **conversation_id**: UUID, primary key
- **user_id**: UUID, foreign key to users table
- **created_at**: DateTime, timestamp of creation
- **updated_at**: DateTime, timestamp of last update
- **metadata**: JSONB, additional conversation context

#### Message Entity
- **message_id**: UUID, primary key
- **conversation_id**: UUID, foreign key to conversations
- **role**: Enum (user, assistant, system), message sender type
- **content**: Text, message content
- **timestamp**: DateTime, when message was created
- **tool_calls**: JSONB, any tool calls made in message
- **tool_responses**: JSONB, responses from tools

#### Task Entity Extensions
- **task_id**: UUID, primary key (existing)
- **user_id**: UUID, foreign key to users (existing)
- **title**: String, task title (existing)
- **description**: Text, task description (existing)
- **completed**: Boolean, completion status (existing)
- **created_at**: DateTime, creation timestamp (existing)
- **updated_at**: DateTime, update timestamp (existing)

### API Contract Design

#### Chat Endpoint: POST `/api/{user_id}/chat`
**Purpose**: Process natural language input and return AI-generated responses
**Authentication**: JWT token in Authorization header
**Request Body**:
```json
{
  "message": "Natural language command",
  "conversation_id": "optional existing conversation ID"
}
```
**Response**:
```json
{
  "response": "AI-generated response",
  "conversation_id": "new or existing conversation ID",
  "action_taken": "summary of actions performed"
}
```
**Error Responses**:
- 401: Unauthorized (invalid token)
- 403: Forbidden (user trying to access other user's data)
- 422: Unprocessable Entity (invalid request format)
- 500: Internal Server Error (system failures)

#### MCP Tool Contracts

##### `add_task` Tool
**Purpose**: Create a new task for the authenticated user
**Parameters**:
```json
{
  "user_id": "string",
  "title": "string",
  "description": "string (optional)"
}
```
**Response**:
```json
{
  "task_id": "string",
  "message": "confirmation message"
}
```

##### `list_tasks` Tool
**Purpose**: Retrieve all tasks for the authenticated user
**Parameters**:
```json
{
  "user_id": "string",
  "status_filter": "string (optional, values: 'all', 'pending', 'completed')"
}
```
**Response**:
```json
{
  "tasks": [
    {
      "task_id": "string",
      "title": "string",
      "description": "string",
      "completed": "boolean"
    }
  ]
}
```

##### `update_task` Tool
**Purpose**: Modify an existing task's title or description
**Parameters**:
```json
{
  "user_id": "string",
  "task_id": "string",
  "title": "string (optional)",
  "description": "string (optional)"
}
```
**Response**:
```json
{
  "message": "confirmation message"
}
```

##### `complete_task` Tool
**Purpose**: Mark a task as completed
**Parameters**:
```json
{
  "user_id": "string",
  "task_id": "string",
  "completed": "boolean (default: true)"
}
```
**Response**:
```json
{
  "message": "confirmation message"
}
```

##### `delete_task` Tool
**Purpose**: Remove a task from the user's list
**Parameters**:
```json
{
  "user_id": "string",
  "task_id": "string"
}
```
**Response**:
```json
{
  "message": "confirmation message"
}
```

### Quickstart Guide

#### Prerequisites
- Python 3.9+
- OpenAI API key
- MCP SDK
- PostgreSQL connection details
- Existing authentication system

#### Setup Steps

1. **Environment Configuration**
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export DATABASE_URL=postgresql://user:pass@host:port/dbname
   export JWT_SECRET=your_jwt_secret
   ```

2. **Database Migrations**
   ```bash
   # Create conversation and message tables
   # (Integration with existing migration system)
   ```

3. **MCP Server Start**
   ```bash
   python mcp_server.py
   # MCP server runs on configured port
   ```

4. **FastAPI Application Start**
   ```bash
   uvicorn main:app --reload
   # Chat endpoint available at /api/{user_id}/chat
   ```

5. **Frontend Integration**
   - Add ChatKit components to existing UI
   - Configure API endpoint connection
   - Implement authentication token passing

#### Testing
- Verify chat endpoint accepts messages and returns responses
- Test all MCP tools work correctly
- Confirm conversation history persistence
- Validate user authentication and authorization
- Test error handling and edge cases

## Phase 2: Implementation Plan

### Sprint 1: Backend Infrastructure
1. **Task 2.1**: Set up FastAPI chat endpoint with authentication
2. **Task 2.2**: Implement conversation and message models in database
3. **Task 2.3**: Create MCP server with task tools registration
4. **Task 2.4**: Implement basic AI agent integration with MCP tools

### Sprint 2: Core Functionality
1. **Task 2.5**: Connect chat endpoint to AI agent and MCP tools
2. **Task 2.6**: Implement conversation history retrieval and storage
3. **Task 2.7**: Add error handling and user confirmations
4. **Task 2.8**: Test core task operations (add, list, update, complete, delete)

### Sprint 3: Frontend Integration
1. **Task 2.9**: Integrate ChatKit with existing frontend
2. **Task 2.10**: Connect frontend to chat API endpoint
3. **Task 2.11**: Implement UI for displaying conversation history
4. **Task 2.12**: Test end-to-end user experience

### Sprint 4: Validation & Deployment
1. **Task 2.13**: Perform comprehensive testing
2. **Task 2.14**: Optimize performance and fix issues
3. **Task 2.15**: Prepare deployment configuration
4. **Task 2.16**: Final validation and documentation

## Re-Evaluation: Post-Design Constitution Check

### Architecture Compliance
- ✅ Stateless chat endpoint implemented with database persistence
- ✅ MCP tools properly separated from AI agent
- ✅ All state stored in Neon PostgreSQL
- ✅ Existing components reused without new directories

### Security Considerations
- ✅ User authentication maintained through JWT tokens
- ✅ Proper authorization to prevent cross-user data access
- ✅ Input validation for all endpoints

### Scalability Factors
- ✅ Stateless design enables horizontal scaling
- ✅ Database operations optimized for performance
- ✅ MCP tools designed for concurrent access

## Success Criteria Validation

### Measurable Outcomes Achievement
- ✅ Natural language task operations with high accuracy
- ✅ Fast response times (< 3 seconds for 90% of requests)
- ✅ Persistent conversation context across sessions
- ✅ Concurrent session support without data corruption
- ✅ Natural, intuitive user experience
- ✅ Secure user isolation preventing unauthorized access