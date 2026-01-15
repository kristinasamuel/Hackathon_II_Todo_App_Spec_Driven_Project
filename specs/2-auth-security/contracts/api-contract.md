# API Contract: Authentication & Security for Todo Backend API

## Overview
Secure API for managing user tasks with authentication and user isolation using JWT tokens issued by Better Auth.

## Authentication Requirements
All endpoints require a valid JWT token in the Authorization header:
`Authorization: Bearer <jwt_token>`

## Endpoint Security Patterns

### Protected Endpoints (require authentication)
All existing task endpoints will be enhanced with authentication:
- GET /api/{user_id}/tasks
- POST /api/{user_id}/tasks
- GET /api/{user_id}/tasks/{id}
- PUT /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH /api/{user_id}/tasks/{id}/complete

### Authentication Validation
For each protected endpoint:
1. Verify JWT token is present in Authorization header
2. Validate JWT signature using BETTER_AUTH_SECRET
3. Confirm token is not expired
4. Extract user_id from JWT token
5. Verify route user_id matches JWT user_id
6. Proceed with original operation if all validations pass

## Authentication-Specific Endpoints
(These would be handled by Better Auth on frontend, but documented for completeness)

### Token Validation Endpoint
**POST /auth/validate**
**Description**: Validates a JWT token and returns user information
**Authentication**: Required (JWT token in header)
**Request Body**:
```json
{
  "token": "jwt_token_string"
}
```
**Response**:
- 200: Valid token with user info
```json
{
  "valid": true,
  "user_id": "user123",
  "expires_at": "2023-12-31T23:59:59Z"
}
```
- 401: Invalid token
```json
{
  "valid": false,
  "error": "Invalid token"
}
```

## Error Responses
Standard error response format for authentication failures:
```json
{
  "detail": "Error message"
}
```

### Authentication Error Codes
- 401 Unauthorized: Missing or invalid JWT token
- 403 Forbidden: Valid token but user ID mismatch with route
- 422 Unprocessable Entity: Malformed request related to authentication

## Security Headers
All responses will include security headers:
- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options