# project/celery_app.py

import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

# Load environment variables from .env file at the very beginning
load_dotenv()

def create_celery():
    """
    Creates and configures a Celery application instance.
    This factory pattern is useful for organizing configuration.
    """
    # Get the Redis URL from environment variables, with a default for local development
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # It's good practice to use different Redis DBs for broker and backend
    broker_url = f"{redis_url}/0"
    result_backend = f"{redis_url}/1"

    # Create the Celery application instance
    # The first argument is the name of your project's main module.
    # The 'include' argument tells Celery where to find your task modules.
    celery_app = Celery(
        'job_boost_project', # A more descriptive name for your project
        broker=broker_url,
        backend=result_backend,
        include=['tasks.job_search']
    )

    # Optional Celery configuration
    celery_app.conf.update(
        task_track_started=True,
        broker_connection_retry_on_startup=True, # Essential for robust startup
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        result_expires=3600,  # Expire results after 1 hour
        timezone='UTC',       # Use UTC for scheduling
        enable_utc=True,
    )

    # Configure the Celery Beat scheduler
    celery_app.conf.beat_schedule = {
        # A descriptive name for the scheduled task
        'run-daily-job-searches': {
            # The full path to the task function to be executed
            'task': 'tasks.job_search.schedule_daily_job_searches',
            
            # The schedule for execution. crontab(hour=3, minute=0) runs it at 3:00 AM UTC every day.
            'schedule': crontab(hour=3, minute=0),
        },
    }
    
    return celery_app

# Create the celery instance to be imported by your FastAPI app and workers
app = create_celery()
