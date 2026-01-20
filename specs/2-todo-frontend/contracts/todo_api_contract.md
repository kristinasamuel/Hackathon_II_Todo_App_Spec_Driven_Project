# Todo Application - Frontend-Backend API Contract

## Base URL
```
${NEXT_PUBLIC_API_BASE_URL}
```

## Authentication

### Login
- **Endpoint**: `POST /auth/login`
- **Request Body**:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```
- **Response**:
```json
{
  "access_token": "string (required)",
  "token_type": "string (required, value: 'bearer')"
}
```
- **Headers**:
  - `Content-Type: application/json`
- **Errors**:
  - `401 Unauthorized`: Invalid credentials

### Register
- **Endpoint**: `POST /auth/register`
- **Request Body**:
```json
{
  "email": "string (required, unique)",
  "password": "string (required, min length: 8)"
}
```
- **Response**:
```json
{
  "id": "string (required)",
  "email": "string (required)",
  "created_at": "datetime (required)",
  "updated_at": "datetime (required)"
}
```
- **Headers**:
  - `Content-Type: application/json`
- **Errors**:
  - `400 Bad Request`: Email already registered

## Tasks

### Get User Tasks
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Headers**:
  - `Authorization: Bearer {token}`
- **Path Parameters**:
  - `user_id`: string (required, user's ID)
- **Response**:
```json
[
  {
    "id": "string (required)",
    "title": "string (required)",
    "description": "string (optional)",
    "completed": "boolean (required)",
    "user_id": "string (required)",
    "created_at": "datetime (required)",
    "updated_at": "datetime (required)"
  }
]
```
- **Errors**:
  - `401 Unauthorized`: Invalid or expired token
  - `403 Forbidden`: Not authorized to access these tasks
  - `404 Not Found`: User not found

### Create Task
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Headers**:
  - `Authorization: Bearer {token}`
- **Path Parameters**:
  - `user_id`: string (required, must match authenticated user)
- **Request Body**:
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (optional, default: false)"
}
```
- **Response**:
```json
{
  "id": "string (required)",
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (required)",
  "user_id": "string (required)",
  "created_at": "datetime (required)",
  "updated_at": "datetime (required)"
}
```
- **Errors**:
  - `401 Unauthorized`: Invalid or expired token
  - `403 Forbidden`: Not authorized to create tasks for this user

### Get Task
- **Endpoint**: `GET /api/{user_id}/tasks/{id}`
- **Headers**:
  - `Authorization: Bearer {token}`
- **Path Parameters**:
  - `user_id`: string (required)
  - `id`: string (required, task ID)
- **Response**:
```json
{
  "id": "string (required)",
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (required)",
  "user_id": "string (required)",
  "created_at": "datetime (required)",
  "updated_at": "datetime (required)"
}
```
- **Errors**:
  - `401 Unauthorized`: Invalid or expired token
  - `403 Forbidden`: Not authorized to access this task
  - `404 Not Found`: Task not found

### Update Task
- **Endpoint**: `PUT /api/{user_id}/tasks/{id}`
- **Headers**:
  - `Authorization: Bearer {token}`
- **Path Parameters**:
  - `user_id`: string (required)
  - `id`: string (required, task ID)
- **Request Body**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```
- **Response**:
```json
{
  "id": "string (required)",
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (required)",
  "user_id": "string (required)",
  "created_at": "datetime (required)",
  "updated_at": "datetime (required)"
}
```
- **Errors**:
  - `401 Unauthorized`: Invalid or expired token
  - `403 Forbidden`: Not authorized to update this task
  - `404 Not Found`: Task not found

### Delete Task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{id}`
- **Headers**:
  - `Authorization: Bearer {token}`
- **Path Parameters**:
  - `user_id`: string (required)
  - `id`: string (required, task ID)
- **Response**:
```json
{
  "message": "string (required, value: 'Task deleted successfully')"
}
```
- **Errors**:
  - `401 Unauthorized`: Invalid or expired token
  - `403 Forbidden`: Not authorized to delete this task
  - `404 Not Found`: Task not found

### Toggle Task Completion
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`
- **Headers**:
  - `Authorization: Bearer {token}`
- **Path Parameters**:
  - `user_id`: string (required)
  - `id`: string (required, task ID)
- **Response**:
```json
{
  "id": "string (required)",
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (required)",
  "user_id": "string (required)",
  "created_at": "datetime (required)",
  "updated_at": "datetime (required)"
}
```
- **Errors**:
  - `401 Unauthorized`: Invalid or expired token
  - `403 Forbidden`: Not authorized to update this task
  - `404 Not Found`: Task not found

## Error Response Format

All error responses follow this format:
```json
{
  "detail": "string (descriptive error message)"
}
```

## Authentication Token Handling

- All authenticated endpoints require the `Authorization` header with a Bearer token
- Tokens should be stored in browser's localStorage under the key `access_token`
- Frontend should automatically include the token in all API requests
- If a 401 Unauthorized response is received, the token should be cleared and user redirected to login

## Rate Limiting

- API may implement rate limiting (to be confirmed)
- Recommended retry strategy: exponential backoff
- Maximum recommended retry attempts: 3

## Data Types

- `string`: UTF-8 encoded string
- `datetime`: ISO 8601 format (e.g., "2023-01-01T00:00:00.000Z")
- `boolean`: true or false
- `integer`: signed 32-bit integer
- `number`: floating-point number

## Versioning

- API versioning: Current version is v1 (included in base URL)
- Breaking changes will result in new version (e.g., v2)
- Backward compatibility maintained for 6 months after new version release