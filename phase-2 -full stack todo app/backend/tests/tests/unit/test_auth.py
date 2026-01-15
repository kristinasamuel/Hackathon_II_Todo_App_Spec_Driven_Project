import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from sqlmodel.pool import StaticPool

from src.main import app
from src.database.database import get_session


@pytest.fixture(name="client")
def client_fixture():
    """Test client for the API"""
    with TestClient(app) as client:
        yield client


def test_auth_endpoint_exists(client: TestClient):
    """Test that auth endpoints exist"""
    # This will initially fail until we implement the auth endpoints
    pass