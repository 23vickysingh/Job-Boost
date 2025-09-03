from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine for PostgreSQL
if DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=False)
else:
    print("⚠️ Warning: DATABASE_URL not set, using fallback")
    engine = create_engine("postgresql://postgres:password@localhost:5432/job_boost", echo=False)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models - using modern SQLAlchemy 2.0+ approach
class Base(DeclarativeBase):
    pass

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
