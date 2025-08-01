from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    job_matches = relationship("JobMatch", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    query = Column(String(255), nullable=True)  # Job title/query
    location = Column(String(255), nullable=True)  # Job location
    mode_of_job = Column(String(50), nullable=True)  # remote, hybrid, in-place
    work_experience = Column(String(100), nullable=True)  # Experience level
    employment_types = Column(JSON, nullable=True)  # List of employment types
    company_types = Column(JSON, nullable=True)  # Company types preferences
    job_requirements = Column(Text, nullable=True)  # Additional requirements
    resume_location = Column(String(500), nullable=True)  # Path to uploaded resume
    resume_parsed = Column(JSON, nullable=True)  # Parsed resume data as JSON
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    description = Column(Text)
    apply_link = Column(String(500))

    job_matches = relationship("JobMatch", back_populates="job")


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    relevance_score = Column(Float)

    user = relationship("User", back_populates="job_matches")
    job = relationship("Job", back_populates="job_matches")
