from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .api import tasks
from .api import auth
from .database.database import async_engine
from sqlmodel import SQLModel
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

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

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://kristinasamuel-phase-3-ai-chatbot-todo-app.hf.space",
        "https://kristinasamuel-phase-3-ai-chatbot-todo-app.hf.space/"
    ],  # Allow specific origins including the deployed Hugging Face Space
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes - auth endpoints should be under /auth prefix
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

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
    uvicorn.run(app, host="127.0.0.1", port=8000)