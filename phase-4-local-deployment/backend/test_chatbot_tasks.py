#!/usr/bin/env python3
"""
Test script to verify that chatbot tasks are being added to the database correctly.
"""

import asyncio
import json
import sqlite3
from datetime import datetime
from ai_agent.agent import process_user_message

async def test_chatbot_tasks():
    print("Testing chatbot task functionality...")

    # Sample user ID - using an existing user from the database
    user_id = "user_20260119_121847_8264"  # From the database

    print(f"\nUsing user_id: {user_id}")

    # Test adding a task via chatbot
    print("\n1. Adding a task via chatbot...")
    message = "Add a task: Buy milk from the store"
    response = await process_user_message(user_id, message)
    print(f"Chatbot response: {response}")

    # Wait a moment to ensure the task is saved
    await asyncio.sleep(1)

    # Test adding another task
    print("\n2. Adding another task via chatbot...")
    message = "Create a new task: Walk the dog"
    response = await process_user_message(user_id, message)
    print(f"Chatbot response: {response}")

    # Wait a moment to ensure the task is saved
    await asyncio.sleep(1)

    # Test listing tasks via chatbot
    print("\n3. Listing tasks via chatbot...")
    message = "Show me my tasks"
    response = await process_user_message(user_id, message)
    print(f"Chatbot response: {response}")

    # Now check the database directly
    print("\n4. Checking database directly...")
    conn = sqlite3.connect('todo_backend.db')
    cursor = conn.cursor()

    # Count total tasks for this user
    cursor.execute('SELECT COUNT(*) FROM task WHERE user_id = ?', (user_id,))
    task_count = cursor.fetchone()[0]
    print(f"Total tasks for user {user_id}: {task_count}")

    # Get all tasks for this user
    cursor.execute('SELECT id, title, description, completed FROM task WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    tasks = cursor.fetchall()
    print(f"\nTasks for user {user_id}:")
    for task in tasks[-3:]:  # Show last 3 tasks
        status = "✓" if task[3] else "○"
        print(f"  [{status}] {task[0]}: {task[1]} - {task[2]}")

    # Get all tasks in the database
    cursor.execute('SELECT COUNT(*) FROM task')
    total_tasks = cursor.fetchone()[0]
    print(f"\nTotal tasks in database: {total_tasks}")

    conn.close()

    print("\n5. Test completed!")
    print("If tasks were added successfully, the chatbot functionality is working correctly.")
    print("The tasks should now be visible in the dashboard when logged in as the same user.")

if __name__ == "__main__":
    asyncio.run(test_chatbot_tasks())