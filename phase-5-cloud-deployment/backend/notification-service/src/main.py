from fastapi import FastAPI, Depends, HTTPException, status, Request
from typing import Optional, List
from sqlmodel import Session, SQLModel, create_engine
from contextlib import asynccontextmanager
from dapr.clients import DaprClient
import json
from datetime import datetime
import uuid

# Placeholder for database and models
# In a real implementation, you would define actual models and database connection
# from ...database.database import get_sync_session # Not directly needed if only consuming events

# Assuming event models are defined or handled dynamically
class DaprEvent(SQLModel):
    id: str
    source: str
    type: str
    specversion: str
    datacontenttype: str
    data: dict
    pubsubname: str
    topic: str

# Helper to publish events (re-using from TaskService for consistency, though not publishing here)
# def publish_event(pubsub_name: str, topic_name: str, event_data: dict):
#     with DaprClient() as dapr_client:
#         dapr_client.publish_event(
#             pubsub_name=pubsub_name,
#             topic_name=topic_name,
#             data=json.dumps(event_data),
#             data_content_type='application/json'
#         )
#         print(f"Published event to pubsub '{pubsub_name}', topic '{topic_name}': {event_data.get('eventType', 'N/A')}")

# Asynchronous context manager for the application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Notification Service",
    description="Consumes reminder events and sends notifications.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Notification Service is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Dapr subscription endpoint
@app.get("/dapr/subscribe", include_in_schema=False)
async def subscribe():
    """
    Dapr subscription endpoint to register pub/sub topics.
    """
    return [
        {
            "pubsubname": "pubsub",
            "topic": "reminders",
            "route": "/reminders-events-handler"
        }
    ]

# Event handler for reminder-events
@app.post("/reminders-events-handler") # Updated route based on subscription
async def handle_reminder_event(dapr_event: DaprEvent): # No session needed for this example
    """
    Handles incoming reminder-events from Dapr Pub/Sub.
    Sends notifications to the user.
    """
    event_data = dapr_event.data
    event_type = event_data.get("eventType")
    
    print(f"Notification Service received event: {event_type} for Reminder ID: {event_data.get('reminderId')}")

    if event_type == "ReminderDue":
        task_id = event_data.get("taskId")
        user_id = event_data.get("userId")
        title = event_data.get("title")
        reminder_time = event_data.get("reminderTime")
        notification_channel = event_data.get("notificationChannel", "email")

        print(f"--- Sending Notification ---")
        print(f"User ID: {user_id}")
        print(f"Task ID: {task_id}")
        print(f"Task Title: {title}")
        print(f"Reminder Time: {reminder_time}")
        print(f"Channel: {notification_channel}")
        print(f"Notification: Your task '{title}' is due!")
        print(f"--------------------------")

        # In a real application, you would integrate with external services here:
        # - Dapr SendGrid binding for email
        # - Dapr Twilio binding for SMS
        # - WebSocket for in-app notifications
        # - Logging for audit trails

    return {"status": "notification processed"}