# Todo Backend API

This is the backend API for the Todo Full-Stack Web Application. It provides secure, authenticated endpoints for managing user tasks with proper user isolation.

## Features

- Secure JWT-based authentication with Better Auth integration
- User isolation for tasks (users can only access their own tasks)
- Full CRUD operations for tasks
- Task completion tracking
- RESTful API design
- Security headers (HSTS, X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy)
- Comprehensive error logging for authentication failures
- Token expiration validation

## Tech Stack

- FastAPI
- SQLModel
- PostgreSQL (with asyncpg)
- python-jose for JWT handling
- passlib for password hashing
- Better Auth for authentication

## Authentication Setup

### Environment Variables

1. Set up the required environment variables:

```bash
export DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
export BETTER_AUTH_SECRET=your_secure_better_auth_secret_here
```

The `BETTER_AUTH_SECRET` should be a strong, random secret key used for signing JWT tokens. Generate a secure key using:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### .env Configuration

Create a `.env` file in the backend root directory:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your_secure_better_auth_secret_here
```

## Usage Instructions

### Authentication Flow

1. **Obtain JWT Token**: Use Better Auth to authenticate users and obtain a JWT token
2. **Include Token in Requests**: Add the JWT token to the Authorization header for all API requests
3. **User-Specific Endpoints**: Access endpoints using the user ID in the URL path

### API Endpoints

#### Authentication Endpoints

- `POST /auth/validate` - Validate a JWT token and return user information
- `GET /auth/me` - Get information about the currently authenticated user
- `POST /auth/refresh` - Refresh an existing JWT token (placeholder implementation)

#### Task Endpoints (Require Authentication)

All task endpoints require a valid JWT token in the Authorization header and follow the pattern:
`/api/{user_id}/{endpoint}`

- `GET /api/{user_id}/tasks` - Get all tasks for the specified user
- `POST /api/{user_id}/tasks` - Create a new task for the specified user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task for the specified user
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task for the specified user
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task for the specified user
- `PATCH /api/{user_id}/tasks/{id}/complete` - Mark a task as complete/incomplete for the specified user

### Example API Usage

```bash
# Get user's tasks
curl -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     http://localhost:8000/api/user123/tasks

# Create a new task
curl -X POST \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Task", "description": "Task description"}' \
     http://localhost:8000/api/user123/tasks

# Update a task
curl -X PUT \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Task", "description": "Updated description"}' \
     http://localhost:8000/api/user123/tasks/1

# Mark task as complete
curl -X PATCH \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     http://localhost:8000/api/user123/tasks/1/complete
```

### Security Features

- **JWT Token Validation**: All protected endpoints validate JWT tokens using the shared secret
- **User Isolation**: Users can only access resources associated with their user ID
- **Token Expiration**: Tokens are checked for expiration before granting access
- **Security Headers**: All responses include security headers to prevent common attacks
- **Error Logging**: Authentication failures are logged for security monitoring

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (see Authentication Setup section)

3. Run the application:
```bash
uvicorn src.main:app --reload --port 8000
```

## API Documentation

The API documentation is available at `/docs` when the application is running.

## Testing

Run the tests with pytest:
```bash
pytest
```

Run specific test modules:
```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run specific test file
pytest tests/unit/test_auth.py
```

## Project Structure

```
backend/
├── src/
│   ├── models/          # SQLModel database models
│   ├── api/             # FastAPI route handlers
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── tasks.py     # Task endpoints
│   │   └── deps.py      # Authentication dependencies
│   ├── services/        # Business logic
│   │   └── auth_service.py  # Authentication service
│   ├── database/        # Database connection and setup
│   └── utils/           # Utility functions (JWT handling)
│       └── jwt_utils.py # JWT utilities and token validation
├── tests/
│   ├── unit/            # Unit tests
│   │   └── test_auth.py # Authentication unit tests
│   └── integration/     # Integration tests
│       └── test_auth.py # Authentication integration tests
├── requirements.txt
├── pyproject.toml
└── alembic/             # Database migrations
```