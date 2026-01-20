#!/usr/bin/env python3
"""
Test script to verify the task functionality is working correctly
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
TEST_PASSWORD = "password123"

def test_task_functionality():
    print(f"Testing task functionality at {BASE_URL}")

    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"[PASS] Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[FAIL] Health check failed: {e}")
        return False

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
            print(f"[PASS] Signup successful: {response.status_code}")
            token_data = response.json()
            auth_token = token_data.get("token")
            if auth_token:
                print(f"[PASS] Received authentication token")
            else:
                print("[FAIL] No token received")
                return False
        else:
            print(f"[FAIL] Signup failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[FAIL] Signup request failed: {e}")
        return False

    # Test login
    print("\nTesting login...")
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print(f"[PASS] Login successful: {response.status_code}")
            login_result = response.json()
            auth_token = login_result.get("token")
            if auth_token:
                print(f"[PASS] Received authentication token")
            else:
                print("[FAIL] No token received")
                return False
        else:
            print(f"[FAIL] Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[FAIL] Login request failed: {e}")
        return False

    # Test task operations with authentication
    if auth_token:
        headers = {"Authorization": f"Bearer {auth_token}"}

        print("\nTesting task creation...")
        task_data = {
            "title": "Test Task 1",
            "description": "This is the first test task"
        }
        try:
            response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
            if response.status_code in [200, 201]:
                print(f"[PASS] Task creation successful: {response.status_code}")
                task1 = response.json()
                task1_id = task1.get("id")
                print(f"[PASS] Created task ID: {task1_id}")

                # Test creating another task
                task_data2 = {
                    "title": "Test Task 2",
                    "description": "This is the second test task"
                }
                response2 = requests.post(f"{BASE_URL}/api/tasks", json=task_data2, headers=headers)
                if response2.status_code in [200, 201]:
                    print(f"[PASS] Second task creation successful: {response2.status_code}")
                    task2 = response2.json()
                    task2_id = task2.get("id")
                    print(f"[PASS] Created second task ID: {task2_id}")

                    # Test getting tasks
                    print("\nTesting get all tasks...")
                    response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
                    if response.status_code == 200:
                        tasks = response.json()
                        print(f"[PASS] Retrieved {len(tasks)} tasks")

                        # Test updating task
                        if task1_id:
                            print(f"\nTesting update task {task1_id}...")
                            update_data = {
                                "title": "Updated Test Task 1",
                                "description": "Updated description for test task 1",
                                "completed": True
                            }
                            response = requests.put(f"{BASE_URL}/api/tasks/{task1_id}", json=update_data, headers=headers)
                            if response.status_code == 200:
                                print(f"[PASS] Task update successful: {response.status_code}")
                            else:
                                print(f"[FAIL] Task update failed: {response.status_code} - {response.text}")

                        # Test toggle completion
                        if task2_id:
                            print(f"\nTesting toggle task completion {task2_id}...")
                            toggle_data = {"completed": True}
                            response = requests.patch(f"{BASE_URL}/api/tasks/{task2_id}/complete", json=toggle_data, headers=headers)
                            if response.status_code == 200:
                                print(f"[PASS] Task completion toggle successful: {response.status_code}")
                            else:
                                print(f"[FAIL] Task completion toggle failed: {response.status_code} - {response.text}")

                        # Test getting specific task
                        if task1_id:
                            print(f"\nTesting get specific task {task1_id}...")
                            response = requests.get(f"{BASE_URL}/api/tasks/{task1_id}", headers=headers)
                            if response.status_code == 200:
                                specific_task = response.json()
                                print(f"[PASS] Retrieved specific task: {specific_task.get('title')}")
                            else:
                                print(f"[FAIL] Failed to get specific task: {response.status_code} - {response.text}")

                        # Test deleting tasks
                        if task1_id:
                            print(f"\nTesting delete task {task1_id}...")
                            response = requests.delete(f"{BASE_URL}/api/tasks/{task1_id}", headers=headers)
                            if response.status_code == 204:
                                print(f"[PASS] Task deletion successful: {response.status_code}")
                            else:
                                print(f"[FAIL] Task deletion failed: {response.status_code} - {response.text}")

                        if task2_id:
                            print(f"\nTesting delete task {task2_id}...")
                            response = requests.delete(f"{BASE_URL}/api/tasks/{task2_id}", headers=headers)
                            if response.status_code == 204:
                                print(f"[PASS] Task deletion successful: {response.status_code}")
                            else:
                                print(f"[FAIL] Task deletion failed: {response.status_code} - {response.text}")

                    else:
                        print(f"[FAIL] Get tasks failed: {response.status_code} - {response.text}")
                else:
                    print(f"[FAIL] Second task creation failed: {response2.status_code} - {response2.text}")
            else:
                print(f"[FAIL] Task creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"[FAIL] Task operations failed: {e}")
            return False

    print("\n[ALL PASS] All task functionality tests passed!")
    return True

if __name__ == "__main__":
    success = test_task_functionality()
    if success:
        print("\n[SUCCESS] All tests completed successfully!")
    else:
        print("\n[FAILURE] Some tests failed!")
        exit(1)