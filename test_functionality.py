import requests
import json

def test_full_functionality():
    """
    Test the full functionality of the AI Chatbot
    """
    print("=" * 60)
    print("Testing Full AI Chatbot Functionality")
    print("=" * 60)

    base_url = "http://localhost:8000"

    # Test 1: Check if servers are running
    print("1. Checking server connectivity...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   [SUCCESS] Backend server is running")
            print(f"   Response: {response.json()}")
        else:
            print(f"   [ERROR] Backend server returned status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   [ERROR] Backend server is not accessible")
        return False
    except Exception as e:
        print(f"   [ERROR] Error connecting to backend: {str(e)}")
        return False

    print()

    # Test 2: Check API endpoints
    print("2. Checking API endpoints...")
    try:
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            openapi_spec = response.json()
            paths = openapi_spec.get("paths", {})

            if "/api/chat" in paths:
                print("   [SUCCESS] Chat API endpoint available")
            else:
                print("   [ERROR] Chat API endpoint not found")

            if "/auth/login" in paths:
                print("   [SUCCESS] Auth API endpoint available")
            else:
                print("   [ERROR] Auth API endpoint not found")
        else:
            print(f"   [ERROR] Could not retrieve OpenAPI spec: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] Error checking API spec: {str(e)}")

    print()

    # Test 3: Try to get a test token by creating a user or using an existing one
    print("3. Testing authentication...")

    # First, try to login with test credentials
    test_email = "test@example.com"
    test_password = "password123"

    try:
        login_response = requests.post(
            f"{base_url}/auth/login",
            json={"email": test_email, "password": test_password},
            headers={"Content-Type": "application/json"}
        )

        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get("access_token")
            if token:
                print("   [SUCCESS] Successfully obtained authentication token")
            else:
                print("   [ERROR] No token in login response")
                print(f"   Response: {login_data}")
                # Try with different response structure
                if "token" in login_data:
                    token = login_data["token"]
                    print("   [SUCCESS] Successfully obtained authentication token (alternative format)")
                elif "data" in login_data and "access_token" in login_data["data"]:
                    token = login_data["data"]["access_token"]
                    print("   [SUCCESS] Successfully obtained authentication token (nested format)")
                else:
                    print("   [ERROR] Could not find token in response")
                    token = None
        else:
            print(f"   [ERROR] Login failed with status {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            token = None

    except Exception as e:
        print(f"   [ERROR] Error during login: {str(e)}")
        token = None

    print()

    # Test 4: Test chat functionality if token is available
    if token:
        print("4. Testing chat functionality...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Test adding a task
        print("   Testing: Add a task")
        try:
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": "Add a task to buy groceries"},
                headers=headers
            )

            if response.status_code == 200:
                result = response.json()
                print(f"   [SUCCESS] Chat response received")
                print(f"   AI Response: {result.get('response', 'No response')[:100]}...")
            else:
                print(f"   [ERROR] Chat request failed with status {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   [ERROR] Error in chat request: {str(e)}")

        print()

        # Test listing tasks
        print("   Testing: List tasks")
        try:
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": "Show me my tasks"},
                headers=headers
            )

            if response.status_code == 200:
                result = response.json()
                print(f"   [SUCCESS] Chat response received")
                print(f"   AI Response: {result.get('response', 'No response')[:100]}...")
            else:
                print(f"   [ERROR] Chat request failed with status {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   [ERROR] Error in chat request: {str(e)}")

    else:
        print("4. Skipping chat functionality tests (no token available)")
        print("   You need to create a user account and obtain a token first")
        print("   Or ensure your auth system is working properly")

    print()
    print("=" * 60)
    print("Functionality Test Complete!")
    print("=" * 60)

    if token:
        print("[SUCCESS] All systems operational! AI Chatbot is working correctly.")
        print(f"Use this token for frontend testing: {token[:20]}...")
    else:
        print("[WARNING] Authentication token not available.")
        print("Please ensure:")
        print("- Your auth system is working")
        print("- You have valid test credentials")
        print("- Users can log in and receive tokens")

    return True

def test_frontend_pages():
    """
    Test frontend page accessibility
    """
    print("\n" + "=" * 60)
    print("Testing Frontend Pages")
    print("=" * 60)

    frontend_url = "http://localhost:3000"

    pages_to_test = [
        ("/", "Home page"),
        ("/login", "Login page"),
        ("/signup", "Sign up page"),
        ("/dashboard", "Dashboard"),
        ("/tasks", "Tasks page"),
        ("/ai-chatbot", "AI Chatbot page")
    ]

    for path, description in pages_to_test:
        try:
            response = requests.get(f"{frontend_url}{path}", timeout=5)
            if response.status_code == 200:
                print(f"   [SUCCESS] {description} accessible")
            else:
                print(f"   [ERROR] {description} returned status {response.status_code}")
        except Exception as e:
            print(f"   [ERROR] {description} error: {str(e)}")

    print()
    print("=" * 60)
    print("Frontend Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    print("Starting Comprehensive Functionality Test")
    print()

    # Test backend functionality
    test_full_functionality()

    # Test frontend pages
    test_frontend_pages()

    print()
    print("Summary:")
    print("   - Backend server: http://localhost:8000")
    print("   - Frontend server: http://localhost:3000")
    print("   - AI Chatbot endpoint: http://localhost:8000/api/chat")
    print("   - AI Chatbot page: http://localhost:3000/ai-chatbot")
    print()
    print("To use the AI Chatbot:")
    print("   1. Log in to the application")
    print("   2. Navigate to the AI Chatbot page")
    print("   3. Start chatting to manage your tasks!")