from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, profile
from .database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Search Assistant API",
    description="Backend for job search assistant platform",
    version="1.0.0"
)

# Enable CORS (adjust origins for frontend later)
origins = [
    "http://localhost:3000",  # React frontend default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(profile.router)
