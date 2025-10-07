"""Pydantic schemas for task data validation and serialization.

This module defines request/response schemas for task operations,
including validation rules and field descriptions.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.task import TaskStatus

class TaskBase(BaseModel):
    """Base task schema with common fields.
    
    Attributes:
        title: Task title (1-255 characters)
        description: Optional task description
        text: Optional detailed task content
        due_date: When the task should be completed
        status: Current task status (defaults to PENDING)
    """
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    text: Optional[str] = Field(None, description="Detailed task text")
    due_date: datetime = Field(..., description="Due date")

class TaskCreate(TaskBase):
    """Schema for creating new tasks."""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating existing tasks.
    
    All fields are optional for partial updates.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    text: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    short_description: Optional[str] = None

class TaskResponse(BaseModel):
    """Schema for task responses with all fields including metadata.
    
    Includes auto-generated fields like id, created_at, updated_at.
    """
    id: int
    title: str
    short_description: Optional[str] = None
    description: Optional[str] = None
    text: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    due_date: datetime
    status: TaskStatus

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True
