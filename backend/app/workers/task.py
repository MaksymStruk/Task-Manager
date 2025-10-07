from app.workers.celery_app import celery_app
from app.db.database import get_celery_db_session
from app.services.task_service import TaskService
from app.log.custom_logger import custom_logger as logger
from datetime import datetime, timezone
from app.models.task import TaskStatus

@celery_app.task(bind=True, name='update_task_status')
def update_task_status_task(self, task_id: int):
    db = get_celery_db_session()
    service = TaskService(db)
    try:
        task = service.get_task(task_id)
        if not task:
            self.update_state(state='FAILURE', meta={'error': f'Task {task_id} not found'})
            return f'Task {task_id} not found'

        now_utc = datetime.now(timezone.utc)
        task_due = task.due_date
        if task_due.tzinfo is None:
            task_due = task_due.replace(tzinfo=timezone.utc)

        if now_utc >= task_due:
            task.status = TaskStatus.DONE
            db.commit()
            logger.trace(f'Task {task_id} status updated to DONE')
            return f'Task {task_id} status updated to DONE'
        else:
            logger.trace(f'Task {task_id} due date not yet reached')
            return f'Task {task_id} due date not yet reached'
    except Exception as exc:
        self.update_state(state='FAILURE', meta={'error': str(exc)})
        logger.critical(f'Error updating task {task_id}: {exc}')
        raise exc
    finally:
        db.close()


@celery_app.task(bind=True, name='generate_short_description')
def generate_short_description_task(self, task_id: int):
    db = get_celery_db_session()
    service = TaskService(db)
    try:
        task = service.get_task(task_id)
        if not task:
            self.update_state(state='FAILURE', meta={'error': f'Task {task_id} not found'})
            return f'Task {task_id} not found'

        # Генеруємо короткий опис
        short_description = (task.text[:100] + "...") if task.text else "Lorem ipsum dolor sit amet"
        task.short_description = short_description
        db.commit()
        logger.trace(f'Short description generated for task {task_id}')
        return f'Short description generated for task {task_id}: {short_description}'

    except Exception as exc:
        self.update_state(state='FAILURE', meta={'error': str(exc)})
        logger.critical(f'Error generating description for task {task_id}: {exc}')
        raise exc
    finally:
        db.close()