# Todo Application - Backend Specification

## 1. Overview

The Todo Application backend is a RESTful API built with FastAPI that provides authentication and task management functionality. It uses SQLModel for database interactions and JWT tokens for authentication.

## 2. Requirements

### 2.1 Functional Requirements

#### 2.1.1 Authentication
- Users must be able to register with email and password
- Users must be able to log in with email and password
- Authentication must be secured with JWT tokens
- Passwords must be hashed using bcrypt
- User sessions must be stateless using JWT

#### 2.1.2 User Management
- Users must have unique email addresses
- User profiles must include creation and update timestamps
- User data must be validated upon creation
- User accounts must be retrievable by email

#### 2.1.3 Task Management
- Users must be able to create tasks associated with their account
- Users must only be able to access their own tasks
- Tasks must have title, description, completion status, and timestamps
- Tasks must support CRUD operations
- Task completion status must be toggleable

#### 2.1.4 Data Persistence
- User and task data must be persisted in a database
- Data relationships must be properly enforced
- Database migrations must be supported
- Data integrity must be maintained

### 2.2 Non-Functional Requirements

#### 2.2.1 Performance
- API response time under 500ms for typical operations
- Support for concurrent users
- Efficient database queries
- Proper indexing for common operations

#### 2.2.2 Security
- Passwords must be securely hashed
- JWT tokens must have appropriate expiration
- Authentication required for protected endpoints
- SQL injection prevention
- Input validation to prevent attacks

#### 2.2.3 Scalability
- Stateless authentication for horizontal scaling
- Database connection pooling
- Proper resource cleanup
- Asynchronous operations where appropriate

#### 2.2.4 Reliability
- Proper error handling and logging
- Database transaction management
- Backup and recovery procedures
- Health check endpoints

## 3. Architecture

### 3.1 Technology Stack
- FastAPI (Python web framework)
- SQLModel (SQLAlchemy + Pydantic)
- PostgreSQL (primary database)
- Alembic (database migrations)
- PyJWT (JSON Web Tokens)
- Passlib (password hashing)
- Uvicorn (ASGI server)

### 3.2 Project Structure
```
backend/
├── src/
│   ├── models/          # SQLModel database models
│   │   ├── user.py     # User model
│   │   └── task.py     # Task model
│   ├── api/             # FastAPI route handlers
│   │   ├── auth.py     # Authentication endpoints
│   │   ├── tasks.py    # Task endpoints
│   │   └── deps.py     # Dependency injection
│   ├── services/        # Business logic
│   │   └── auth_service.py  # Authentication service
│   ├── database/        # Database connection and setup
│   └── utils/           # Utility functions
│       └── jwt_utils.py # JWT utilities
├── alembic/             # Database migrations
├── tests/               # Test files
├── requirements.txt     # Python dependencies
├── main.py              # Application entry point
└── .env                 # Environment variables
```

## 4. API Design

### 4.1 Authentication Endpoints
- POST `/auth/login` - Authenticate user and return JWT
- POST `/auth/register` - Register new user

### 4.2 Task Endpoints
- GET `/api/{user_id}/tasks` - Get user's tasks
- POST `/api/{user_id}/tasks` - Create new task for user
- GET `/api/{user_id}/tasks/{id}` - Get specific task
- PUT `/api/{user_id}/tasks/{id}` - Update task
- DELETE `/api/{user_id}/tasks/{id}` - Delete task
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle task completion

### 4.3 Security Headers
- Authorization: Bearer {token}
- Content-Type: application/json
- CORS headers for frontend integration

## 5. Database Schema

### 5.1 Users Table
- id (Primary Key, UUID)
- email (Unique, String)
- hashed_password (String)
- created_at (DateTime)
- updated_at (DateTime)

### 5.2 Tasks Table
- id (Primary Key, UUID)
- title (String, Not Null)
- description (String, Nullable)
- completed (Boolean, Default: False)
- user_id (Foreign Key to Users)
- created_at (DateTime)
- updated_at (DateTime)

### 5.3 Relationships
- One-to-Many: User to Tasks
- Tasks belong to a single User

## 6. Authentication Flow

### 6.1 Registration Flow
1. User sends registration request with email and password
2. System validates input
3. System hashes password
4. System creates user record
5. System returns success response

### 6.2 Login Flow
1. User sends login request with email and password
2. System verifies credentials
3. System generates JWT token
4. System returns token to user

### 6.3 Protected Endpoint Flow
1. User makes request with Authorization header
2. System validates JWT token
3. System extracts user information
4. System processes request with user context

## 7. Error Handling

### 7.1 HTTP Status Codes
- 200 OK: Successful requests
- 201 Created: Successfully created resource
- 400 Bad Request: Invalid request parameters
- 401 Unauthorized: Authentication required/failed
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Validation error
- 500 Internal Server Error: Server error

### 7.2 Error Response Format
```json
{
  "detail": "Human-readable error message"
}
```

## 8. Testing Strategy

### 8.1 Unit Tests
- Model validation tests
- Service function tests
- Utility function tests

### 8.2 Integration Tests
- API endpoint tests
- Database interaction tests
- Authentication flow tests

### 8.3 Test Coverage
- Minimum 80% code coverage
- Critical paths fully tested
- Error condition testing

## 9. Deployment

### 9.1 Environment Variables
- DATABASE_URL: Database connection string
- SECRET_KEY: JWT signing secret
- ALGORITHM: JWT algorithm
- ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time

### 9.2 Production Deployment
- ASGI server configuration
- Database migration setup
- SSL certificate configuration
- Environment-specific configurations