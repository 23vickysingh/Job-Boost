from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    job_matches = relationship("JobMatch", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    full_name = Column(String(255))
    interested_role = Column(String(255))
    experience = Column(Integer)
    resume_filename = Column(String(255))
    resume_data = Column(Text)  # Raw or parsed resume content

    user = relationship("User", back_populates="profile")


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    description = Column(Text)
    apply_link = Column(String(500))
    hr_contact = Column(String(255))

    job_matches = relationship("JobMatch", back_populates="job")


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    relevance_score = Column(Float)  # Later filled via utils.matcher

    user = relationship("User", back_populates="job_matches")
    job = relationship("Job", back_populates="job_matches")


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    otp = Column(String(6))
    expires_at = Column(DateTime)
    is_verified = Column(Boolean, default=False)

    user = relationship("User")
