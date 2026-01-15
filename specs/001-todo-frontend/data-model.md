# Data Model: Phase II Frontend - Todo Full-Stack Web Application

## Entity Definitions

### User Session
**Description**: Represents authenticated user state with associated JWT token and user identity
**Fields**:
- `user_id` (string): Unique identifier for the user
- `token` (string): JWT token for authentication
- `expires_at` (Date): Token expiration timestamp
- `is_authenticated` (boolean): Current authentication status
- `user_email` (string): User's email address
- `user_name` (string): User's display name (optional)

### Task
**Description**: Represents individual user task with title, description, completion status, and user ownership
**Fields**:
- `id` (string): Unique identifier for the task
- `title` (string): Task title (required, max 255 chars)
- `description` (string): Task description (optional, max 1000 chars)
- `completed` (boolean): Completion status (default: false)
- `created_at` (Date): Timestamp of creation
- `updated_at` (Date): Timestamp of last update
- `due_date` (Date): Optional due date
- `priority` (string): Priority level ('low', 'medium', 'high') (default: 'medium')
- `category` (string): Task category/tag (optional)
- `user_id` (string): Reference to owner user

### UI Component
**Description**: Reusable interface elements that provide consistent user experience across application
**Fields**:
- `component_id` (string): Unique identifier for the component
- `type` (string): Component type ('button', 'form', 'card', 'input', etc.)
- `props_schema` (object): JSON schema defining expected props
- `styles` (object): Styling properties and variants
- `state_dependencies` (array): List of state objects the component depends on

### Authentication State
**Description**: Manages user login/logout state and JWT token lifecycle
**Fields**:
- `status` (string): Current auth status ('idle', 'loading', 'authenticated', 'unauthenticated', 'error')
- `user` (UserSession): Associated user session data
- `error` (string): Error message if authentication failed
- `loading` (boolean): Whether auth operations are in progress
- `redirect_url` (string): URL to redirect after login (optional)

## Relationships

### User Session ↔ Task
- One-to-many relationship
- One user session can own many tasks
- Tasks are filtered by user_id to maintain user isolation

### Authentication State → User Session
- One-to-one relationship
- Authentication state manages the user session lifecycle

## State Transitions

### Task State Transitions
1. **Created**: `completed: false` → Task is initially created
2. **Updated**: Any field can be modified → Task details are changed
3. **Completed**: `completed: true` → Task completion status toggled
4. **Deleted**: Task is removed → Task no longer exists

### Authentication State Transitions
1. **Idle**: Initial state → Waiting for user action
2. **Loading**: Login/signup initiated → Processing authentication
3. **Authenticated**: Valid token received → User is logged in
4. **Unauthenticated**: Logout or invalid token → User is logged out
5. **Error**: Authentication failed → Error state with message

## Validation Rules

### Task Validation
- `title`: Required, minimum 1 character, maximum 255 characters
- `description`: Optional, maximum 1000 characters
- `priority`: Must be one of ['low', 'medium', 'high']
- `user_id`: Required, must match authenticated user
- `due_date`: If provided, must be a valid future date

### Authentication Validation
- `token`: Required for authenticated state, must be valid JWT
- `user_id`: Must match token claims
- `expires_at`: Must be in the future for valid session

## API Response Models

### Task Response
```typescript
interface TaskResponse {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  due_date?: string; // ISO date string
  priority: 'low' | 'medium' | 'high';
  category?: string;
  user_id: string;
}
```

### Auth Response
```typescript
interface AuthResponse {
  valid: boolean;
  user_id: string;
  email?: string;
  expires_at?: string;
}
```

### Error Response
```typescript
interface ErrorResponse {
  error: string;
  message: string;
  code?: string;
  details?: object;
}
```

## Frontend State Models

### Task Store
```typescript
interface TaskStore {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  filters: {
    completed?: boolean;
    priority?: 'low' | 'medium' | 'high';
    category?: string;
  };
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
}
```

### Auth Store
```typescript
interface AuthStore {
  isAuthenticated: boolean;
  user: UserSession | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}
```