from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session
from src.database import engine
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.api.chat import router as chat_router
from src.api.tags import router as tags_router # Import the new tags router
from src.api.auth import get_current_user
from src.models.user_model import User
from src.models.task_model import Task
from src.models.conversation_model import Conversation, Message
from src.services.auth_service import create_default_admin_user

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables including the new conversation and message tables
    SQLModel.metadata.create_all(bind=engine)

    # Create default admin user
    with Session(engine) as session:
        create_default_admin_user(session)

    yield


app = FastAPI(
    title="Todo API",
    description="Full-stack Todo application backend API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[  "http://localhost:3000",
        "http://localhost:3001",
        "https://kristinasamuel-phase-3-ai-chatbot-todo-app.hf.space",
        "https://kristinasamuel-phase-3-ai-chatbot-todo-app.hf.space/"],  # In production, change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(tags_router, prefix="/api", tags=["tags"]) # Include the new tags router

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)