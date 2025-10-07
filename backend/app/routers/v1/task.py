from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from datetime import timezone

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.db.database import get_db_session
from app.services.task_service import TaskService
from app.models.task import TaskStatus
from app.workers.task import update_task_status_task, generate_short_description_task

router = APIRouter(
    prefix='/task',
    tags=['Task']
)

def get_task_service(db: Session = Depends(get_db_session)):
    return TaskService(db)

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(service: TaskService = Depends(get_task_service), skip: int = 0, limit: int = 100):
    return service.get_tasks(skip, limit)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    db_task = service.create_task(task)

    eta = db_task.due_date
    if eta.tzinfo is None:
        eta = eta.replace(tzinfo=timezone.utc)

    update_task_status_task.apply_async(args=[db_task.id], eta=eta)

    generate_short_description_task.delay(db_task.id)

    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, service: TaskService = Depends(get_task_service)):
    task = service.update_task(task_id, task_update)
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
    result = service.delete_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task successfully deleted"}

@router.get("/status/{status}", response_model=List[TaskResponse])
async def get_tasks_by_status(status: TaskStatus, service: TaskService = Depends(get_task_service)):
    return service.get_tasks_by_status(status)
