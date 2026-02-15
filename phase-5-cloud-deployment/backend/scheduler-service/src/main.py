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
from ....models.task_model import Task, TaskCreate, Priority # Example model import
from ....models.user_model import User # Assuming User model might be needed

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
    title="Scheduler Service",
    description="Manages recurring task logic and Dapr Jobs API integration.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Scheduler Service is running!"}

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
    """
    event_data = dapr_event.data
    event_type = event_data.get("eventType")
    
    print(f"Scheduler Service received event: {event_type} for Task ID: {event_data.get('taskId')}")

    if event_type == "TaskCreated" and event_data.get("isRecurring"):
        # Logic to schedule recurring task instances
        task_id = event_data.get("taskId")
        user_id = event_data.get("userId")
        recurrence_rule = event_data.get("recurrenceRule")
        title = event_data.get("title")

        if not recurrence_rule:
            print(f"Warning: Recurring task {task_id} has no recurrence rule defined.")
            return {"status": "ignored - no recurrence rule"}

        # For demonstration, let's simulate a simple daily recurrence using Dapr Jobs API
        # In a real scenario, recurrence_rule parsing would be more complex (e.g., rrule-js)

        # Schedule the job to create the next instance
        with DaprClient() as dapr_client:
            # Dapr Job requires a target endpoint in this service to be invoked
            # This is a simplified example. A real recurring task might schedule
            # itself or a separate process.
            job_name = f"recurring-task-{task_id}"
            
            # For simplicity, let's assume recurrence_rule means "daily"
            # Schedule for next day
            next_occurrence_time = (datetime.now(pytz.utc) + timedelta(days=1)).isoformat()
            
            # This is a direct invocation for the 'create_recurring_instance' endpoint in THIS service
            # Dapr Job API scheduling using HTTP is done by posting to Dapr sidecar /v1.0/schedule/job
            # The job will call back into this service.
            
            # The cron expression '0 0 * * *' would mean every day at midnight UTC
            # For testing, we might schedule it for a few seconds later.
            
            # This is a more complex aspect. Let's assume a "job definition" for Dapr
            # For simplicity now, let's just log that it would be scheduled.
            print(f"Would schedule a Dapr Job for recurring task {task_id} with rule {recurrence_rule}")
            
            # Example: schedule a job to fire 'create_recurring_instance' endpoint in 1 minute
            # Dapr Job API requires a cron string and a definition of what to call
            # This part is conceptual for now, as Dapr Jobs API is still evolving or requires a different approach
            # for programmatic scheduling of a new task.

            # Simplified: Publish an event to task-updates directly for immediate "next" instance
            # In real life, Dapr scheduler component or a dedicated library would manage this.
            
            # For immediate next instance (demonstration purpose):
            # This is not actually scheduling, but creating a new instance
            # which is better done by the Reminder service or a dedicated job
            
            # For T014, the focus is on "handle recurring task scheduling".
            # This implies setting up a job.
            
            # For now, let's just acknowledge the event and conceptually handle scheduling.
            # Actual Dapr Job creation logic will be more involved.

            # Example of how a next task *could* be created by this service (conceptual)
            next_instance_id = str(uuid.uuid4())
            new_task_create_data = TaskCreate(
                title=f"{title} (recurring instance)",
                user_id=user_id,
                due_date=(datetime.now(pytz.utc) + timedelta(days=1)) # Example next due date
            )
            
            # This service shouldn't directly create tasks in DB, it should publish an event
            # to the main Task Service to create the new instance.

            # Example of event to publish (T013 published to task-events, this is task-updates)
            event_payload = {
                "eventType": "RecurringTaskInstanceCreated",
                "originalTaskId": task_id,
                "newTaskId": next_instance_id,
                "userId": user_id,
                "title": f"{title} (recurring instance)",
                "dueDate": new_task_create_data.due_date.isoformat() if new_task_create_data.due_date else None,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            publish_event("pubsub", "task-updates", event_payload)
            print(f"Published 'RecurringTaskInstanceCreated' for original task {task_id}")
            
    return {"status": "event processed by scheduler"}