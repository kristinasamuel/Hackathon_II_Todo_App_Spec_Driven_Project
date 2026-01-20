import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from sqlmodel.pool import StaticPool
from datetime import datetime, timedelta
from jose import jwt

from src.main import app
from src.utils.jwt_utils import verify_jwt_token, TokenData, create_access_token
from src.services.auth_service import AuthService
import os


# Use a test secret for testing
TEST_SECRET = "test_secret_for_testing_purposes_only"
os.environ["BETTER_AUTH_SECRET"] = TEST_SECRET


@pytest.fixture(name="client")
def client_fixture():
    """Test client for the API"""
    with TestClient(app) as client:
        yield client


def test_jwt_verification_with_valid_token():
    """Test JWT verification with a valid token"""
    # Create a valid token
    data = {"sub": "test_user_123", "exp": datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(data, TEST_SECRET, algorithm="HS256")

    # Verify the token
    token_data = verify_jwt_token(token)

    assert token_data is not None
    assert token_data.user_id == "test_user_123"


def test_jwt_verification_with_invalid_signature():
    """Test JWT verification with an invalid signature"""
    # Create a token with a different secret
    wrong_secret = "wrong_secret"
    data = {"sub": "test_user_123", "exp": datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(data, wrong_secret, algorithm="HS256")

    # Verify the token (should fail)
    token_data = verify_jwt_token(token)

    assert token_data is None


def test_jwt_verification_with_expired_token():
    """Test JWT verification with an expired token"""
    # Create an expired token
    data = {"sub": "test_user_123", "exp": datetime.utcnow() - timedelta(minutes=30)}
    token = jwt.encode(data, TEST_SECRET, algorithm="HS256")

    # Verify the token (should fail)
    token_data = verify_jwt_token(token)

    assert token_data is None


def test_jwt_verification_with_missing_user_id():
    """Test JWT verification with a token missing user ID"""
    # Create a token without a subject (user ID)
    data = {"exp": datetime.utcnow() + timedelta(minutes=30)}  # No 'sub' field
    token = jwt.encode(data, TEST_SECRET, algorithm="HS256")

    # Verify the token (should fail)
    token_data = verify_jwt_token(token)

    assert token_data is None


def test_create_access_token():
    """Test creating an access token"""
    data = {"sub": "test_user_123", "email": "test@example.com"}

    token = create_access_token(data)

    # Verify the token can be decoded
    decoded_data = jwt.decode(token, TEST_SECRET, algorithms=["HS256"])
    assert decoded_data["sub"] == "test_user_123"
    assert "exp" in decoded_data


def test_auth_service_validate_token():
    """Test the auth service token validation"""
    # Create a valid token
    data = {"sub": "test_user_123", "exp": datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(data, TEST_SECRET, algorithm="HS256")

    # Mock session for auth service
    from unittest.mock import MagicMock
    mock_session = MagicMock()
    auth_service = AuthService(mock_session)

    # Validate the token
    token_data = auth_service.validate_token(token)

    assert token_data is not None
    assert token_data.user_id == "test_user_123"


def test_auth_service_get_current_user_id():
    """Test getting user ID from token using auth service"""
    # Create a valid token
    data = {"sub": "test_user_123", "exp": datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(data, TEST_SECRET, algorithm="HS256")

    # Mock session for auth service
    from unittest.mock import MagicMock
    mock_session = MagicMock()
    auth_service = AuthService(mock_session)

    # Get user ID
    user_id = auth_service.get_current_user_id(token)

    assert user_id == "test_user_123"


def test_auth_endpoint_exists(client: TestClient):
    """Test that auth endpoints exist"""
    # Test the validate endpoint with a dummy token
    # This will test if the auth endpoints are registered
    response = client.post("/auth/validate",
                          headers={"Authorization": f"Bearer dummy_token"})

    # Should return invalid token response, not 404
    assert response.status_code in [401, 200]  # Either unauthorized or valid response