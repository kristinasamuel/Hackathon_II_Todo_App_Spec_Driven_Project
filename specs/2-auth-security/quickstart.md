# Quickstart Guide: Phase II Todo App Authentication & Security

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database
- Better Auth configured for frontend
- Shared secret for JWT verification

## Setup

1. **Clone the repository**
```bash
git clone <repo-url>
cd hackathon_2_Ai_todo_app
```

2. **Install dependencies**
```bash
cd phase-2/backend
pip install -r requirements.txt
# OR if using poetry
poetry install
```

3. **Environment variables**
Create a `.env` file with:
```env
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database
BETTER_AUTH_SECRET=your_shared_secret_with_better_auth
```

4. **Run database migrations**
```bash
alembic upgrade head
```

5. **Start the server**
```bash
uvicorn src.main:app --reload --port 8000
```

## Authentication Usage

### Getting a JWT Token
1. User signs in through Better Auth on the frontend
2. Better Auth issues a JWT token
3. Frontend stores and sends token with API requests

### Making Authenticated Requests
All API requests must include the JWT token in the Authorization header:
```bash
curl -H "Authorization: Bearer <jwt_token>" \
  http://localhost:8000/api/user123/tasks
```

### User Isolation
- Each user can only access their own tasks
- The user ID in the JWT must match the user ID in the route
- Attempts to access another user's data will result in 401/403 errors

## Testing Authentication

```bash
# Test valid authentication
pytest tests/unit/test_auth.py

# Test integration with task endpoints
pytest tests/integration/test_auth.py

# Run all authentication tests
pytest tests/**/test_auth.py
```

## Development

- Place authentication utilities in `src/utils/jwt_utils.py`
- Place middleware in `src/middleware/auth_middleware.py`
- Update API routes in `src/api/tasks.py` to include authentication dependencies
- Update services in `src/services/task_service.py` to enforce user ownership