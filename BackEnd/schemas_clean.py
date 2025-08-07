from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
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


# ---------------- User Schemas ----------------
class UserBase(BaseModel):
    user_id: EmailStr  # Using email as user ID


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    user_id: EmailStr
    password: str


# ---------------- OTP Schemas ----------------
class OTPRequest(BaseModel):
    email: EmailStr
    purpose: str  # 'registration' or 'password_reset'


class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str
    purpose: str


class PasswordReset(BaseModel):
    email: EmailStr
    otp_code: str
    new_password: str


# ---------------- Token Schemas ----------------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


# ---------------- Profile Schemas ----------------
class JobPreferencesBase(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    mode_of_job: Optional[str] = None
    work_experience: Optional[str] = None
    employment_types: Optional[List[str]] = None
    company_types: Optional[List[str]] = None
    job_requirements: Optional[str] = None


class JobPreferencesCreate(JobPreferencesBase):
    pass


class JobPreferencesOut(JobPreferencesBase):
    pass


class UserProfileBase(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    mode_of_job: Optional[str] = None
    work_experience: Optional[str] = None
    employment_types: Optional[List[str]] = None
    company_types: Optional[List[str]] = None
    job_requirements: Optional[str] = None
    resume_location: Optional[str] = None
    resume_text: Optional[str] = None
    resume_parsed: Optional[Dict[str, Any]] = None


class UserProfileOut(UserProfileBase):
    id: int
    user_id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True


class CompleteUserProfile(UserProfileOut):
    user_email: str
    user_name: Optional[str] = None


class ResumeUploadResponse(BaseModel):
    message: str
    filename: str
    status: str


# ---------------- API Response Schemas ----------------
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    detail: str
