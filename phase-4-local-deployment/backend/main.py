from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session

from src.database import engine
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router

# ✅ DIRECT IMPORT (NO try/except)
# agar error hoga to logs me clearly dikhega
# Import chat router with error handling to prevent startup failures
try:
    from src.api.chat import router as chat_router
    CHAT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Chat functionality not available: {e}")
    CHAT_AVAILABLE = False
    chat_router = None

from src.services.auth_service import create_default_admin_user


# ========================
# Lifespan
# ========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        create_default_admin_user(session)

    yield


# ========================
# App
# ========================
app = FastAPI(
    title="Todo API",
    description="Full-stack Todo application backend API",
    version="1.0.0",
    lifespan=lifespan
)


# ========================
# CORS
# ========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:3001","http://127.0.0.1:3000","http://127.0.0.1:3001","https://kristinasamuel-phase-3-ai-chatbot-todo-app.hf.space",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================
# Routers
# ========================
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])

# Conditionally include chat router if available
if CHAT_AVAILABLE:
    app.include_router(chat_router, prefix="/api", tags=["chat"])
else:
    @app.post("/api/chat")
    async def chat_unavailable():
        return {
            "response": "Chat functionality is not available due to missing dependencies or configuration",
            "conversation_id": "fallback-conversation-id",
            "action_taken": "None - Chat unavailable"
        }

    # Also add a GET endpoint for health check
    @app.get("/api/chat")
    async def chat_health():
        return {"status": "Chat functionality is not available"}


# ========================
# Basic routes
# ========================
@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ========================
# Local run ONLY
# HuggingFace safe port
# ========================
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Changed from 7860 to 8000 for local deployment
    uvicorn.run(app, host="0.0.0.0", port=port)
