from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean
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
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class OTPVerification(Base):
    __tablename__ = "otp_verification"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    otp_code = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)
    purpose = Column(String(50))  # 'registration', 'password_reset'
