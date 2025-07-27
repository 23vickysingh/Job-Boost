from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import os

SQL_ALCHEMY_DATABASE_URL = os.getenv("DOCKER_DATABASE_URL")

# Update these as per your local MySQL config
# DB_USER = "developer"
# DB_PASSWORD = "password"
# DB_HOST = "localhost"
# DB_PORT = "3306"
# DB_NAME = "fastapi_db"

# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models - using modern SQLAlchemy 2.0+ approach
class Base(DeclarativeBase):
    pass

# For example use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
