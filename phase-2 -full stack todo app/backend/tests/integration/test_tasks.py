import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.database import get_sync_session
from unittest.mock import patch
from src.models.task_model import TaskRead


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI app
    """
    with TestClient(app) as test_client:
        yield test_client


def test_get_tasks_endpoint(client: TestClient):
    """
    Test the GET /api/{user_id}/tasks endpoint
    """
    # Mock the JWT token validation
    with patch("src.api.auth.get_user_id_from_header", return_value="user123"):
        response = client.get("/api/user123/tasks")

        # Should return a list (even if empty)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_create_task_endpoint(client: TestClient):
    """
    Test the POST /api/{user_id}/tasks endpoint
    """
    # Mock the JWT token validation
    with patch("src.api.auth.get_user_id_from_header", return_value="user123"):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "user_id": "user123"
        }
        response = client.post("/api/user123/tasks", json=task_data)

        # Should return the created task
        assert response.status_code == 201
        assert response.json()["title"] == "Test Task"
        assert response.json()["user_id"] == "user123"


def test_get_specific_task_endpoint(client: TestClient):
    """
    Test the GET /api/{user_id}/tasks/{task_id} endpoint
    """
    # This test requires an existing task, so we'll test the error case
    # Mock the JWT token validation
    with patch("src.api.auth.get_user_id_from_header", return_value="user123"):
        response = client.get("/api/user123/tasks/nonexistent-task-id")

        # Should return 404 for non-existent task
        assert response.status_code == 404


def test_update_task_endpoint(client: TestClient):
    """
    Test the PUT /api/{user_id}/tasks/{task_id} endpoint
    """
    # Mock the JWT token validation
    with patch("src.api.auth.get_user_id_from_header", return_value="user123"):
        update_data = {
            "title": "Updated Task"
        }
        response = client.put("/api/user123/tasks/nonexistent-task-id", json=update_data)

        # Should return 404 for non-existent task
        assert response.status_code == 404


def test_delete_task_endpoint(client: TestClient):
    """
    Test the DELETE /api/{user_id}/tasks/{task_id} endpoint
    """
    # Mock the JWT token validation
    with patch("src.api.auth.get_user_id_from_header", return_value="user123"):
        response = client.delete("/api/user123/tasks/nonexistent-task-id")

        # Should return 404 for non-existent task
        assert response.status_code == 404


def test_update_task_completion_endpoint(client: TestClient):
    """
    Test the PATCH /api/{user_id}/tasks/{task_id}/complete endpoint
    """
    # Mock the JWT token validation
    with patch("src.api.auth.get_user_id_from_header", return_value="user123"):
        completion_data = {
            "completed": True
        }
        response = client.patch("/api/user123/tasks/nonexistent-task-id/complete", json=completion_data)

        # Should return 404 for non-existent task
        assert response.status_code == 404