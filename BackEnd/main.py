from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, profile, personal_info
from .database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Search Assistant API",
    description="Backend for job search assistant platform",
    version="1.0.0"
)

# Enable CORS for the frontend
# During local development the Vite dev server may run on a
# couple different ports depending on the environment so we
# simply allow all origins.  This keeps the example easy to run
# while still restricting allowed methods/headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(personal_info.router)
