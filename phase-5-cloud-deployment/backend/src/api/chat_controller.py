from fastapi import Depends, HTTPException, status
from typing import Optional
from sqlmodel import Session
from ..database.database import get_sync_session
from ..models.conversation_model import Conversation, Message
from ..services.conversation_service import ConversationService
from ..services.auth_service import AuthService
from ..models.user_model import User
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from ai_agent.agent import process_user_message
    logger.info("Successfully imported ai_agent.agent")
except ImportError as e:
    logger.error(f"Failed to import ai_agent.agent: {e}")
    # Re-raise the exception to cause a startup failure which will be visible
    raise
except Exception as e:
    logger.error(f"Unexpected error importing ai_agent.agent: {e}")
    raise
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    action_taken: str


def process_chat_request(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_sync_session)
) -> ChatResponse:
    """
    Process a chat request from a user
    """
    try:
        # Validate that the user exists
        user_exists = AuthService.validate_user_exists(session, user_id)
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if the AI agent can be initialized (validate API key is available)
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
            from ai_agent.agent import TodoChatAgent
            _ = TodoChatAgent()  # This will raise an error if GEMINI_API_KEY is not set
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI service not properly configured: {str(e)}"
            )
        except ImportError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI service dependencies not available: {str(e)}"
            )

        # Get or create conversation
        conversation = ConversationService.get_or_create_conversation(
            session, user_id, request.conversation_id
        )

        # Get recent conversation history for context
        conversation_history = ConversationService.get_conversation_history(
            session, conversation.conversation_id, limit=10
        )

        # Format history for AI agent
        formatted_history = []
        for msg in conversation_history:
            formatted_history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Process the message with the AI agent - run synchronously since the agent handles async internally
        import asyncio

        # Run the async function in a new event loop if none exists
        try:
            loop = asyncio.get_running_loop()
            # If we're in a running loop, we need to run the async function differently
            import concurrent.futures
            import threading

            def run_async_process():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return asyncio.run(process_user_message(
                        user_id=user_id,
                        message=request.message,
                        conversation_history=formatted_history
                    ))
                finally:
                    new_loop.close()

            # Run in a thread to avoid nested event loop issues
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_async_process)
                ai_response = future.result()

        except RuntimeError:
            # No event loop running, safe to use asyncio.run
            ai_response = asyncio.run(process_user_message(
                user_id=user_id,
                message=request.message,
                conversation_history=formatted_history
            ))

        # Save the interaction to the database
        saved_conversation, user_msg, ai_msg = ConversationService.save_chat_interaction(
            session=session,
            user_id=user_id,
            user_message=request.message,
            ai_response=ai_response,
            conversation_id=conversation.conversation_id
        )

        # Determine what action was taken based on the AI response
        action_taken = "Processed user request with AI assistance"
        if "task" in ai_response.lower():
            if "added" in ai_response.lower() or "created" in ai_response.lower():
                action_taken = "Added new task"
            elif "deleted" in ai_response.lower() or "removed" in ai_response.lower():
                action_taken = "Deleted task"
            elif "updated" in ai_response.lower() or "changed" in ai_response.lower():
                action_taken = "Updated task"
            elif "completed" in ai_response.lower() or "done" in ai_response.lower():
                action_taken = "Completed task"
            elif "listed" in ai_response.lower() or "shown" in ai_response.lower():
                action_taken = "Retrieved tasks"

        return ChatResponse(
            response=ai_response,
            conversation_id=saved_conversation.conversation_id,
            action_taken=action_taken
        )

    except Exception as e:
        # Log the error for debugging
        print(f"Error in process_chat_request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )