from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from src.utils.jwt_utils import verify_jwt_token
from src.services.auth_service import validate_token_standalone, create_validation_exception


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware to validate JWT tokens on incoming requests.

    This middleware intercepts requests and validates JWT tokens before
    they reach the application endpoints. It's designed to be stateless
    and not interfere with public endpoints.
    """

    def __init__(self, app, public_paths: Optional[list] = None):
        """
        Initialize the authentication middleware.

        Args:
            app: The FastAPI application instance
            public_paths: List of paths that don't require authentication
        """
        super().__init__(app)
        self.public_paths = public_paths or [
            "/docs", "/redoc", "/openapi.json",  # Documentation endpoints
            "/health", "/ping",  # Health check endpoints
            "/",  # Root endpoint
        ]

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Process the incoming request and validate authentication if required.

        Args:
            request: The incoming request
            call_next: The next middleware/endoint in the chain

        Returns:
            Response: The response from the next handler
        """
        # Check if the path is public and skip authentication
        if self._is_public_path(request.url.path):
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            # For protected paths, require authentication
            if not self._is_protected_path(request.url.path):
                return await call_next(request)

            # Return 401 if no auth header is provided
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"}
            )

        # Validate the token format (should be "Bearer <token>")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication scheme"}
            )

        # Extract the token
        token = auth_header[len("Bearer "):]

        # Validate the JWT token
        token_data = validate_token_standalone(token)

        if not token_data:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired token"}
            )

        # Add the user ID to the request state for use in endpoints
        request.state.user_id = token_data.user_id

        # Continue with the request
        response = await call_next(request)
        return response

    def _is_public_path(self, path: str) -> bool:
        """
        Check if the given path is public and doesn't require authentication.

        Args:
            path: The request path to check

        Returns:
            bool: True if the path is public, False otherwise
        """
        for public_path in self.public_paths:
            if path.startswith(public_path):
                return True
        return False

    def _is_protected_path(self, path: str) -> bool:
        """
        Check if the given path requires authentication.

        Args:
            path: The request path to check

        Returns:
            bool: True if the path is protected, False otherwise
        """
        # All API paths under /api should be protected
        return path.startswith("/api/")


# Alternative implementation as a decorator-style function
async def validate_authentication(request: Request) -> str:
    """
    Validate authentication for a request and return the user ID.

    Args:
        request: The incoming request

    Returns:
        str: The authenticated user ID

    Raises:
        HTTPException: If authentication fails
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise create_validation_exception("Missing or invalid Authorization header")

    token = auth_header[len("Bearer "):]
    token_data = validate_token_standalone(token)

    if not token_data:
        raise create_validation_exception("Invalid or expired token")

    return token_data.user_id