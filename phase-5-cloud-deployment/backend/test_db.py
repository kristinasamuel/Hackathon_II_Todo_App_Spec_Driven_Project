import asyncio
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine
from src.models.user_model import User
from src.models.task_model import Task

# Use the same DATABASE_URL as in your .env file
DATABASE_URL = 'postgresql://neondb_owner:npg_74lsByufGWOX@ep-shy-truth-ahpgj255-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

async def test_database_connection():
    print("Testing database connection...")

    # Create async engine
    engine = create_async_engine(DATABASE_URL)

    try:
        # Create all tables
        print("Creating tables...")
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        print("Tables created successfully!")

        # Verify tables exist by trying to query them
        print("Verifying tables exist...")

        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import create_engine
        from sqlmodel import Session

        # Create sync engine for testing
        sync_engine = create_engine(DATABASE_URL.replace('+asyncpg', ''))
        session = Session(sync_engine)

        # Test if we can query users (should be empty initially)
        users = session.exec(select(User)).all()
        print(f"Found {len(users)} users in database")

        # Test if we can query tasks (should be empty initially)
        tasks = session.exec(select(Task)).all()
        print(f"Found {len(tasks)} tasks in database")

        session.close()
        print("Database connection test completed successfully!")

    except Exception as e:
        print(f"Error connecting to database: {e}")

    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_database_connection())