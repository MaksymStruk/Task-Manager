from celery.signals import worker_ready, beat_init
from app.db.database import get_celery_db_session
from app.services.task_service import TaskService
from app.log.custom_logger import custom_logger as logger

def schedule_due_tasks():
    """Check tasks whose due_date has passed and enqueue them in Celery"""
    db = get_celery_db_session()
    service = TaskService(db)
    try:
        due_tasks = service.get_due_tasks()
        if due_tasks:
            from app.workers.task import update_task_status_task
            for task in due_tasks:
                logger.trace(f'Scheduling missed task {task.id} for status update')
                update_task_status_task.delay(task.id)
            logger.info(f"Scheduled {len(due_tasks)} overdue tasks for status update")
        else:
            logger.info("No overdue tasks to schedule")
    finally:
        db.close()


@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    logger.info("[Celery Worker] Worker ready, checking overdue tasks...")
    schedule_due_tasks()


@beat_init.connect
def on_beat_init(sender, **kwargs):
    logger.info("[Celery Beat] Beat initialized, checking overdue tasks...")
    schedule_due_tasks()
