"""Task service layer for business logic.

This module provides async CRUD operations for task management,
including creation, updates, deletion, and status management.
"""

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    """Service class for task operations.

    Provides async CRUD operations and business logic for task management.
    """
    def __init__(self, db: AsyncSession):
        """Initialize TaskService with database session.

        Args:
            db: Async database session
        """
        self.db = db

    async def get_tasks(self, skip: int = 0, limit: int = 100):
        """Get tasks with pagination.

        Args:
            skip: Number of tasks to skip
            limit: Maximum number of tasks to return

        Returns:
            list[Task]: List of task instances
        """
        result = await self.db.execute(select(Task).offset(skip).limit(limit))
        tasks = result.scalars().all()
        return tasks

    async def get_task(self, task_id: int):
        """Get a task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task: Task instance or None if not found
        """
        result = await self.db.execute(select(Task).filter(Task.id == task_id))
        task = result.scalar_one_or_none()
        return task

    async def create_task(self, task_create: TaskCreate):
        """Create a new task.

        Args:
            task_create: Task creation data

        Returns:
            Task: Created task instance
        """
        task = Task(**task_create.model_dump())
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update_task(self, task_id: int, task_update: TaskUpdate):
        """Update an existing task.

        Args:
            task_id: ID of task to update
            task_update: Update data (only provided fields will be updated)

        Returns:
            Task: Updated task instance or None if not found
        """
        task = await self.get_task(task_id)
        if not task:
            return None
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: int):
        """Delete a task.

        Args:
            task_id: ID of task to delete

        Returns:
            bool: True if deleted, False if not found
        """
        task = await self.get_task(task_id)
        if not task:
            return False
        await self.db.delete(task)
        await self.db.commit()
        return True

    async def get_tasks_by_status(self, status: TaskStatus):
        """Get tasks by status.

        Args:
            status: Task status to filter by

        Returns:
            list[Task]: List of tasks with specified status
        """
        result = await self.db.execute(select(Task).filter(Task.status == status))
        tasks = result.scalars().all()
        return tasks

    async def get_due_tasks(self):
        """Get tasks that are overdue (due date passed, status not DONE).

        Returns:
            list[Task]: List of overdue tasks
        """
        now = datetime.now(timezone.utc)
        result = await self.db.execute(
            select(Task).filter(Task.status != TaskStatus.DONE, Task.due_date <= now)
        )
        tasks = result.scalars().all()
        return tasks

    async def mark_overdue_tasks_done(self):
        """Mark all overdue tasks as DONE.

        Returns:
            int: Number of tasks marked as done
        """
        now_utc = datetime.now(timezone.utc)
        result = await self.db.execute(
            select(Task).filter(Task.status != TaskStatus.DONE, Task.due_date <= now_utc)
        )
        overdue_tasks = result.scalars().all()
        for task in overdue_tasks:
            task.status = TaskStatus.DONE
        if overdue_tasks:
            await self.db.commit()
        return len(overdue_tasks)
