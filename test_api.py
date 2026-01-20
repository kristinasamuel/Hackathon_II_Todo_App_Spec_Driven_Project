#!/usr/bin/env python3
"""
Test script to verify the API endpoints are working correctly
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
TEST_PASSWORD = "password123"

def test_api_endpoints():
    print(f"Testing API endpoints at {BASE_URL}")

    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return

    # Test signup
    print("\nTesting signup...")
    signup_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "name": "Test User"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if response.status_code == 200:
            print(f"Signup successful: {response.status_code}")
            token_data = response.json()
            auth_token = token_data.get("token")
            print(f"Received token: {auth_token[:20]}..." if auth_token else "No token received")
        else:
            print(f"Signup failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"Signup request failed: {e}")
        return

    # Test login
    print("\nTesting login...")
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print(f"Login successful: {response.status_code}")
            login_result = response.json()
            auth_token = login_result.get("token")
            print(f"Received token: {auth_token[:20]}..." if auth_token else "No token received")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"Login request failed: {e}")
        return

    # Test task operations with authentication
    if auth_token:
        headers = {"Authorization": f"Bearer {auth_token}"}

        print("\nTesting task creation...")
        task_data = {
            "title": "Test Task",
            "description": "This is a test task"
        }
        try:
            response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
            if response.status_code == 200 or response.status_code == 201:
                print(f"Task creation successful: {response.status_code}")
                task = response.json()
                task_id = task.get("id")
                print(f"Created task ID: {task_id}")

                # Test getting tasks
                print("\nTesting get tasks...")
                response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
                if response.status_code == 200:
                    tasks = response.json()
                    print(f"Retrieved {len(tasks)} tasks")

                    # Test updating task
                    if task_id:
                        print(f"\nTesting update task {task_id}...")
                        update_data = {
                            "title": "Updated Test Task",
                            "completed": True
                        }
                        response = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data, headers=headers)
                        if response.status_code == 200:
                            print(f"Task update successful: {response.status_code}")
                        else:
                            print(f"Task update failed: {response.status_code} - {response.text}")

                    # Test toggle completion
                    if task_id:
                        print(f"\nTesting toggle task completion {task_id}...")
                        toggle_data = {"completed": False}
                        response = requests.patch(f"{BASE_URL}/api/tasks/{task_id}/complete", json=toggle_data, headers=headers)
                        if response.status_code == 200:
                            print(f"Task completion toggle successful: {response.status_code}")
                        else:
                            print(f"Task completion toggle failed: {response.status_code} - {response.text}")

                    # Test deleting task
                    if task_id:
                        print(f"\nTesting delete task {task_id}...")
                        response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
                        if response.status_code == 204:
                            print(f"Task deletion successful: {response.status_code}")
                        else:
                            print(f"Task deletion failed: {response.status_code} - {response.text}")
                else:
                    print(f"Get tasks failed: {response.status_code} - {response.text}")
            else:
                print(f"Task creation failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Task operations failed: {e}")

    print("\nAPI test completed!")

if __name__ == "__main__":
    test_api_endpoints()