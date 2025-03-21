from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from app.database import Base

# Example association table
post_tag = Table(
    'post_tag',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)

class User(Base):
    """Example user model."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=True)
    
    # Define a unique constraint
    __table_args__ = (
        UniqueConstraint('username', name='uq_users_username'),
    )
    
    # Define relationships
    posts = relationship("Post", back_populates="author")

# Create an index
Index('ix_users_email', User.email, unique=True)

class Post(Base):
    """Example post model."""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Define relationships
    author = relationship("User", back_populates="posts")
    tags = relationship("Tag", secondary=post_tag, back_populates="posts")

class Tag(Base):
    """Example tag model."""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    
    # Define relationships
    posts = relationship("Post", secondary=post_tag, back_populates="tags") 