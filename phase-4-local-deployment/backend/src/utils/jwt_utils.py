from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from pydantic import BaseModel
import logging

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Secret key for JWT encoding/decoding
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    user_id: str
    expires_at: Optional[datetime] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with the provided data and expiration time.

    Args:
        data (dict): Data to encode in the token (typically user info)
        expires_delta (timedelta, optional): Expiration time delta

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # Add required JWT claims
    to_encode.update({
        "exp": expire,
        "sub": data.get("user_id", ""),  # Subject claim required for validation
        "iat": datetime.utcnow(),  # Issued at claim
        "iss": "todo-backend"  # Issuer claim
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify a JWT token and return the decoded data if valid.

    Args:
        token (str): JWT token to verify

    Returns:
        TokenData: Decoded token data if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        exp_timestamp = payload.get("exp")

        if user_id is None:
            logging.warning(f"JWT verification failed: Missing subject claim in token")
            return None

        # Check if token is expired
        if exp_timestamp and datetime.fromtimestamp(exp_timestamp) < datetime.utcnow():
            logging.warning(f"JWT verification failed: Token expired for user {user_id}")
            return None

        token_data = TokenData(user_id=user_id, expires_at=datetime.fromtimestamp(exp_timestamp) if exp_timestamp else None)
        return token_data
    except JWTError as e:
        logging.error(f"JWT verification failed: Invalid token format or signature - Error: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"JWT verification failed: Unexpected error during token verification - Error: {str(e)}")
        return None


def verify_jwt_token(jwt_token: str) -> Optional[TokenData]:
    """
    Verify a JWT token received from Better Auth and extract user information.

    Args:
        jwt_token (str): JWT token string from Better Auth

    Returns:
        TokenData: User information extracted from the token if valid, None if invalid
    """
    try:
        # Decode the JWT token using the shared secret
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user ID from the subject claim
        user_id: str = payload.get("sub")
        exp_timestamp = payload.get("exp")
        issuer = payload.get("iss")

        # Validate that required claims are present
        if user_id is None:
            logging.warning(f"Better Auth JWT verification failed: Missing subject claim in token")
            return None

        # Verify token is not expired
        if exp_timestamp and datetime.fromtimestamp(exp_timestamp) < datetime.utcnow():
            logging.warning(f"Better Auth JWT verification failed: Token expired for user {user_id}")
            return None

        # Create and return token data
        token_data = TokenData(
            user_id=user_id,
            expires_at=datetime.fromtimestamp(exp_timestamp) if exp_timestamp else None
        )
        return token_data

    except JWTError as e:
        # JWTError indicates the token is malformed or signature is invalid
        logging.error(f"Better Auth JWT verification failed: Invalid token format or signature - Error: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Better Auth JWT verification failed: Unexpected error during token verification - Error: {str(e)}")
        return None


def is_token_expired(token_data: TokenData) -> bool:
    """
    Check if a token is expired.

    Args:
        token_data (TokenData): Token data to check

    Returns:
        bool: True if token is expired, False otherwise
    """
    if token_data.expires_at and token_data.expires_at < datetime.utcnow():
        return True
    return False


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from a JWT token.

    Args:
        token (str): JWT token to extract user ID from

    Returns:
        str: User ID if token is valid, None otherwise
    """
    token_data = verify_jwt_token(token)
    if token_data:
        return token_data.user_id
    else:
        logging.warning(f"Failed to extract user ID from token: Token verification failed")
        return None