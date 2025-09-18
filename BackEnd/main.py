from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import tasks.job_search as job_search_tasks
from database import get_db

from routers import user, profile, jobs, contact
from database import Base, engine

load_dotenv()

# create the database table based on models.py if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Boost API",
    description="Backend API for Job Boost application",
    version="1.2.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(profile.router)
app.include_router(jobs.router)
app.include_router(contact.router)


@app.get("/")
def root():
    return {
        "message": "Job Boost API",
        "version": app.version,
        "features": "Job search, User profiles, Resume parsing, Email notifications, Job matches, Contact forms"
    }


# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "service": "job-boost-api"}




# endpoint to manually trigger the daily job search task

@app.post("/trigger-daily-search/")
def trigger_search(db: Session = Depends(get_db)):
    
    print("API endpoint called, triggering Celery task...")
    
    # Use .delay() to send the task to the Celery queue
    task = job_search_tasks.schedule_daily_job_searches.delay()
    
    return {
        "message": "Daily job search task has been triggered.",
        "task_id": task.id
    }
