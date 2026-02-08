"""
Test script to verify chatbot functionality and identify the 403 error
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json"
}

def get_auth_token():
    """Get authentication token for testing"""
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            print(f"[SUCCESS] Successfully obtained auth token")
            return token
        else:
            print(f"[ERROR] Failed to login. Status: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Error during login: {e}")
        return None

def test_basic_task_operations(auth_token):
    """Test basic task operations to ensure they work"""
    headers = {**HEADERS, "Authorization": f"Bearer {auth_token}"}

    # Test getting tasks
    try:
        response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
        print(f"[SUCCESS] GET /api/tasks - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"[ERROR] Error testing GET /api/tasks: {e}")

    # Test creating a task
    try:
        task_data = {
            "title": "Test task from direct API",
            "description": "This is a test task created directly via API"
        }
        response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
        print(f"[SUCCESS] POST /api/tasks - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Created task: {response.json()}")
            return response.json().get('id')  # Return task ID for later tests
    except Exception as e:
        print(f"[ERROR] Error testing POST /api/tasks: {e}")
        return None

def test_chatbot_functionality(auth_token):
    """Test chatbot functionality that should create tasks"""
    headers = {**HEADERS, "Authorization": f"Bearer {auth_token}"}

    # Test 1: Simple message
    print("\n--- Testing simple chat message ---")
    chat_data = {
        "message": "Hello, how are you?",
        "conversation_id": None
    }

    try:
        response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
        print(f"Chat response status: {response.status_code}")
        if response.status_code == 200:
            print(f"[SUCCESS] Chat response: {response.json()}")
        else:
            print(f"[ERROR] Chat error response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Error in simple chat test: {e}")

    # Test 2: Task creation request (this should trigger the 403 error)
    print("\n--- Testing task creation via chat ---")
    chat_data = {
        "message": "Add a task to buy groceries",
        "conversation_id": None
    }

    try:
        response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
        print(f"Task creation chat status: {response.status_code}")
        if response.status_code == 200:
            print(f"[SUCCESS] Task creation response: {response.json()}")
        else:
            print(f"[ERROR] Task creation error: {response.text}")

        # Check specifically for the 403 error
        if response.status_code == 403 or ('403' in str(response.text)):
            print("[ERROR] DETECTED 403 ERROR in chat response!")
            print(f"Full response: {response.text}")

    except Exception as e:
        print(f"[ERROR] Error in task creation chat test: {e}")

def test_api_key_configuration():
    """Test if the API key is properly configured"""
    print("\n--- Checking API key configuration ---")

    # Check if GEMINI_API_KEY is set in environment
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print(f"✅ GEMINI_API_KEY is set in environment")
        # Check if it looks like a real API key (basic validation)
        if gemini_key.startswith("AIza") and len(gemini_key) > 20:
            print("✅ API key format appears valid")
        else:
            print("⚠️  API key format might be invalid")
    else:
        print("❌ GEMINI_API_KEY is not set in environment")

def main():
    print("[INFO] Starting Chatbot Functionality Test")
    print("="*50)

    # Test API key configuration first
    test_api_key_configuration()

    # Get authentication token
    auth_token = get_auth_token()
    if not auth_token:
        print("[ERROR] Cannot proceed without authentication token")
        return

    print(f"\nUsing auth token: {auth_token[:20]}..." if auth_token else "No token")

    # Test basic functionality first
    print("\n[TEST] Testing basic task operations...")
    task_id = test_basic_task_operations(auth_token)

    # Test chatbot functionality
    print("\n[TEST] Testing chatbot functionality...")
    test_chatbot_functionality(auth_token)

    print("\n" + "="*50)
    print("Test completed. Check results above for 403 error details.")

if __name__ == "__main__":
    main()