"""Celery application configuration.

This module configures the Celery application for async task processing,
including broker settings, task routing, and worker configuration.
"""

import os

from celery import Celery

from app.core.config import settings

# Create celery directory for beat schedule
celery_dir = os.path.join(settings.BASE_DIR, "celery")
os.makedirs(celery_dir, exist_ok=True)
CELERYBEAT_SCHEDULE_PATH = os.path.join(celery_dir, "celerybeat-schedule")

# Initialize Celery application
celery_app = Celery(
    "taskmanager",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.workers.task']
)

# Configure Celery settings
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule_filename=CELERYBEAT_SCHEDULE_PATH,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes max
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
    worker_prefetch_multiplier=1,  # Process one task at a time
    worker_max_tasks_per_child=1000,  # Restart worker after 1000 tasks
)
