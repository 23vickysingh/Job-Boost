from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

import models, schemas
from utils.resume_parser import extract_text_from_upload, parse_resume_details
from database import get_db
from auth.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/", response_model=schemas.UserProfileOut)
def create_or_update_profile(
    experiences: str = Form(...),
    skills: str = Form(...),
    projects: str = Form(...),
    education: str = Form(...),
    courses: str = Form(...),
    achievements: str = Form(...),
    extra_curricular: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    file_bytes = resume.file.read()
    content = extract_text_from_upload(file_bytes, resume.filename)
    parsed = parse_resume_details(content)
    existing = db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()

    if existing:
        existing.experiences = experiences
        existing.skills = skills
        existing.projects = projects
        existing.education = education
        existing.courses = courses
        existing.achievements = achievements
        existing.extra_curricular = extra_curricular
        existing.resume_filename = resume.filename
        existing.resume_data = content
    else:
        profile = models.UserProfile(
            user_id=current_user.id,
            experiences=experiences,
            skills=skills,
            projects=projects,
            education=education,
            courses=courses,
            achievements=achievements,
            extra_curricular=extra_curricular,
            resume_filename=resume.filename,
            resume_data=content,
        )
        db.add(profile)

    db.commit()
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()


@router.get("/", response_model=schemas.UserProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
