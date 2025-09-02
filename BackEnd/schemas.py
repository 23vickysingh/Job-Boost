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


class RegistrationRequest(UserBase):
    password: str


class RegistrationVerify(BaseModel):
    user_id: EmailStr
    otp: str


class PasswordResetRequest(BaseModel):
    user_id: EmailStr


class PasswordUpdate(BaseModel):
    user_id: EmailStr
    otp: str
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    user_id: EmailStr
    password: str


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
    ats_score: Optional[float] = None
    ats_score_calculated_at: Optional[datetime] = None


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


# ---------------- Job Schemas ----------------
class JobBase(BaseModel):
    job_id: str
    employer_name: Optional[str] = None
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    job_apply_link: Optional[str] = None
    job_city: Optional[str] = None
    job_country: Optional[str] = None
    job_employment_type: Optional[str] = None
    employer_logo: Optional[str] = None
    job_is_remote: Optional[bool] = False
    job_posted_at_datetime_utc: Optional[str] = None
    job_required_skills: Optional[List[str]] = None
    job_min_salary: Optional[float] = None
    job_max_salary: Optional[float] = None
    job_salary_currency: Optional[str] = None
    job_salary_period: Optional[str] = None
    job_api_response: Optional[Dict[str, Any]] = None

class JobCreate(JobBase):
    pass

class JobOut(JobBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- Job Match Schemas ----------------
class JobMatchBase(BaseModel):
    user_id: int
    job_id: int
    relevance_score: float
    status: Optional[str] = "pending"

class JobMatchCreate(JobMatchBase):
    pass

class JobMatchOut(JobMatchBase):
    id: int
    created_at: datetime
    job: JobOut  # Nest the full job details in the response

    class Config:
        from_attributes = True


# ---------------- Contact Schemas ----------------
class ContactBase(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    contact_type: str  # feedback, query, support


class ContactCreate(ContactBase):
    pass


class ContactOut(ContactBase):
    id: int
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------------- Dashboard Stats Schema ----------------
class DashboardStats(BaseModel):
    total_matches: int
    high_relevance_jobs: int 
    recent_matches: int
    applied_jobs: int
    ats_score: Optional[float] = None
    ats_percentage: int = 0


# ---------------- Job Relevance Schemas ----------------
class RelevanceCalculationResponse(BaseModel):
    message: str
    job_match_id: int
    relevance_score: float
    relevance_percentage: int


class HighRelevanceJobMatch(BaseModel):
    id: int
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    relevance_score: Optional[float] = None
    relevance_percentage: int = 0
    location: Optional[str] = None
    created_at: datetime
    status: str


class HighRelevanceJobsResponse(BaseModel):
    message: str
    min_relevance: float
    matches: List[HighRelevanceJobMatch]