# Claude Agent Context

## Current Project: Hackathon II - Todo Spec Driven Project

### Phase II: Full-Stack Web Application
- Technology: Next.js, FastAPI, SQLModel, Neon DB (per constitution)
- Focus: Secure, authenticated API for multi-user Todo application
- Architecture: Backend API service with JWT authentication and user isolation

### Key Technologies for Phase II
- **Backend Framework**: FastAPI (Python)
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens from Better Auth
- **Testing**: pytest

### Project Structure
```
phase-2/
├── backend/
│   ├── src/
│   │   ├── models/      # SQLModel database models
│   │   ├── api/         # FastAPI route handlers
│   │   ├── services/    # Business logic
│   │   ├── database/    # Database connection and setup
│   │   └── utils/       # Utility functions (JWT handling)
│   ├── tests/
│   ├── requirements.txt
│   └── alembic/         # Database migrations
└── frontend/            # Next.js frontend (existing)
```

### API Contract
- Base path: `/api/{user_id}`
- Authentication: JWT token in Authorization header
- User isolation: All endpoints validate user owns the requested resources
- Endpoints:
  - GET /api/{user_id}/tasks
  - POST /api/{user_id}/tasks
  - GET /api/{user_id}/tasks/{id}
  - PUT /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH /api/{user_id}/tasks/{id}/complete

### Data Models
- **Task**: id, title, description, completed, created_at, updated_at, user_id
- **User**: id (from Better Auth), email, created_at, updated_at

### Security Requirements
- JWT token validation on all endpoints
- User ownership validation for all operations
- No cross-user data access allowed
- Proper error responses (401, 403, 404) for unauthorized access
- JWT token verification using BETTER_AUTH_SECRET shared with Better Auth
- Token expiration validation to prevent use of stale tokens
- User ID extraction from JWT claims and validation against route parameters
- FastAPI dependency injection for authentication middleware
- Stateful verification disabled (stateless JWT validation only)

### Development Workflow
1. Follow Spec-Driven Development (specs first)
2. Use Claude Code for all implementations
3. Maintain phase isolation (no regression of previous phases)
4. Ensure deterministic and spec-traceable behaviors