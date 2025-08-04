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
    job_matching: Optional[dict] = None


# ---------------- Job Schemas ----------------
class JobBase(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    description: Optional[str] = None
    apply_link: str
    job_employment_type: Optional[str] = None
    job_city: Optional[str] = None
    job_state: Optional[str] = None
    job_country: Optional[str] = None
    job_latitude: Optional[float] = None
    job_longitude: Optional[float] = None
    job_benefits: Optional[List[str]] = None
    job_google_link: Optional[str] = None
    job_offer_expiration_datetime_utc: Optional[str] = None
    job_required_experience: Optional[dict] = None
    job_required_skills: Optional[List[str]] = None
    job_required_education: Optional[dict] = None
    job_experience_in_place_of_education: Optional[str] = None
    job_min_salary: Optional[float] = None
    job_max_salary: Optional[float] = None
    job_salary_currency: Optional[str] = None
    job_salary_period: Optional[str] = None
    job_highlights: Optional[dict] = None
    job_job_title: Optional[str] = None
    job_posting_language: Optional[str] = None
    job_onet_soc: Optional[str] = None
    job_onet_job_zone: Optional[str] = None
    job_naics_code: Optional[str] = None
    job_naics_name: Optional[str] = None
    employer_logo: Optional[str] = None
    employer_website: Optional[str] = None
    employer_company_type: Optional[str] = None
    employer_reviews_count: Optional[int] = None
    employer_rating: Optional[float] = None


class JobCreate(JobBase):
    pass


class JobOut(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobMatchRequest(BaseModel):
    user_id: Optional[int] = None  # If not provided, use current user


class JobMatchingResult(BaseModel):
    message: str
    jobs_processed: int
    matches_created: int
    user_id: int


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