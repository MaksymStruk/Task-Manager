from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    text: Optional[str] = Field(None, description="Detailed task text")
    due_date: datetime = Field(..., description="Due date")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    text: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    short_description: Optional[str] = None

class TaskResponse(BaseModel):
    """Inheritance from BaseModel instead of TaskBase is intentional, made this for a cleaner output"""
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
        from_attributes = True