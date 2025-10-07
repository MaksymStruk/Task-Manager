from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def get_tasks(self, skip: int = 0, limit: int = 100):
        return self.db.query(Task).offset(skip).limit(limit).all()

    def get_task(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create_task(self, task_create: TaskCreate):
        task = Task(**task_create.model_dump())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(self, task_id: int, task_update: TaskUpdate):
        task = self.get_task(task_id)
        if not task:
            return None
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int):
        task = self.get_task(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True

    def get_tasks_by_status(self, status: TaskStatus):
        return self.db.query(Task).filter(Task.status == status).all()

    def get_due_tasks(self):
        now = datetime.now(timezone.utc)
        return self.db.query(Task).filter(
            Task.status != TaskStatus.DONE,
            Task.due_date <= now
        ).all()
    
    def mark_overdue_tasks_done(self):
        """Marks all overdue tasks as DONE"""
        now_utc = datetime.now(timezone.utc)
        overdue_tasks = (
            self.db.query(Task)
            .filter(Task.status != TaskStatus.DONE)
            .filter(Task.due_date <= now_utc)
            .all()
        )
        for task in overdue_tasks:
            task.status = TaskStatus.DONE
        if overdue_tasks:
            self.db.commit()
        return len(overdue_tasks)
