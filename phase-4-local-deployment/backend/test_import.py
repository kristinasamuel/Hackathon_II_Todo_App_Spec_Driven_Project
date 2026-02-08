#!/usr/bin/env python3
"""
Simple test script to verify that the database module can be imported without errors
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_database_import():
    """Test that the database module can be imported without errors"""
    try:
        print("Attempting to import database module...")
        from database.database import async_engine, sync_engine
        print("[SUCCESS] Successfully imported database module!")
        print(f"[INFO] Async engine type: {type(async_engine)}")
        print(f"[INFO] Sync engine type: {type(sync_engine)}")

        # Test that we can access the database URL
        import os
        from database.database import DATABASE_URL
        print(f"[INFO] Database URL: {DATABASE_URL}")

        return True
    except Exception as e:
        print(f"[ERROR] Error importing database module: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_main_import():
    """Test that the main module can be imported without errors"""
    try:
        print("\n[INFO] Attempting to import main module...")
        from main import app
        print("[SUCCESS] Successfully imported main module!")
        print(f"[INFO] App title: {app.title}")
        return True
    except Exception as e:
        print(f"[ERROR] Error importing main module: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("[INFO] Testing imports for Hugging Face deployment...")

    db_success = test_database_import()
    main_success = test_main_import()

    if db_success and main_success:
        print("\n[SUCCESS] All imports successful! The application should run on Hugging Face.")
    else:
        print("\n[ERROR] Some imports failed. Please check the errors above.")
        sys.exit(1)

        