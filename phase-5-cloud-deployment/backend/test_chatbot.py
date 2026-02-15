import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_ai_chatbot():
    print("Testing AI Chatbot Endpoint...")

    # Start the server first (make sure to run `python -m uvicorn main:app --reload` in another terminal)

    # Login to get the authentication token
    print("\n1. Logging in to get authentication token...")
    try:
        login_data = {
            "email": "admin@example.com",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('token')
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            print("Logged in successfully!")
        else:
            print(f"Login failed: {response.text}")
            return
    except Exception as e:
        print(f"Error during login: {e}")
        return

    # Test the AI chat endpoint
    print("\n2. Testing AI chat endpoint...")
    try:
        chat_data = {
            "message": "Hello, how are you?"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
        print(f"Chat Response Status: {response.status_code}")

        if response.status_code == 200:
            chat_response = response.json()
            print(f"Chat Response: {chat_response}")
        else:
            print(f"Chat failed: {response.text}")

    except Exception as e:
        print(f"Error testing chat: {e}")

    # Test with a more specific question
    print("\n3. Testing AI chat with specific question...")
    try:
        chat_data = {
            "message": "What can you help me with regarding my tasks?"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
        print(f"Chat Response Status: {response.status_code}")

        if response.status_code == 200:
            chat_response = response.json()
            print(f"Chat Response: {chat_response}")
        else:
            print(f"Chat failed: {response.text}")

    except Exception as e:
        print(f"Error testing chat: {e}")

    print("\nAI Chatbot testing completed!")

if __name__ == "__main__":
    test_ai_chatbot()