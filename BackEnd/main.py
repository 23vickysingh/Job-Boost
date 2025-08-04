from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import user, profile, jobs
from database import Base, engine
from background_tasks import start_background_tasks, stop_background_tasks


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up Job Search Assistant API...")
    await start_background_tasks()
    yield
    # Shutdown
    print("Shutting down Job Search Assistant API...")
    await stop_background_tasks()


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Search Assistant API",
    description="Backend for job search assistant platform with AI-powered resume parsing",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for the frontend
# For production, replace with specific origins
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


@app.get("/")
async def root():
    return {
        "message": "Job Search Assistant API",
        "version": "2.0.0",
        "features": ["User Authentication", "Profile Management", "AI Resume Parsing"]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "job-search-api"}
