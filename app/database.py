from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect

from app.config.settings import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create base class for models
Base = declarative_base()

# Session dependency
async def get_db() -> AsyncSession:
    """Dependency for getting async database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Function to get inspector
async def get_inspector(session: AsyncSession):
    """Get SQLAlchemy inspector for retrieving metadata."""
    try:
        # Use the engine directly to get the inspector
        return inspect(engine)
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Failed to get database inspector: {str(e)}") 