from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# Create SQLAlchemy engine for PostgreSQL
# if DATABASE_URL:
#     engine = create_engine(DATABASE_URL, echo=False)
# else:
#     engine = create_engine("postgresql://postgres:password@localhost:5432/job_boost", echo=False)


engine = create_engine(DATABASE_URL, echo=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for models
class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
