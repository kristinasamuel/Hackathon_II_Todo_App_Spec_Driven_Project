#!/usr/bin/env python3
"""
Test script to verify the fix for task display number to actual ID mapping
"""

import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'phase-3-Ai-Chatbot', 'backend'))

from mcp_server.tools.task_operations import (
    execute_add_task, execute_list_tasks, execute_complete_task, execute_delete_task
)

# Import database and user model to create a test user
from src.database.database import get_sync_session
from src.models.user_model import User
from src.services.auth_service import AuthService
import bcrypt

def create_test_user():
    """Create a test user in the database"""
    with next(get_sync_session()) as session:
        # Create a unique user ID
        user_id = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        
        # Hash the password
        password_hash = bcrypt.hashpw("testpassword".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        user = User(
            id=user_id,
            email=f"{user_id}@example.com",
            password=password_hash
        )
        
        session.add(user)
        session.commit()
        
        print(f"Created test user: {user_id}")
        return user_id

def test_task_operations():
    # Create a test user
    user_id = create_test_user()
    
    print(f"Testing with user ID: {user_id}")
    
    # Add some test tasks
    print("\n=== Adding test tasks ===")
    print(execute_add_task({"user_id": user_id, "title": "Buy groceries", "description": "Milk, bread, eggs"}))
    print(execute_add_task({"user_id": user_id, "title": "Walk the dog", "description": "30 minutes in the park"}))
    print(execute_add_task({"user_id": user_id, "title": "Finish report", "description": "Submit by end of day"}))
    
    # List tasks to see the display numbers
    print("\n=== Listing tasks ===")
    print(execute_list_tasks({"user_id": user_id}))
    
    # Try to complete task #2 (walk the dog) using display number
    print("\n=== Completing task #2 (walk the dog) ===")
    print(execute_complete_task({"user_id": user_id, "task_id": 2}))
    
    # List tasks again to see the updated status
    print("\n=== Listing tasks after completion ===")
    print(execute_list_tasks({"user_id": user_id}))
    
    # Try to delete task #1 (buy groceries) using display number
    print("\n=== Deleting task #1 (buy groceries) ===")
    print(execute_delete_task({"user_id": user_id, "task_id": 1}))
    
    # List tasks again to see the updated list
    print("\n=== Listing tasks after deletion ===")
    print(execute_list_tasks({"user_id": user_id}))

if __name__ == "__main__":
    test_task_operations()