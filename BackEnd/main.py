from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import user, profile
from database import Base, engine


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
