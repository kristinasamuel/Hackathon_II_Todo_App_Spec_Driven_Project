# Quickstart Guide: Phase II Todo Backend

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database
- Better Auth configured for frontend

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
BETTER_AUTH_SECRET=your_better_auth_secret
```

4. **Run database migrations**
```bash
alembic upgrade head
```

5. **Start the server**
```bash
uvicorn src.main:app --reload --port 8000
```

## API Usage

### Authentication
All API endpoints require a valid JWT token from Better Auth in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Example Requests

**Get user's tasks**:
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/user123/tasks
```

**Create a new task**:
```bash
curl -X POST -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "New task", "description": "Task description"}' \
  http://localhost:8000/api/user123/tasks
```

## Running Tests

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests
pytest
```

## Development

- Place models in `src/models/`
- Place API routes in `src/api/`
- Place business logic in `src/services/`
- Place utility functions in `src/utils/`