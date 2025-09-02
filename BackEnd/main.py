from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import tasks.job_search as job_search_tasks
from database import get_db

from routers import user, profile, jobs, contact
from database import Base, engine

# Load environment variables from .env file
load_dotenv()

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Boost API",
    description="Backend API for Job Boost application",
    version="1.0.0"
)

# Enable CORS for the frontend
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative dev port
    "http://frontend:80",     # Docker frontend service
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(jobs.router)
app.include_router(contact.router)


@app.get("/")
async def root():
    return {
        "message": "Job Boost API",
        "version": "1.0.0",
        "features": ["User Authentication", "Profile Management", "Resume Upload", "AI Resume Parsing"]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "job-boost-api"}


@app.post("/trigger-daily-search/")
def trigger_search(db: Session = Depends(get_db)):
    """
    An API endpoint to manually trigger the daily job search task.
    """
    print("API endpoint called, triggering Celery task...")
    
    # Use .delay() to send the task to the Celery queue
    task = job_search_tasks.schedule_daily_job_searches.delay()
    
    return {
        "message": "Daily job search task has been triggered.",
        "task_id": task.id
    }
