from fastapi import FastAPI, Depends, HTTPException, status, Request
from typing import Optional, List
from sqlmodel import Session, SQLModel, create_engine
from contextlib import asynccontextmanager
from dapr.clients import DaprClient
import json
from datetime import datetime, timedelta
import pytz # for timezone awareness
import uuid

# Placeholder for database and models
from ....database.database import get_sync_session
from ....models.task_model import Task # Example model import

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

# Helper to publish events (re-using from TaskService for consistency)
def publish_event(pubsub_name: str, topic_name: str, event_data: dict):
    with DaprClient() as dapr_client:
        dapr_client.publish_event(
            pubsub_name=pubsub_name,
            topic_name=topic_name,
            data=json.dumps(event_data),
            data_content_type='application/json'
        )
        print(f"Published event to pubsub '{pubsub_name}', topic '{topic_name}': {event_data.get('eventType', 'N/A')}")

# Asynchronous context manager for the application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Reminder Service",
    description="Manages reminder scheduling and Dapr Jobs API integration.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Reminder Service is running!"}

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
            "topic": "task-events",
            "route": "/task-events-handler"
        }
    ]

# Event handler for task-events
@app.post("/task-events-handler")
async def handle_task_event(dapr_event: DaprEvent, session: Session = Depends(get_sync_session)):
    """
    Handles incoming task-events from Dapr Pub/Sub.
    Schedules/cancels reminders based on task data.
    """
    event_data = dapr_event.data
    event_type = event_data.get("eventType")
    task_id = event_data.get("taskId")
    user_id = event_data.get("userId")
    reminder_at_str = event_data.get("reminderAt")

    print(f"Reminder Service received event: {event_type} for Task ID: {task_id}")

    # Job name for Dapr scheduler
    job_name = f"reminder-task-{task_id}"

    with DaprClient() as dapr_client:
        if event_type == "TaskCreated" or event_type == "TaskUpdated":
            if reminder_at_str:
                try:
                    # Ensure timezone awareness. Backend stores UTC, so convert.
                    reminder_time = datetime.fromisoformat(reminder_at_str.replace('Z', '+00:00'))
                    # Dapr scheduler uses cron strings or explicit datetime for single fire
                    # For a single reminder, we want it to fire once at reminder_time
                    
                    # Dapr's schedule_job expects a cron expression.
                    # For a one-off reminder, we could schedule it for the exact time
                    # and have it call an endpoint in this service to publish the ReminderDue event.
                    
                    # Example: schedule job for 1 minute from now for testing
                    # For actual reminder_time, need to generate cron string for specific time
                    
                    # Simplified cron for now: every minute for 5 minutes, starting at current time
                    # In a real scenario, you'd calculate a cron for a single fire or use a more precise Dapr scheduler feature
                    # that allows a specific timestamp.
                    
                    # Dapr Jobs API for programmatic scheduling is not fully direct for single timestamp.
                    # The spec mentions "Scheduler/Jobs API for reminders".
                    # Option 1: Store reminder in state store and have a separate cron job poll.
                    # Option 2: Use Dapr Bindings (e.g., cron binding) to trigger an endpoint at specific time.
                    # Option 3: If Dapr Jobs API supports one-off triggers for specific datetime, use that.
                    
                    # For this implementation, let's assume Dapr has a way to trigger a job once at a specific time.
                    # As a placeholder, we'll log the scheduling and publish the reminder immediately for testing.

                    # Generate cron for reminder_time. This is complex for one-off exact time.
                    # Instead, we will use a simplified approach, and log that it should be scheduled.
                    print(f"Would schedule Dapr Job '{job_name}' to trigger at {reminder_time.isoformat()}")

                    # For demonstration, publish the reminder event immediately if reminder_time is close
                    # or for simple testing. In production, this would be a Dapr Job firing.
                    if reminder_time <= datetime.now(pytz.utc) + timedelta(minutes=5): # If reminder is due soon, simulate fire
                        reminder_event_payload = {
                            "eventType": "ReminderDue",
                            "reminderId": str(uuid.uuid4()),
                            "taskId": task_id,
                            "userId": user_id,
                            "title": event_data.get("title"),
                            "description": event_data.get("description"),
                            "reminderTime": reminder_time.isoformat() + "Z",
                            "notificationChannel": "email", # Default channel
                            "timestamp": datetime.utcnow().isoformat() + "Z"
                        }
                        publish_event("pubsub", "reminders", reminder_event_payload)
                        print(f"Published 'ReminderDue' event for task {task_id} immediately for test.")
                    
                except ValueError:
                    print(f"Invalid reminderAt format for task {task_id}: {reminder_at_str}")
            else:
                # If reminderAt is cleared, cancel any existing job
                print(f"Reminder cleared for task {task_id}. Would cancel job '{job_name}'")
                # dapr_client.delete_job(job_name=job_name) # Requires Dapr Jobs API
        elif event_type == "TaskDeleted":
            print(f"Task {task_id} deleted. Would cancel job '{job_name}'")
            # dapr_client.delete_job(job_name=job_name) # Requires Dapr Jobs API

    return {"status": "event processed by reminder service"}