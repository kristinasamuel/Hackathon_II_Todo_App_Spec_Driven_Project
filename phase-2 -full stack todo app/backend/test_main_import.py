#!/usr/bin/env python3
"""
Simple test to verify that the main module can be imported without errors
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_main_import():
    """Test that the main module can be imported without errors"""
    try:
        print("[INFO] Attempting to import main module...")

        # Temporarily disable relative imports by changing the working directory
        original_cwd = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(__file__), 'src'))

        # Import the main module
        import main
        print("[SUCCESS] Successfully imported main module!")
        print(f"[INFO] App title: {main.app.title}")

        # Change back to original directory
        os.chdir(original_cwd)

        return True
    except Exception as e:
        print(f"[ERROR] Error importing main module: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("[INFO] Testing main module import for Hugging Face deployment...")

    success = test_main_import()

    if success:
        print("\n[SUCCESS] Main module import successful! The application should run on Hugging Face.")
    else:
        print("\n[ERROR] Main module import failed. Please check the errors above.")
        sys.exit(1)