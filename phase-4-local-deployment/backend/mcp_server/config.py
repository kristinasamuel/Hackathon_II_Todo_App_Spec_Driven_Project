import os
from typing import Optional

# Database URL for MCP server
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_backend.db")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# JWT Secret for authentication
JWT_SECRET = os.getenv("JWT_SECRET", os.getenv("BETTER_AUTH_SECRET", ""))