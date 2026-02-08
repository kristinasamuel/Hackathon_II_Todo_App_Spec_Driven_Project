import pytest
from sqlmodel import create_engine, Session
from sqlmodel.pool import StaticPool
from src.main import app  # Adjust import based on your app structure
from src.database.database import sync_engine
from contextlib import contextmanager
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker


@pytest.fixture(name="test_client")
def test_client_fixture():
    """
    Create a test client for the FastAPI app
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(name="session")
def session_fixture():
    """
    Create an in-memory database session for testing
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Create tables
    # SQLModel.metadata.create_all(engine)  # Uncomment when SQLModel is properly imported

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()