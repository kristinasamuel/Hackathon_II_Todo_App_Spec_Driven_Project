# Research Summary: Phase II Todo App Authentication & Security

## Decision: JWT Token Design
**Rationale**: Using standard JWT format with required claims for user identification and security. The token will contain user ID (sub claim), expiration time, and issuer information. This follows industry best practices for stateless authentication.

**Claims structure**:
- `sub` (subject): User ID from Better Auth
- `exp` (expiration): Token expiration timestamp
- `iat` (issued at): Token creation timestamp
- `iss` (issuer): Better Auth identifier

**Alternatives considered**:
- Custom token format: More complex to implement and maintain
- Session-based tokens: Would require backend storage, violating stateless requirement

## Decision: Middleware Placement Options
**Rationale**: Implementing authentication using FastAPI dependencies rather than traditional middleware. This approach provides more granular control and integrates better with FastAPI's dependency injection system. Route guards will be implemented at the individual endpoint level for maximum flexibility.

**Trade-offs**:
- **Pros**: Better integration with FastAPI, more precise control, easier testing
- **Cons**: Need to add dependency to each protected route

**Alternative approaches**:
- Global middleware: Simpler to implement but less flexible for mixed public/protected endpoints
- Custom decorator: Could be harder to maintain and test

## Decision: Error Handling for Invalid/Missing Tokens
**Rationale**: Following HTTP standards by returning 401 Unauthorized for missing or invalid tokens. The system will provide clear error messages while avoiding information leakage about system internals.

**Error responses**:
- Missing token: 401 Unauthorized with "Not authenticated" message
- Invalid/expired token: 401 Unauthorized with "Invalid token" message
- Token-user mismatch: 401 or 403 Forbidden depending on context

**Alternatives considered**:
- Generic error responses: Less informative for debugging
- Different status codes: Could confuse frontend implementations

## Decision: Shared Secret Management
**Rationale**: Using environment variables (BETTER_AUTH_SECRET) for storing the shared secret. This follows security best practices and enables secure deployment across different environments without hardcoding secrets.

**Management approach**:
- Store secret in environment variable
- Use python-dotenv for local development
- Document secret requirements in configuration files
- Ensure secret is not logged or exposed in error messages

**Alternatives considered**:
- Hardcoded secrets: Major security vulnerability
- Configuration files: Risk of committing to version control
- External secret stores: Overly complex for this implementation level

## Decision: Better Auth Integration Pattern
**Rationale**: Implementing a verification layer that can validate JWT tokens issued by Better Auth using the shared secret. This ensures compatibility with the frontend authentication system while maintaining backend security.

**Integration approach**:
- Use python-jose for JWT verification
- Implement reusable dependency for token validation
- Validate user ID in token matches route parameter
- Support token refresh patterns if needed

**Alternatives considered**:
- Custom authentication: Would break compatibility with Better Auth
- Direct API calls to Better Auth: Would create dependency and performance issues