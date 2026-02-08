import requests
import json
import time

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_api_endpoints():
    print("Testing Todo API Endpoints...")

    # Test the root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Response: {response.json()}")
        print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error testing root endpoint: {e}")

    # Test health endpoint
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Response: {response.json()}")
        print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error testing health endpoint: {e}")

    # Register a test user
    print("\n3. Testing user registration...")
    try:
        register_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/auth/signup", json=register_data)
        print(f"Registration Response: {response.json()}")
        print(f"Status: {response.status_code}")

        # Store token if registration successful
        if response.status_code == 200:
            print("User registered successfully!")
        else:
            print(f"Registration failed: {response.text}")
    except Exception as e:
        print(f"Error testing registration: {e}")

    # Login the test user
    print("\n4. Testing user login...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login Response: {response.json()}")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('token')  # Changed from access_token to token
            headers = {'Authorization': f'Bearer {access_token}'}
            print("User logged in successfully!")
        else:
            print(f"Login failed: {response.text}")
            # Try with admin user if default admin exists
            admin_login_data = {
                "email": "admin@example.com",
                "password": "admin123"
            }
            response = requests.post(f"{BASE_URL}/auth/login", json=admin_login_data)
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('token')  # Changed from access_token to token
                headers = {'Authorization': f'Bearer {access_token}'}
                print("Admin user logged in successfully!")
            else:
                print("No valid user credentials available")
                headers = {}
    except Exception as e:
        print(f"Error testing login: {e}")
        headers = {}

    # Test creating a task
    print("\n5. Testing task creation...")
    try:
        if headers:
            task_data = {
                "title": "Test Task",
                "description": "This is a test task",
                "completed": False
            }
            response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
            print(f"Create Task Response: {response.json()}")
            print(f"Status: {response.status_code}")

            if response.status_code == 201:  # Changed to 201 as per the API
                task_id = response.json().get('id')
                print(f"Task created successfully with ID: {task_id}")
            else:
                print(f"Task creation failed: {response.text}")
        else:
            print("Skipping task creation - no valid authentication")
    except Exception as e:
        print(f"Error testing task creation: {e}")

    # Test getting all tasks
    print("\n6. Testing getting all tasks...")
    try:
        if headers:
            response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
            print(f"Get Tasks Response: {response.json()}")
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                tasks = response.json()
                if tasks:
                    task_id = tasks[0]['id'] if len(tasks) > 0 else None
                    print(f"Retrieved {len(tasks)} tasks")
                else:
                    print("No tasks found")
            else:
                print(f"Getting tasks failed: {response.text}")
        else:
            print("Skipping get tasks - no valid authentication")
    except Exception as e:
        print(f"Error testing get tasks: {e}")

    # Test updating a task (if we have a task ID)
    print("\n7. Testing task update...")
    try:
        if headers and 'task_id' in locals() and task_id:
            update_data = {
                "title": "Updated Test Task",
                "description": "This is an updated test task",
                "completed": True
            }
            response = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data, headers=headers)
            print(f"Update Task Response: {response.json()}")
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                print("Task updated successfully!")
            else:
                print(f"Task update failed: {response.text}")
        else:
            print("Skipping task update - no valid authentication or task ID")
    except Exception as e:
        print(f"Error testing task update: {e}")

    # Test marking task as complete/incomplete
    print("\n8. Testing task completion toggle...")
    try:
        if headers and 'task_id' in locals() and task_id:
            # Toggle completion status
            response = requests.patch(f"{BASE_URL}/api/tasks/{task_id}/complete", headers=headers)
            print(f"Toggle Task Response: {response.json()}")
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                print("Task completion toggled successfully!")
            else:
                print(f"Task toggle failed: {response.text}")
        else:
            print("Skipping task toggle - no valid authentication or task ID")
    except Exception as e:
        print(f"Error testing task toggle: {e}")

    # Test deleting a task (if we have a task ID)
    print("\n9. Testing task deletion...")
    try:
        if headers and 'task_id' in locals() and task_id:
            response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
            print(f"Status: {response.status_code}")

            if response.status_code == 204:
                print("Task deleted successfully!")
            elif response.status_code == 200 and response.text == "":
                print("Task deleted successfully!")
            else:
                print(f"Task deletion failed: {response.text}")
        else:
            print("Skipping task deletion - no valid authentication or task ID")
    except Exception as e:
        print(f"Error testing task deletion: {e}")

    print("\nTesting completed!")

if __name__ == "__main__":
    test_api_endpoints()