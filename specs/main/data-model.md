# Data Model: TaskManager Pro - Phase II Frontend

## Frontend Data Models

### User Entity
- **Fields**:
  - email: string (required, unique)
  - password: string (required, during registration/login)
- **Validations**:
  - Email format validation
  - Password strength requirements (min 6 characters)
- **Relationships**: N/A (managed by backend)

### Task Entity
- **Fields**:
  - id: string (required, unique identifier from backend)
  - title: string (required, task title)
  - description: string (optional, task description)
  - completed: boolean (required, completion status)
  - user_id: string (required, owner of the task)
  - created_at: datetime (required, creation timestamp)
  - updated_at: datetime (required, last update timestamp)
- **Validations**:
  - Title must not be empty
  - Length limits for description
- **State Transitions**:
  - Active ↔ Completed (toggle operation)

### JWT Token Entity
- **Fields**:
  - token: string (required, JWT token string)
  - expiration_time: datetime (required, token expiration)
- **Validations**:
  - Token format validation (proper JWT structure)
  - Expiration check
- **Relationships**: Associated with a user session

## Component State Models

### Form State
- **Login Form**:
  - email: string
  - password: string
  - loading: boolean
  - error: string
- **Signup Form**:
  - email: string
  - password: string
  - confirmPassword: string
  - loading: boolean
  - error: string

### Task Form State
- **Task Creation Form**:
  - title: string
  - description: string
  - loading: boolean
  - error: string
- **Task Edit Form**:
  - id: string
  - title: string
  - description: string
  - loading: boolean
  - error: string

### Application State
- **Authentication State**:
  - isAuthenticated: boolean
  - currentUser: User | null
  - loading: boolean
- **Task State**:
  - tasks: Task[]
  - loading: boolean
  - error: string
  - currentFilter: "all" | "active" | "completed"

## API Response Models

### Authentication Response
- **Login Response**:
  - access_token: string (JWT token)
  - token_type: string (always "bearer")
- **Signup Response**:
  - id: string (user ID)
  - email: string (user email)
  - created_at: datetime
  - updated_at: datetime

### Task Response
- **Single Task Response**:
  - id: string
  - title: string
  - description: string | null
  - completed: boolean
  - user_id: string
  - created_at: datetime
  - updated_at: datetime
- **Multiple Tasks Response**: Array of Single Task Response

### Error Response
- **Standard Error Format**:
  - detail: string (human-readable error message)

## Validation Rules

### Input Validation
- Email: Must match standard email format
- Password: Minimum 6 characters
- Task Title: Required, maximum 255 characters
- Task Description: Optional, maximum 1000 characters

### Business Logic Validation
- Users can only modify their own tasks
- Completed tasks can be marked as incomplete
- Task deletion requires confirmation
- Duplicate task titles allowed

## UI State Models

### Loading States
- **Global Loading**: Show spinner when API request in progress
- **Component Loading**: Specific component loading states
- **Empty States**: Display appropriate messaging when no tasks exist

### Error States
- **Form Errors**: Inline validation messages
- **API Errors**: Toast notifications or banner messages
- **Network Errors**: Offline indicators and retry mechanisms

### Success States
- **Action Confirmations**: Toast notifications for successful operations
- **Transitional States**: Immediate UI updates with optimistic updates