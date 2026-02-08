import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_backend.db")

    # Authentication settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")

    # JWT settings
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Todo App Backend"

    # CORS settings
    BACKEND_CORS_ORIGINS: str = "*"  # In production, replace with specific origins

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    """
    Get the application settings instance.

    Returns:
        Settings: The application settings
    """
    return Settings()


# Validate required settings on startup
def validate_settings():
    """
    Validate that required settings are present.

    Raises:
        ValueError: If required settings are missing
    """
    settings = get_settings()

    if not settings.BETTER_AUTH_SECRET:
        raise ValueError("BETTER_AUTH_SECRET environment variable is required")

    # Don't require DATABASE_URL since database.py has a default
    # if not settings.DATABASE_URL:
    #     raise ValueError("DATABASE_URL environment variable is required")


# Call validation on module import
validate_settings()