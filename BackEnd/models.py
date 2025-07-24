from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    information = relationship("UserInformation", back_populates="user", uselist=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    job_matches = relationship("JobMatch", back_populates="user")


class UserInformation(Base):
    __tablename__ = "user_information"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone_number = Column(String(50))
    country = Column(String(100))
    state = Column(String(100))
    city = Column(String(100))
    street = Column(String(255))
    alternate_email = Column(String(255))
    resume_path = Column(String(255))

    user = relationship("User", back_populates="information")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    experiences = Column(Text)
    skills = Column(Text)
    projects = Column(Text)
    education = Column(Text)
    courses = Column(Text)
    achievements = Column(Text)
    extra_curricular = Column(Text)
    resume_filename = Column(String(255))
    resume_data = Column(Text)

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
