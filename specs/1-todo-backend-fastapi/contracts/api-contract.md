# API Contract: Todo Backend API

## Overview
RESTful API for managing user tasks with authentication and user isolation.

## Base Path
`/api/{user_id}`

## Endpoints

### GET /api/{user_id}/tasks
**Description**: Retrieve all tasks for the specified user
**Authentication**: Required (JWT token)
**Parameters**:
- `user_id` (path): User identifier from Better Auth
**Response**:
- 200: Array of Task objects
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (user_id doesn't match token)

### POST /api/{user_id}/tasks
**Description**: Create a new task for the specified user
**Authentication**: Required (JWT token)
**Parameters**:
- `user_id` (path): User identifier from Better Auth
**Request Body**:
```json
{
  "title": "string",
  "description": "string (optional)",
  "completed": "boolean (default: false)"
}
```
**Response**:
- 201: Created Task object
- 400: Invalid request body
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (user_id doesn't match token)

### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific task for the specified user
**Authentication**: Required (JWT token)
**Parameters**:
- `user_id` (path): User identifier from Better Auth
- `id` (path): Task identifier
**Response**:
- 200: Task object
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (user_id doesn't match token or task doesn't belong to user)
- 404: Task not found

### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task for the specified user
**Authentication**: Required (JWT token)
**Parameters**:
- `user_id` (path): User identifier from Better Auth
- `id` (path): Task identifier
**Request Body**:
```json
{
  "title": "string",
  "description": "string (optional)",
  "completed": "boolean"
}
```
**Response**:
- 200: Updated Task object
- 400: Invalid request body
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (user_id doesn't match token or task doesn't belong to user)
- 404: Task not found

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task for the specified user
**Authentication**: Required (JWT token)
**Parameters**:
- `user_id` (path): User identifier from Better Auth
- `id` (path): Task identifier
**Response**:
- 204: Successfully deleted
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (user_id doesn't match token or task doesn't belong to user)
- 404: Task not found

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle the completion status of a specific task for the specified user
**Authentication**: Required (JWT token)
**Parameters**:
- `user_id` (path): User identifier from Better Auth
- `id` (path): Task identifier
**Request Body**:
```json
{
  "completed": "boolean"
}
```
**Response**:
- 200: Updated Task object
- 400: Invalid request body
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (user_id doesn't match token or task doesn't belong to user)
- 404: Task not found

## Authentication
All endpoints require a valid JWT token in the Authorization header:
`Authorization: Bearer {jwt_token}`

## Error Responses
Standard error response format:
```json
{
  "detail": "Error message"
}
```