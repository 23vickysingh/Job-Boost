from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL Database Configuration
POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")

# Create SQLAlchemy engine for PostgreSQL
if POSTGRES_DATABASE_URL:
    engine = create_engine(POSTGRES_DATABASE_URL, echo=False)
else:
    print("⚠️ Warning: POSTGRES_DATABASE_URL not set, using fallback")
    engine = create_engine("postgresql://user:password@localhost:5432/job_boost_db", echo=False)

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
