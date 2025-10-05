# celery-worker/celery_app.py
from celery import Celery
import os

celery_app = Celery(
    "tasks",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    include=["tasks.job_search"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Add the beat schedule
celery_app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.job_search.search_and_save_jobs',
        'schedule': 30.0,
    },
}