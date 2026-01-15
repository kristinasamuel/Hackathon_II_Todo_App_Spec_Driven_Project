from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request  # Added for rate limiter
from typing import Dict, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime
from sqlmodel import Session, select
from pydantic import BaseModel
import bcrypt
from ..utils.jwt_utils import verify_jwt_token, TokenData, create_access_token
from ..services.auth_service import validate_token_standalone, create_validation_exception
from ..database.database import get_sync_session
from ..models.user_model import User, UserCreate

# Pydantic models for request/response
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    refresh_token: Optional[str] = None
    user: Dict[str, str]

class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class SignupResponse(BaseModel):
    token: str
    refresh_token: Optional[str] = None
    user: Dict[str, str]

# Initialize rate limiter for auth endpoints
limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/auth", tags=["auth"])

security = HTTPBearer()

@router.post("/login",
             summary="User Login",
             description="Authenticate user and return JWT token.")
@limiter.limit("10/minute")  # Limit to 10 login attempts per minute per IP
async def login_user(request: Request, login_request: LoginRequest, session: Session = Depends(get_sync_session)):
    """
    Authenticate user and return JWT token.

    Args:
        request: FastAPI request object (required for rate limiting)
        login_request: Login credentials (email and password)
        session: Database session

    Returns:
        dict: JWT token and user information
    """
    # Find user by email
    statement = select(User).where(User.email == login_request.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password using bcrypt
    if not bcrypt.checkpw(login_request.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create JWT token
    token_data = {
        "user_id": user.id,
        "email": user.email
    }
    access_token = create_access_token(data=token_data)

    return {
        "token": access_token,
        "refresh_token": None,  # Placeholder
        "user": {
            "user_id": user.id,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
    }


@router.post("/signup",
             summary="User Signup",
             description="Create a new user account and return JWT token.")
@limiter.limit("5/hour")  # Limit to 5 signup attempts per hour per IP
async def signup_user(request: Request, signup_request: SignupRequest, session: Session = Depends(get_sync_session)):
    """
    Create a new user account and return JWT token.

    Args:
        request: FastAPI request object (required for rate limiting)
        signup_request: Signup data (email, password, name)
        session: Database session

    Returns:
        dict: JWT token and user information
    """
    # Check if user already exists
    statement = select(User).where(User.email == signup_request.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Hash the password (using bcrypt)
    hashed_password = bcrypt.hashpw(signup_request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Generate a unique ID
    user_id = f"user_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{abs(hash(signup_request.email)) % 10000}"

    # Create new user with hashed password
    user = User(
        id=user_id,
        email=signup_request.email,
        password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create JWT token
    token_data = {
        "user_id": user.id,
        "email": user.email
    }
    access_token = create_access_token(data=token_data)

    return {
        "token": access_token,
        "refresh_token": None,  # Placeholder
        "user": {
            "user_id": user.id,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
    }


@router.post("/validate",
             summary="Validate JWT Token",
             description="Validate a JWT token and return user information if valid.")
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def validate_token_endpoint(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Validate a JWT token and return user information.

    Args:
        request: FastAPI request object (required for rate limiting)
        credentials: HTTP authorization credentials containing the JWT token

    Returns:
        dict: Validation result with user information if token is valid
    """
    token = credentials.credentials

    # Validate the token
    token_data = validate_token_standalone(token)

    if not token_data:
        return {
            "valid": False,
            "error": "Invalid token"
        }

    # Return token information
    return {
        "valid": True,
        "user_id": token_data.user_id,
        "expires_at": token_data.expires_at.isoformat() if token_data.expires_at else None
    }


@router.get("/me",
            summary="Get Current User",
            description="Get information about the currently authenticated user.")
@limiter.limit("30/minute")  # Limit to 30 requests per minute per IP
async def get_current_user_endpoint(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get information about the currently authenticated user.

    Args:
        request: FastAPI request object (required for rate limiting)
        credentials: HTTP authorization credentials containing the JWT token

    Returns:
        dict: Information about the authenticated user
    """
    token = credentials.credentials

    # Validate the token
    token_data = validate_token_standalone(token)

    if not token_data:
        raise create_validation_exception("Could not validate credentials")

    return {
        "user_id": token_data.user_id,
        "expires_at": token_data.expires_at.isoformat() if token_data.expires_at else None
    }


@router.post("/refresh",
             summary="Refresh JWT Token",
             description="Refresh an existing JWT token.")
@limiter.limit("5/minute")  # Limit to 5 refresh requests per minute per IP
async def refresh_token_endpoint(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_sync_session)
):
    """
    Refresh an existing JWT token.

    Args:
        request: FastAPI request object (required for rate limiting)
        credentials: HTTP authorization credentials containing the refresh token

    Returns:
        dict: New access token
    """
    token = credentials.credentials

    # In this implementation, we'll treat the refresh token similarly to the access token
    # In a production system, you'd have separate refresh token handling
    try:
        # Validate the refresh token
        token_data = validate_token_standalone(token)

        if not token_data:
            raise create_validation_exception("Invalid refresh token")

        # Get user from database to ensure they still exist
        user = session.get(User, token_data.user_id)
        if not user:
            raise create_validation_exception("User no longer exists")

        # Create a new access token
        new_token_data = {
            "user_id": user.id,
            "email": user.email
        }
        new_access_token = create_access_token(data=new_token_data)

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise create_validation_exception("Invalid refresh token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, str]:
    """
    Get the current user from the JWT token in the Authorization header
    """
    token = credentials.credentials

    token_data = validate_token_standalone(token)
    if token_data is None:
        raise create_validation_exception("Could not validate credentials")

    # Return user information
    return {
        "user_id": token_data.user_id,
        "token": token
    }


def get_user_id_from_header(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Extract only the user ID from the token in the Authorization header
    """
    token = credentials.credentials
    token_data = validate_token_standalone(token)

    if token_data is None:
        raise create_validation_exception("Could not validate credentials")

    return token_data.user_id