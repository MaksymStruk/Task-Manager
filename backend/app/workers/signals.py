"""Celery signal handlers for worker lifecycle management.

This module handles Celery worker signals to schedule overdue tasks
when workers start up or beat scheduler initializes.
"""

import asyncio

from celery.signals import worker_ready, beat_init

from app.db.database import get_celery_async_session_context
from app.services.task_service import TaskService
from app.log.custom_logger import custom_logger as logger


async def _schedule_due_tasks():
    """Check tasks whose due_date has passed and enqueue them in Celery (async)"""
    async with get_celery_async_session_context() as db:
        service = TaskService(db)
        due_tasks = await service.get_due_tasks()
        if due_tasks:
            from app.workers.task import update_task_status_task
            for task in due_tasks:
                logger.trace(f'Scheduling missed task {task.id} for status update')
                update_task_status_task.delay(task.id)
            logger.info(f"Scheduled {len(due_tasks)} overdue tasks for status update")
        else:
            logger.info("No overdue tasks to schedule")


def schedule_due_tasks():
    """Wrapper to run async schedule_due_tasks in sync context.
    
    This function bridges the sync Celery signal handlers with async database operations.
    """
    try:
        asyncio.run(_schedule_due_tasks())
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.error(f"[Celery Signals] Error scheduling due tasks: {exc}")


@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    """Signal handler for when Celery worker is ready.
    
    Args:
        sender: Celery worker instance
        **kwargs: Additional signal arguments
    """
    logger.info("[Celery Worker] Worker ready, checking overdue tasks...")
    schedule_due_tasks()


@beat_init.connect
def on_beat_init(sender, **kwargs):
    """Signal handler for when Celery beat scheduler initializes.
    
    Args:
        sender: Celery beat instance
        **kwargs: Additional signal arguments
    """
    logger.info("[Celery Beat] Beat initialized, checking overdue tasks...")
    schedule_due_tasks()
