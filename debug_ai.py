#!/usr/bin/env python3
"""
Debug script to see what the AI agent generates for task commands
"""

import sys
import os
import asyncio

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'phase-3-Ai-Chatbot', 'backend'))

from ai_agent.agent import TodoChatAgent

async def debug_ai_agent():
    # Create a test user ID
    user_id = "test_user_debug"
    
    # Test different commands
    test_commands = [
        "complete task 1",
        "delete task 2", 
        "mark task 3 as done",
        "show my tasks"
    ]
    
    agent = TodoChatAgent()
    
    for command in test_commands:
        print(f"\n--- Testing command: '{command}' ---")
        try:
            response = await agent.process_message(user_id, command)
            print(f"AI Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_ai_agent())