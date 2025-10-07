"""Celery task definitions for async task processing.

This module defines Celery tasks that handle async operations
using asyncio.run() to bridge sync Celery with async database operations.
"""

import asyncio
from datetime import datetime, timezone

from app.workers.celery_app import celery_app
from app.db.database import get_celery_async_session_context
from app.services.task_service import TaskService
from app.log.custom_logger import custom_logger as logger
from app.models.task import TaskStatus


async def _update_task_status(task_id: int):
    """Async helper function to update task status based on due date.
    
    Args:
        task_id: ID of task to update
        
    Returns:
        dict: Result with 'success' or 'error' key
    """
    async with get_celery_async_session_context() as db:
        service = TaskService(db)
        task = await service.get_task(task_id)
        if not task:
            return {'error': f'Task {task_id} not found'}

        now_utc = datetime.now(timezone.utc)
        task_due = task.due_date
        if task_due.tzinfo is None:
            task_due = task_due.replace(tzinfo=timezone.utc)

        if now_utc >= task_due:
            task.status = TaskStatus.DONE
            await db.commit()
            logger.trace(f'Task {task_id} status updated to DONE')
            return {'success': f'Task {task_id} status updated to DONE'}

        logger.trace(f'Task {task_id} due date not yet reached')
        return {'success': f'Task {task_id} due date not yet reached'}


@celery_app.task(bind=True, name='update_task_status')
def update_task_status_task(self, task_id: int):
    """Celery task to update task status when due date is reached.
    
    Args:
        task_id: ID of task to update
        
    Returns:
        str: Success or error message
    """
    try:
        result = asyncio.run(_update_task_status(task_id))
        if 'error' in result:
            self.update_state(state='FAILURE', meta={'error': result['error']})
            return result['error']
        return result['success']
    except Exception as exc:
        self.update_state(state='FAILURE', meta={'error': str(exc)})
        logger.critical(f'Error updating task {task_id}: {exc}')
        raise


async def _generate_short_description(task_id: int):
    """Async helper function to generate short description for task.
    
    Args:
        task_id: ID of task to generate description for
        
    Returns:
        dict: Result with 'success' or 'error' key
    """
    async with get_celery_async_session_context() as db:
        service = TaskService(db)
        task = await service.get_task(task_id)
        if not task:
            return {'error': f'Task {task_id} not found'}

        # Generate short description from task text
        short_description = (task.text[:100] + "...") if task.text else "Lorem ipsum dolor sit amet"
        task.short_description = short_description
        await db.commit()
        logger.trace(f'Short description generated for task {task_id}')
        return {'success': f'Short description generated for task {task_id}: {short_description}'}


@celery_app.task(bind=True, name='generate_short_description')
def generate_short_description_task(self, task_id: int):
    """Celery task to generate short description for a task.
    
    Args:
        task_id: ID of task to generate description for
        
    Returns:
        str: Success or error message
    """
    try:
        result = asyncio.run(_generate_short_description(task_id))
        if 'error' in result:
            self.update_state(state='FAILURE', meta={'error': result['error']})
            return result['error']
        return result['success']
    except Exception as exc:
        self.update_state(state='FAILURE', meta={'error': str(exc)})
        logger.critical(f'Error generating description for task {task_id}: {exc}')
        raise
