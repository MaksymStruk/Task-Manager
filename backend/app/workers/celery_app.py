import os
from app.core.config import settings
from celery import Celery

celery_dir = os.path.join(settings.BASE_DIR, "celery")
os.makedirs(celery_dir, exist_ok=True)
CELERYBEAT_SCHEDULE_PATH = os.path.join(celery_dir, "celerybeat-schedule")

# Initialize Celery
celery_app = Celery(
    "taskmanager",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.workers.task']
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule_filename=CELERYBEAT_SCHEDULE_PATH,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)