from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .api import tasks
from .api import auth
try:
    from .api import chat
    CHAT_AVAILABLE = True
except ImportError:
    CHAT_AVAILABLE = False
    chat = None
from .database.database import async_engine
from sqlmodel import SQLModel
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from .middleware.auth_middleware import AuthMiddleware
import uvicorn
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response


# Create FastAPI app instance
app = FastAPI(
    title="Todo Backend API",
    description="Secure, RESTful backend for a multi-user Todo Web Application",
    version="0.1.0"
)

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)
# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Add authentication middleware first (before CORS)
app.add_middleware(
    AuthMiddleware,
    public_paths=[
        "/docs", "/redoc", "/openapi.json",  # Documentation endpoints
        "/health", "/ping",  # Health check endpoints
        "/",  # Root endpoint
        "/auth/login",  # Authentication endpoints
        "/auth/signup",
        "/auth/validate",
        "/auth/me",
        "/auth/refresh",
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://kristinasamuel-phase-3-ai-chatbot-todo-app.hf.space",
    ],  # Allow specific origins including the deployed Hugging Face Space and local addresses
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes - auth endpoints should be under /auth prefix
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

# Conditionally include chat router if available
if CHAT_AVAILABLE:
    app.include_router(chat.router, prefix="/api", tags=["chat"])
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

@app.on_event("startup")
def on_startup():
    """
    Initialize the database on startup
    """
    from sqlmodel import SQLModel
    from sqlalchemy import create_engine
    import os

    logger.info("Creating database tables...")

    # Get database URL from environment variable, with a default for development
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_backend.db")

    # Use sync engine for startup to avoid async issues with multiprocessing
    if DATABASE_URL.startswith("sqlite"):
        sync_engine = create_engine(DATABASE_URL)
    elif DATABASE_URL.startswith("postgresql"):
        # Convert asyncpg URL back to regular postgresql for sync operations
        base_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        sync_engine = create_engine(base_url)
    else:
        sync_engine = create_engine(DATABASE_URL)
   # Create all tables
    SQLModel.metadata.create_all(bind=sync_engine)
    logger.info("Database tables created successfully")

@app.get("/")
def read_root():
    """
    Root endpoint to verify the API is running
    """
    return {"message": "Todo Backend API is running!"}

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "todo-backend"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Changed host to 0.0.0.0 for broader accessibility