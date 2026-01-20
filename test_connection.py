import requests
import sys

def test_backend_connection():
    """Test if the backend API is accessible"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running on port 8000?")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

def test_frontend_running():
    """Test if the frontend is accessible"""
    try:
        # Note: Frontend is running on port 3001 according to the output
        response = requests.get("http://localhost:3001", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            print(f"Status code: {response.status_code}")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to frontend. Is it running on port 3001?")
        return False
    except Exception as e:
        print(f"❌ Error connecting to frontend: {e}")
        return False

if __name__ == "__main__":
    print("Testing TaskManager Pro Application...")
    print("="*50)

    backend_ok = test_backend_connection()
    print()
    frontend_ok = test_frontend_running()

    print("\n" + "="*50)
    if backend_ok and frontend_ok:
        print("🎉 SUCCESS: Both servers are running and accessible!")
        print("🎯 TaskManager Pro is ready to use.")
        print("🌐 Access the application at: http://localhost:3001")
    else:
        print("❌ FAILURE: Some services are not accessible.")
        sys.exit(1)