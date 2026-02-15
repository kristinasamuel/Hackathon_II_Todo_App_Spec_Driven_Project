import os
from typing import Dict, Any, List
import asyncio
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import the new Google AI library first, fall back to old one
try:
    import google.genai as genai
    GENAI_AVAILABLE = True
    logger.info("Using new google.genai library")
except ImportError:
    try:
        import google.generativeai as genai
        GENAI_AVAILABLE = True
        logger.info("Using deprecated google.generativeai library")
    except ImportError:
        GENAI_AVAILABLE = False
        logger.error("No Google AI library available. Please install with: pip install google-genai")

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from mcp_server.tools.task_operations import (
        execute_add_task, execute_list_tasks, execute_update_task,
        execute_complete_task, execute_delete_task, execute_get_user_info
    )
    logger.info("Successfully imported mcp_server.tools.task_operations")
except ImportError as e:
    logger.error(f"Failed to import mcp_server.tools.task_operations: {e}")
    # Define dummy functions as fallback
    def execute_add_task(params): return "Add task functionality not available"
    def execute_list_tasks(params): return "List tasks functionality not available"
    def execute_update_task(params): return "Update task functionality not available"
    def execute_complete_task(params): return "Complete task functionality not available"
    def execute_delete_task(params): return "Delete task functionality not available"
    def execute_get_user_info(params): return "Get user info functionality not available"
    logger.warning("Using fallback functions for task operations")
except Exception as e:
    logger.error(f"Unexpected error importing mcp_server.tools.task_operations: {e}")
    raise


class TodoChatAgent:
    def __init__(self):
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or not GENAI_AVAILABLE:
            # Store None to indicate that the model is not available
            self.model = None
            return

        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            logger.error(f"Error initializing Gemini model: {str(e)}")
            self.model = None

    async def process_message(self, user_id: str, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Process a user message and return an AI response
        """
        if conversation_history is None:
            conversation_history = []

        # Check if model is available
        if not self.model:
            return "AI functionality is not available. The GEMINI_API_KEY environment variable is not configured properly."

        # Build conversation history
        history_text = ""
        for msg in conversation_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history_text += f"{role.capitalize()}: {content}\n"

        # Create a prompt that guides the AI to recognize task operations
        system_prompt = f"""You are a helpful AI assistant that manages todo tasks.
You can help users with the following operations:
1. Add tasks: Look for requests to add/create/new tasks
2. List tasks: Look for requests to show/view/list tasks
3. Update tasks: Look for requests to change/edit/modify tasks
4. Complete tasks: Look for requests to mark as done/complete/finished
5. Delete tasks: Look for requests to remove/delete tasks
6. User information: Look for requests asking who the user is, user details, or user identity

IMPORTANT: When the user wants to perform a task operation, respond in this specific format:
- ADD TASK: "TASK_OPERATION:ADD:{{"user_id":"{user_id}","title":"task title","description":"task description"}}"
- LIST TASKS: "TASK_OPERATION:LIST:{{"user_id":"{user_id}","status_filter":"all"}}"
- UPDATE TASK: "TASK_OPERATION:UPDATE:{{"user_id":"{user_id}","task_id":"task_id","title":"new title"}}"
- COMPLETE TASK: "TASK_OPERATION:COMPLETE:{{"user_id":"{user_id}","task_id":"task_id","completed":true}}"
- DELETE TASK: "TASK_OPERATION:DELETE:{{"user_id":"{user_id}","task_id":"task_id"}}"
- GET USER INFO: "USER_INFO_REQUEST:{{"user_id":"{user_id}"}}"

CRITICAL: When users refer to tasks by number (e.g., 'task 1', 'task 2', 'complete task 3', 'delete task 4'),
the number represents the display position from the most recent task list shown to the user.
In these cases, pass the number directly as the 'task_id' parameter.
For example: if a user says 'complete task 2', generate: TASK_OPERATION:COMPLETE:{{"user_id":"{user_id}","task_id":2,"completed":true}}
The backend will handle converting the display number to the actual task ID.

For user information requests, you can access the user's information using the user_id provided.
Always be polite and helpful."""

        # Combine system prompt, history, and current message
        full_prompt = f"{system_prompt}\n\nConversation history:\n{history_text}\n\nCurrent user request: {message}\n\nAssistant response:"

        try:
            # Generate content with the model
            response = self.model.generate_content(full_prompt)

            # Extract the text response
            ai_response = response.text if response.text else "I'm sorry, I couldn't process that request."

            # Check if the response contains a task operation command
            if ai_response.startswith("TASK_OPERATION:") or ai_response.startswith("USER_INFO_REQUEST:"):
                # Determine the operation type
                if ai_response.startswith("TASK_OPERATION:"):
                    parts = ai_response.split(":", 2)
                    if len(parts) >= 3:
                        op_type = parts[1]
                        params_str = parts[2]
                    else:
                        return "I had trouble processing your request. Could you please rephrase it?"
                elif ai_response.startswith("USER_INFO_REQUEST:"):
                    # Handle user info request
                    parts = ai_response.split(":", 1)
                    if len(parts) >= 2:
                        params_str = parts[1]
                        op_type = "USER_INFO"
                    else:
                        return "I had trouble processing your request. Could you please rephrase it?"

                try:
                    params = json.loads(params_str)

                    # Execute the appropriate operation
                    if op_type == "ADD":
                        result = execute_add_task(params)
                    elif op_type == "LIST":
                        result = execute_list_tasks(params)
                    elif op_type == "UPDATE":
                        result = execute_update_task(params)
                    elif op_type == "COMPLETE":
                        result = execute_complete_task(params)
                    elif op_type == "DELETE":
                        result = execute_delete_task(params)
                    elif op_type == "USER_INFO":
                        result = execute_get_user_info(params)
                    else:
                        result = f"Unknown operation: {op_type}"

                    return result
                except json.JSONDecodeError:
                    return "I had trouble processing your request. Could you please rephrase it?"

            return ai_response

        except Exception as e:
            return f"Sorry, I encountered an error processing your request: {str(e)}"


# Async wrapper for the agent
async def process_user_message(user_id: str, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
    try:
        agent = TodoChatAgent()
        return await agent.process_message(user_id, message, conversation_history)
    except Exception as e:
        return f"Sorry, I encountered an error initializing the AI agent: {str(e)}"