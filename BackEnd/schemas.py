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


# ---------------- User Information Schemas ----------------
class UserInformationBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    alternate_email: Optional[EmailStr] = None
    resume_path: Optional[str] = None


class UserInformationCreate(UserInformationBase):
    pass


class UserInformationOut(UserInformationBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- Profile Schemas ----------------
class UserProfileBase(BaseModel):
    experiences: Optional[str] = None
    skills: Optional[str] = None
    projects: Optional[str] = None
    education: Optional[str] = None
    courses: Optional[str] = None
    achievements: Optional[str] = None
    extra_curricular: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    resume_filename: Optional[str] = None
    resume_data: Optional[str] = None


class UserProfileOut(UserProfileBase):
    id: int
    resume_filename: Optional[str] = None
    resume_data: Optional[str] = None

    class Config:
        from_attributes = True


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