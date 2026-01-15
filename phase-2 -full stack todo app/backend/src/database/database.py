from sqlmodel import create_engine, Session
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from typing import Generator

# Get database URL from environment variable, with a default for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_backend.db")

# Async engine for SQLModel
# Handle different database types appropriately
if DATABASE_URL.startswith("sqlite"):
    async_engine = create_async_engine(DATABASE_URL.replace("sqlite", "sqlite+aiosqlite"))
elif DATABASE_URL.startswith("postgresql"):
    # Ensure postgresql URLs use the asyncpg driver
    if "+asyncpg" not in DATABASE_URL:
        temp_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        # Handle problematic parameters for asyncpg
        if "channel_binding=" in temp_url or "sslmode=" in temp_url:
            import urllib.parse
            parsed = urllib.parse.urlparse(temp_url)
            query_params = urllib.parse.parse_qs(parsed.query)

            # Remove parameters not supported by asyncpg
            params_to_remove = ['channel_binding', 'sslmode']
            for param in params_to_remove:
                if param in query_params:
                    del query_params[param]

            # Reconstruct URL without problematic parameters
            new_query = urllib.parse.urlencode(query_params, doseq=True)
            temp_url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, new_query, parsed.fragment
            ))
        async_engine = create_async_engine(temp_url)
    else:
        # Remove problematic parameters for asyncpg if present
        temp_url = DATABASE_URL
        if "channel_binding=" in temp_url or "sslmode=" in temp_url:
            import urllib.parse
            parsed = urllib.parse.urlparse(temp_url)
            query_params = urllib.parse.parse_qs(parsed.query)

            # Remove parameters not supported by asyncpg
            params_to_remove = ['channel_binding', 'sslmode']
            for param in params_to_remove:
                if param in query_params:
                    del query_params[param]

            # Reconstruct URL without problematic parameters
            new_query = urllib.parse.urlencode(query_params, doseq=True)
            temp_url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, new_query, parsed.fragment
            ))
        async_engine = create_async_engine(temp_url)
else:
    async_engine = create_async_engine(DATABASE_URL)

# Async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync engine (if needed for certain operations)
if DATABASE_URL.startswith("sqlite"):
    sync_engine = create_engine(DATABASE_URL)
elif DATABASE_URL.startswith("postgresql+asyncpg"):
    # Convert asyncpg URL back to regular postgresql for sync operations
    base_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    # Remove unsupported parameters for sync connection
    if "channel_binding=" in base_url or "sslmode=" in base_url:
        import urllib.parse
        parsed = urllib.parse.urlparse(base_url)
        query_params = urllib.parse.parse_qs(parsed.query)
        # Remove problematic parameters
        params_to_remove = ['channel_binding']
        for param in params_to_remove:
            if param in query_params:
                del query_params[param]
        # Reconstruct URL without problematic parameters
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        base_url = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, new_query, parsed.fragment
        ))
    sync_engine = create_engine(base_url)
elif DATABASE_URL.startswith("postgresql"):
    # Remove unsupported parameters for sync connection
    temp_url = DATABASE_URL
    if "channel_binding=" in temp_url or "sslmode=" in temp_url:
        import urllib.parse
        parsed = urllib.parse.urlparse(temp_url)
        query_params = urllib.parse.parse_qs(parsed.query)
        # Remove problematic parameters
        params_to_remove = ['channel_binding']
        for param in params_to_remove:
            if param in query_params:
                del query_params[param]
        # Reconstruct URL without problematic parameters
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        temp_url = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, new_query, parsed.fragment
        ))
    sync_engine = create_engine(temp_url)
else:
    sync_engine = create_engine(DATABASE_URL)

def get_sync_session() -> Generator[Session, None, None]:
    """
    Dependency for sync sessions
    """
    with Session(sync_engine) as session:
        yield session

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for async sessions
    """
    async with AsyncSessionLocal() as session:
        yield session