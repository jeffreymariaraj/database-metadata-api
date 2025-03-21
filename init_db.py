import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, Base, async_session
from app.models import User, Post, Tag

async def init_db():
    """Initialize the database with example tables and data."""
    try:
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        # Create example data
        async with async_session() as session:
            # Create users
            user1 = User(username="johndoe", email="john@example.com", full_name="John Doe")
            user2 = User(username="janedoe", email="jane@example.com", full_name="Jane Doe")
            session.add_all([user1, user2])
            await session.commit()
            
            # Create tags
            tag1 = Tag(name="python")
            tag2 = Tag(name="fastapi")
            tag3 = Tag(name="sqlalchemy")
            session.add_all([tag1, tag2, tag3])
            await session.commit()
            
            # Create posts with tags
            post1 = Post(
                title="Getting Started with FastAPI",
                content="FastAPI is a modern web framework for building APIs with Python.",
                user_id=user1.id,
                tags=[tag1, tag2]
            )
            post2 = Post(
                title="SQLAlchemy Tutorial",
                content="SQLAlchemy is a powerful ORM library for Python.",
                user_id=user1.id,
                tags=[tag1, tag3]
            )
            post3 = Post(
                title="Building APIs with FastAPI and SQLAlchemy",
                content="This tutorial shows how to combine FastAPI with SQLAlchemy.",
                user_id=user2.id,
                tags=[tag1, tag2, tag3]
            )
            session.add_all([post1, post2, post3])
            await session.commit()
        
        print("Database initialized successfully with example data.")
    except Exception as e:
        print(f"Database initialization failed: {e}")

if __name__ == "__main__":
    asyncio.run(init_db()) 