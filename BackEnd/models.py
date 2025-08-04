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
    last_job_search = Column(DateTime, nullable=True)  # Track when jobs were last searched/updated

    user = relationship("User", back_populates="profile")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(255), unique=True, nullable=False, index=True)  # JSearch job_id
    title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    description = Column(Text)
    apply_link = Column(String(500))
    # Additional fields from JSearch API
    job_employment_type = Column(String(100))  # FULLTIME, PARTTIME, etc.
    job_city = Column(String(255))
    job_state = Column(String(255))
    job_country = Column(String(255))
    job_latitude = Column(Float)
    job_longitude = Column(Float)
    job_benefits = Column(JSON)  # Array of benefits
    job_google_link = Column(String(500))
    job_offer_expiration_datetime_utc = Column(String(255))
    job_required_experience = Column(JSON)  # Required experience details
    job_required_skills = Column(JSON)  # Array of required skills
    job_required_education = Column(JSON)  # Education requirements
    job_experience_in_place_of_education = Column(String(10))  # true/false
    job_min_salary = Column(Float)
    job_max_salary = Column(Float)
    job_salary_currency = Column(String(10))
    job_salary_period = Column(String(50))  # YEAR, MONTH, etc.
    job_highlights = Column(JSON)  # Qualifications, Responsibilities, Benefits
    job_job_title = Column(String(255))
    job_posting_language = Column(String(10))
    job_onet_soc = Column(String(50))
    job_onet_job_zone = Column(String(10))
    job_naics_code = Column(String(20))
    job_naics_name = Column(String(255))
    employer_logo = Column(String(500))
    employer_website = Column(String(500))
    employer_company_type = Column(String(100))
    employer_reviews_count = Column(Integer)
    employer_rating = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job_matches = relationship("JobMatch", back_populates="job")


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    relevance_score = Column(Float)

    user = relationship("User", back_populates="job_matches")
    job = relationship("Job", back_populates="job_matches")
