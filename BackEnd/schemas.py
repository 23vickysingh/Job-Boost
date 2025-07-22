from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ---------------- User Schemas ----------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str


class RegistrationVerify(BaseModel):
    email: EmailStr
    otp: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------- Profile Schemas ----------------

class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    interested_role: Optional[str] = None
    experience: Optional[int] = None
    skills: Optional[str] = None
    projects: Optional[str] = None
    experiences_detail: Optional[str] = None
    achievements: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    resume_filename: Optional[str] = None
    resume_data: Optional[str] = None


class UserProfileOut(UserProfileBase):
    id: int
    resume_filename: Optional[str]
    resume_data: Optional[str]

    class Config:
        from_attributes = True


# ---------------- Job Schemas ----------------

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    apply_link: str
    hr_contact: Optional[str]


class JobCreate(JobBase):
    pass


class JobOut(JobBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- Job Match Schemas ----------------

class JobMatchOut(BaseModel):
    id: int
    relevance_score: float
    job: JobOut

    class Config:
        from_attributes = True


# ---------------- Password Reset Schemas ----------------

class PasswordResetRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str


class PasswordUpdate(BaseModel):
    email: EmailStr
    otp: str
    password: str
