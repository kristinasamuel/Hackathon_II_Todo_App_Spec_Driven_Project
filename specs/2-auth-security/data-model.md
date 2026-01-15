# Data Model: Phase II Todo App Authentication & Security

## JWT Token Entity

**Fields**:
- `token`: String, JWT token string received from Better Auth
- `user_id`: String, User identifier from Better Auth (extracted from JWT)
- `expires_at`: DateTime, Token expiration time (extracted from JWT)
- `issued_at`: DateTime, Token issue time (extracted from JWT)
- `is_valid`: Boolean, Validation status after verification

**Validation rules**:
- Token must be properly formatted JWT
- User ID must match the authenticated user in the route
- Token must not be expired
- Token signature must be valid using shared secret

## Authorization Context Entity

**Fields**:
- `authenticated_user_id`: String, User ID from verified JWT token
- `permissions`: List, User permissions (currently read/write for owned tasks)
- `valid_from`: DateTime, When context was created
- `valid_until`: DateTime, When context expires (matches token expiration)

**Validation rules**:
- Context is only valid if associated JWT token is valid
- User ID in context must match route parameter for operations
- Permissions are limited to operations on user's own tasks

## Authentication Result Entity

**Fields**:
- `is_authenticated`: Boolean, Whether authentication was successful
- `user_id`: String, Authenticated user ID (if successful)
- `error_message`: String, Error message (if failed)
- `status_code`: Integer, HTTP status code to return

**Validation rules**:
- Either is_authenticated is true OR error_message is populated
- User ID is only populated if authentication was successful
- Status code corresponds to authentication outcome