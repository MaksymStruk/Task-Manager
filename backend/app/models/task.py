"""Task model definitions.

This module contains SQLAlchemy models for task management,
including the Task model and TaskStatus enum.
"""

import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from sqlalchemy.sql import func

from app.db.database import Base

class TaskStatus(str, enum.Enum):
    """Task status enumeration.
    
    Attributes:
        PENDING: Task is waiting to be processed
        DONE: Task has been completed
    """
    PENDING = "pending"
    DONE = "done"

class Task(Base):
    """Task model for storing task information.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        title: Task title (required, indexed)
        short_description: Auto-generated short description
        description: Task description
        text: Detailed task content
        due_date: When the task should be completed (required, indexed)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        status: Current task status (PENDING/DONE, indexed)
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    short_description = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    text = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True)

    def __repr__(self):
        """String representation of Task instance."""
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
