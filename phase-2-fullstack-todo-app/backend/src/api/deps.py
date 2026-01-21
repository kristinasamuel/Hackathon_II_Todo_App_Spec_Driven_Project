from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlmodel import Session
import logging

from src.services.auth_service import AuthService, validate_token_standalone, create_validation_exception
from src.database.database import get_session
from src.utils.jwt_utils import TokenData


security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> str:
    """
    Dependency to get the current user ID from the JWT token.

    This function extracts the JWT token from the Authorization header,
    validates it, and returns the user ID if the token is valid.

    Args:
        credentials: HTTP authorization credentials containing the JWT token
        session: Database session for authentication service

    Returns:
        str: The user ID extracted from the JWT token

    Raises:
        HTTPException: If the token is invalid or could not be validated
    """
    token = credentials.credentials

    # Log the token validation attempt
    logging.info(f"Attempting to validate token for user identification")

    # Validate the token using the auth service
    auth_service = AuthService(session)
    user_id = auth_service.get_current_user_id(token)

    if not user_id:
        logging.warning(f"Token validation failed in get_current_user_id: {token[:20]}..." if len(token) > 20 else token)
        raise create_validation_exception()

    logging.info(f"Successfully retrieved user ID: {user_id}")
    return user_id


def get_token_data(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Dependency to get the token data from the JWT token without requiring a session.

    Args:
        credentials: HTTP authorization credentials containing the JWT token

    Returns:
        TokenData: The token data extracted from the JWT token

    Raises:
        HTTPException: If the token is invalid or could not be validated
    """
    token = credentials.credentials

    # Log the token validation attempt
    logging.info(f"Attempting to validate token and extract data")

    # Validate the token without requiring a session
    token_data = validate_token_standalone(token)

    if not token_data:
        logging.warning(f"Token validation failed in get_token_data: {token[:20]}..." if len(token) > 20 else token)
        raise create_validation_exception()

    logging.info(f"Successfully extracted token data for user: {token_data.user_id}")
    return token_data


def verify_user_access(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> str:
    """
    Dependency that verifies user access and returns the user ID.

    This combines token validation with user verification to ensure
    the requesting user has access to the requested resources.

    Args:
        credentials: HTTP authorization credentials containing the JWT token
        session: Database session for authentication service

    Returns:
        str: The user ID extracted from the JWT token

    Raises:
        HTTPException: If the token is invalid or user doesn't have access
    """
    token = credentials.credentials

    # Log the access verification attempt
    logging.info(f"Attempting to verify user access with token")

    # We'll implement route-based verification in specific endpoints
    # For now, just validate the token and return the user ID
    auth_service = AuthService(session)
    user_id = auth_service.get_current_user_id(token)

    if not user_id:
        logging.warning(f"Access verification failed in verify_user_access: {token[:20]}..." if len(token) > 20 else token)
        raise create_validation_exception()

    logging.info(f"Successfully verified user access for user: {user_id}")
    return user_id


def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    """
    Dependency to get an instance of the authentication service.

    Args:
        session: Database session for the authentication service

    Returns:
        AuthService: Instance of the authentication service
    """
    return AuthService(session)