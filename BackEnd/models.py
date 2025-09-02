from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database import Base


class ContactStatus(enum.Enum):
    pending = "pending"
    resolved = "resolved"


class JobMatchStatus(enum.Enum):
    pending = "pending"
    applied = "applied"
    not_interested = "not_interested"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    job_matches = relationship("JobMatch", back_populates="user", cascade="all, delete-orphan")


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
    resume_text = Column(Text, nullable=True)  # Raw extracted text from resume
    resume_parsed = Column(JSON, nullable=True)  # Processed/structured data from Gemini AI
    ats_score = Column(Float, nullable=True)  # ATS score (0.0 to 1.0 or percentage)
    ats_score_calculated_at = Column(DateTime, nullable=True)  # When ATS score was last calculated
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Essential Fields from JSearch API
    job_id = Column(String(255), unique=True, nullable=False, index=True)
    employer_name = Column(String(255), index=True)
    job_title = Column(String(255), index=True)
    job_description = Column(Text, nullable=False)
    job_apply_link = Column(String(1024), nullable=True)
    job_city = Column(String(255), nullable=True)
    job_country = Column(String(5), nullable=True)
    job_employment_type = Column(String(255), nullable=True)
    
    # Important Optional Fields
    employer_logo = Column(String(1024), nullable=True)
    job_is_remote = Column(Boolean, default=False)
    job_posted_at_datetime_utc = Column(String(255), nullable=True)
    job_required_skills = Column(JSON, nullable=True)
    
    # Salary Information
    job_min_salary = Column(Float, nullable=True)
    job_max_salary = Column(Float, nullable=True)
    job_salary_currency = Column(String(10), nullable=True)
    job_salary_period = Column(String(50), nullable=True)

    # Store the full, raw API response for future use or debugging
    job_api_response = Column(JSON, nullable=True)
    
    # New relationship to JobMatch
    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    relevance_score = Column(Float, nullable=False)
    status = Column(Enum(JobMatchStatus), default=JobMatchStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships to easily access User and Job objects
    user = relationship("User", back_populates="job_matches")
    job = relationship("Job", back_populates="matches")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    subject = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    contact_type = Column(String(50), nullable=False)  # feedback, query, support
    status = Column(Enum(ContactStatus), default=ContactStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)