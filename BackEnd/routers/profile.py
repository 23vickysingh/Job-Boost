from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth.dependencies import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.post("/", response_model=schemas.UserProfileOut)
def create_or_update_profile(
    full_name: str = Form(...),
    interested_role: str = Form(...),
    experience: int = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    content = resume.file.read().decode("utf-8", errors="ignore")  # Plain resume text
    existing_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()

    if existing_profile:
        existing_profile.full_name = full_name
        existing_profile.interested_role = interested_role
        existing_profile.experience = experience
        existing_profile.resume_filename = resume.filename
        existing_profile.resume_data = content
    else:
        profile = models.UserProfile(
            user_id=current_user.id,
            full_name=full_name,
            interested_role=interested_role,
            experience=experience,
            resume_filename=resume.filename,
            resume_data=content
        )
        db.add(profile)

    db.commit()
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()


@router.get("/", response_model=schemas.UserProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
