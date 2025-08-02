from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ---------------- Resume Data Schemas ----------------
class PersonalInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    location: Optional[str] = None


class Experience(BaseModel):
    role: Optional[str] = None
    company: Optional[str] = None
    dates: Optional[str] = None
    location: Optional[str] = None
    description: List[str] = []


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    dates: Optional[str] = None
    gpa: Optional[str] = None
    location: Optional[str] = None


class Project(BaseModel):
    name: Optional[str] = None
    technologies: List[str] = []
    description: Optional[str] = None
    dates: Optional[str] = None
    link: Optional[str] = None


class ParsedResumeData(BaseModel):
    personal_info: Optional[PersonalInfo] = None
    summary: Optional[str] = None
    experience: List[Experience] = []
    education: List[Education] = []
    skills: List[str] = []
    projects: List[Project] = []
    courses_undertaken: List[str] = []
    achievements: List[str] = []
    certifications: List[str] = []


class ResumeProcessingStatus(BaseModel):
    status: str  # "processing", "completed", "failed", "no_resume"
    filename: Optional[str] = None
    message: str
    has_parsed_data: Optional[bool] = None


# ---------------- User Schemas ----------------
class UserCreate(BaseModel):
    user_id: EmailStr
    password: str


class RegistrationRequest(BaseModel):
    user_id: EmailStr
    password: str


class RegistrationVerify(BaseModel):
    user_id: EmailStr
    otp: str


class UserLogin(BaseModel):
    user_id: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    user_id: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------- User Profile Schemas ----------------
class JobPreferencesCreate(BaseModel):
    query: str  # Job title/query - required
    location: str  # Job location - required
    mode_of_job: str  # remote, hybrid, in-place - required
    work_experience: str  # Experience level - required
    employment_types: List[str]  # List of employment types - required
    company_types: Optional[List[str]] = None  # Company types preferences
    job_requirements: Optional[str] = None  # Additional requirements


class UserProfileBase(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    mode_of_job: Optional[str] = None
    work_experience: Optional[str] = None
    employment_types: Optional[List[str]] = None
    company_types: Optional[List[str]] = None
    job_requirements: Optional[str] = None
    resume_location: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfileOut(UserProfileBase):
    id: int
    user_id: int
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    resume_parsed: Optional[dict] = None
    last_updated: datetime

    class Config:
        from_attributes = True


class CompleteUserProfile(UserProfileBase):
    id: int
    user_id: int
    user_email: str
    user_name: Optional[str] = None
    resume_parsed: Optional[dict] = None
    last_updated: datetime

    class Config:
        from_attributes = True


class ResumeUploadResponse(BaseModel):
    message: str
    resume_location: str
    status: str


# ---------------- Job Schemas ----------------
class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    apply_link: str


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
    user_id: EmailStr


class OTPVerify(BaseModel):
    user_id: EmailStr
    otp: str


class PasswordUpdate(BaseModel):
    user_id: EmailStr
    otp: str
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None