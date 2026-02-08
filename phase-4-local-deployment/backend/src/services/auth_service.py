import logging
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.models.user_model import User
from src.utils.jwt_utils import verify_jwt_token, TokenData, create_access_token
from src.database.database import get_sync_session


class AuthService:
    """
    Service class for handling authentication-related operations.
    """

    def __init__(self, session: Session):
        self.session = session

    def validate_token(self, token: str) -> Optional[TokenData]:
        """
        Validate a JWT token and return the user information if valid.

        Args:
            token (str): JWT token to validate

        Returns:
            TokenData: User information if token is valid, None otherwise
        """
        token_data = verify_jwt_token(token)
        if not token_data:
            logging.warning(f"Token validation failed for token: {token[:20]}..." if len(token) > 20 else token)
        return token_data

    def get_current_user_id(self, token: str) -> Optional[str]:
        """
        Extract the user ID from a JWT token.

        Args:
            token (str): JWT token to extract user ID from

        Returns:
            str: User ID if token is valid, None otherwise
        """
        token_data = self.validate_token(token)
        if token_data:
            return token_data.user_id
        else:
            logging.warning(f"Failed to extract user ID from token: Token validation failed")
            return None

    def verify_user_owns_resource(self, token: str, user_id_from_route: str) -> bool:
        """
        Verify that the user identified by the token owns the resource
        identified by the user_id in the route.

        Args:
            token (str): JWT token containing user information
            user_id_from_route (str): User ID from the route parameter

        Returns:
            bool: True if user owns the resource, False otherwise
        """
        current_user_id = self.get_current_user_id(token)
        if not current_user_id:
            return False

        return current_user_id == user_id_from_route

    @staticmethod
    def validate_user_exists(session: Session, user_id: str) -> bool:
        """
        Validate that a user exists in the database.

        Args:
            session: Database session
            user_id: User ID to validate

        Returns:
            bool: True if user exists, False otherwise
        """
        try:
            statement = select(User).where(User.id == user_id)
            user = session.exec(statement).first()
            return user is not None
        except Exception as e:
            logging.error(f"Error validating user exists: {str(e)}")
            return False

    def validate_and_get_user_id(self, token: str, expected_user_id: str) -> str:
        """
        Validate the token and ensure it matches the expected user ID.

        Args:
            token (str): JWT token to validate
            expected_user_id (str): Expected user ID that should match the token

        Returns:
            str: User ID if validation passes

        Raises:
            HTTPException: If token is invalid or user ID doesn't match
        """
        token_data = self.validate_token(token)

        if not token_data:
            logging.warning(f"Token validation failed in validate_and_get_user_id: {token[:20]}..." if len(token) > 20 else token)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if token_data.user_id != expected_user_id:
            logging.warning(f"User ID mismatch in validate_and_get_user_id: Expected {expected_user_id}, got {token_data.user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: User ID mismatch"
            )

        return token_data.user_id


# Standalone function for validating tokens without needing a session
def validate_token_standalone(token: str) -> Optional[TokenData]:
    """
    Validate a JWT token without requiring a database session.

    Args:
        token (str): JWT token to validate

    Returns:
        TokenData: User information if token is valid, None otherwise
    """
    return verify_jwt_token(token)


def create_validation_exception(detail: str = "Could not validate credentials"):
    """
    Create an HTTP exception for authentication failures.

    Args:
        detail (str): Detail message for the exception

    Returns:
        HTTPException: HTTP 401 Unauthorized exception
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_forbidden_exception(detail: str = "Access forbidden"):
    """
    Create an HTTP exception for authorization failures.

    Args:
        detail (str): Detail message for the exception

    Returns:
        HTTPException: HTTP 403 Forbidden exception
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail
    )


def create_default_admin_user(session: Session):
    """
    Create a default admin user if one doesn't exist.

    Args:
        session: Database session for creating the user
    """
    # Check if admin user already exists
    admin_email = "admin@example.com"

    statement = select(User).where(User.email == admin_email)
    existing_user = session.exec(statement).first()

    if not existing_user:
        # Create a default admin user
        import bcrypt
        from datetime import datetime

        # Hash the default password
        default_password = "admin123"  # In a real app, this should be more secure
        hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create user ID
        import uuid
        user_id = f"admin_{uuid.uuid4()}"

        admin_user = User(
            id=user_id,
            email=admin_email,
            password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(admin_user)
        session.commit()
        logging.info("Default admin user created successfully")
    else:
        logging.info("Admin user already exists, skipping creation")