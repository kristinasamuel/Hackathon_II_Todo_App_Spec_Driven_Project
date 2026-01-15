# Data Model: Phase II Todo Backend

## Task Entity

**Fields**:
- `id`: UUID/GUID, Primary Key, Auto-generated
- `title`: String, Required, Max length 255
- `description`: String, Optional, Max length 1000
- `completed`: Boolean, Default False
- `created_at`: DateTime, Auto-generated, UTC
- `updated_at`: DateTime, Auto-generated and updated, UTC
- `user_id`: String/UUID, Foreign Key to User, Required for ownership validation

**Relationships**:
- Many-to-One: Task belongs to one User
- User has many Tasks

**Validation rules**:
- Title must not be empty
- User ID must match authenticated user for operations
- Cannot modify another user's task

## User Entity

**Fields**:
- `id`: String/UUID, Primary Key from Better Auth, Required
- `email`: String, Unique, Required
- `created_at`: DateTime, Auto-generated, UTC
- `updated_at`: DateTime, Auto-generated and updated, UTC

**Relationships**:
- One-to-Many: User has many Tasks
- Tasks belong to one User

**Validation rules**:
- User ID comes from Better Auth JWT token
- Email must be valid format
- User must exist in Better Auth system