from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    DONE = "done"

class Task(Base):
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
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
