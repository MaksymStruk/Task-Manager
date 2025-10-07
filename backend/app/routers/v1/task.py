"""Task API endpoints for CRUD operations.

This module provides REST API endpoints for task management,
including creation, retrieval, updates, and deletion of tasks.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.db.database import get_db_session
from app.services.task_service import TaskService
from app.models.task import TaskStatus
from app.workers.task import update_task_status_task, generate_short_description_task

router = APIRouter(
    prefix='/task',
    tags=['Task']
)

def get_task_service(db: AsyncSession = Depends(get_db_session)):
    """Dependency to get TaskService instance.

    Args:
        db: Database session dependency

    Returns:
        TaskService: Service instance with database session
    """
    return TaskService(db)

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(service: TaskService = Depends(get_task_service), skip: int = 0, limit: int = 100):
    """Get all tasks with pagination.

    Retrieve a list of tasks with optional pagination parameters.

    Query Parameters:
        skip (int, optional): Number of tasks to skip for pagination. Defaults to 0.
        limit (int, optional): Maximum number of tasks to return. Defaults to 100.

    Returns:
        List[TaskResponse]: List of tasks with their details

    Example:
        GET /api/v1/task/?skip=0&limit=10
    """
    tasks = await service.get_tasks(skip, limit)
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """Get a specific task by ID.

    Retrieve detailed information about a single task.

    Path Parameters:
        task_id (int): The unique identifier of the task

    Returns:
        TaskResponse: Complete task details including:
            - id: Task identifier
            - title: Task title
            - description: Task description
            - text: Detailed task content
            - due_date: When the task should be completed
            - status: Current status (PENDING/DONE)
            - created_at: When the task was created
            - updated_at: When the task was last updated
            - short_description: Auto-generated summary

    Raises:
        HTTPException: 404 if task with given ID is not found

    Example:
        GET /api/v1/task/123
    """
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    """Create a new task.

    Create a new task with the provided details. The task will be automatically
    scheduled for status updates based on its due date.

    Request Body (TaskCreate):
        title (str, required): Task title (1-255 characters)
        description (str, optional): Brief task description
        text (str, optional): Detailed task content
        due_date (datetime, required): When the task should be completed (ISO format)
        status (TaskStatus, optional): Initial status, defaults to "PENDING"

    Returns:
        TaskResponse: Created task with auto-generated ID and timestamps

    Example:
        POST /api/v1/task/
        {
            "title": "Complete project documentation",
            "description": "Write comprehensive docs",
            "text": "Create detailed API documentation with examples...",
            "due_date": "2025-12-31T23:59:59Z",
            "status": "PENDING"
        }
    """
    db_task = await service.create_task(task)

    eta = db_task.due_date
    if eta.tzinfo is None:
        eta = eta.replace(tzinfo=timezone.utc)

    update_task_status_task.apply_async(args=[db_task.id], eta=eta)
    generate_short_description_task.delay(db_task.id)

    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, service: TaskService = Depends(get_task_service)):
    """Update an existing task.

    Update one or more fields of an existing task. Only provided fields will be updated.
    If the due_date is changed, the task will be rescheduled automatically.

    Path Parameters:
        task_id (int): The unique identifier of the task to update

    Request Body (TaskUpdate) - all fields optional:
        title (str, optional): New task title (1-255 characters)
        description (str, optional): New task description
        text (str, optional): New detailed task content
        due_date (datetime, optional): New due date (ISO format)
        status (TaskStatus, optional): New status (PENDING/DONE)
        short_description (str, optional): New short description

    Returns:
        TaskResponse: Updated task with new values and updated timestamp

    Raises:
        HTTPException: 404 if task with given ID is not found

    Example:
        PUT /api/v1/task/123
        {
            "title": "Updated task title",
            "due_date": "2025-12-25T12:00:00Z",
            "status": "DONE"
        }
    """
    task = await service.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_update.due_date:
        eta = task_update.due_date
        if eta.tzinfo is None:
            eta = eta.replace(tzinfo=timezone.utc)
        update_task_status_task.apply_async(args=[task.id], eta=eta)

    return task

@router.delete("/{task_id}")
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """Delete a task.

    Permanently delete a task from the system. This action cannot be undone.

    Path Parameters:
        task_id (int): The unique identifier of the task to delete

    Returns:
        dict: Success message confirming deletion

    Raises:
        HTTPException: 404 if task with given ID is not found

    Example:
        DELETE /api/v1/task/123

    Response:
        {
            "message": "Task successfully deleted"
        }
    """
    result = await service.delete_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task successfully deleted"}

@router.get("/status/{status}", response_model=List[TaskResponse])
async def get_tasks_by_status(status: TaskStatus, service: TaskService = Depends(get_task_service)):
    """Get tasks filtered by status.

    Retrieve all tasks that have a specific status.

    Path Parameters:
        status (TaskStatus): Filter by task status
            - "pending": Tasks that are waiting to be completed
            - "done": Tasks that have been completed

    Returns:
        List[TaskResponse]: List of tasks with the specified status

    Example:
        GET /api/v1/task/status/pending
        GET /api/v1/task/status/done
    """
    tasks = await service.get_tasks_by_status(status)
    return tasks