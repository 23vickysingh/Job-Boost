from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
import json
import os
from datetime import datetime

import models, schemas
from utils.resume_parser import extract_text_from_upload, parse_resume_with_gemini
from database import get_db
from auth.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/job-preferences", response_model=schemas.UserProfileOut)
async def create_job_preferences(
    preferences: schemas.JobPreferencesCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create or update user job preferences."""
    
    # Check if profile exists
    existing_profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if existing_profile:
        # Update existing profile
        existing_profile.query = preferences.query
        existing_profile.location = preferences.location
        existing_profile.mode_of_job = preferences.mode_of_job
        existing_profile.work_experience = preferences.work_experience
        existing_profile.employment_types = preferences.employment_types
        existing_profile.company_types = preferences.company_types
        existing_profile.job_requirements = preferences.job_requirements
        existing_profile.last_updated = datetime.utcnow()
        db.commit()
        db.refresh(existing_profile)
        return existing_profile
    else:
        # Create new profile
        new_profile = models.UserProfile(
            user_id=current_user.id,
            query=preferences.query,
            location=preferences.location,
            mode_of_job=preferences.mode_of_job,
            work_experience=preferences.work_experience,
            employment_types=preferences.employment_types,
            company_types=preferences.company_types,
            job_requirements=preferences.job_requirements
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile


@router.post("/upload-resume", response_model=schemas.ResumeUploadResponse)
async def upload_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Upload and parse resume."""
    
    # Validate file type
    if not resume.filename.lower().endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF, DOCX, and DOC files are supported"
        )
    
    # Create uploads directory if it doesn't exist
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(resume.filename)[1]
    unique_filename = f"{current_user.id}_{resume.filename.replace(' ', '_')}"
    file_path = os.path.join(uploads_dir, unique_filename)
    
    # Save file
    content = await resume.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Extract text from resume
    try:
        resume_text = extract_text_from_upload(content, resume.filename)
        
        # Parse resume with AI
        parsed_data = await parse_resume_with_gemini(resume_text)
        
        resume_data = {
            "filename": resume.filename,
            "text": resume_text,
            "parsed_data": parsed_data,
            "uploaded_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        # Clean up file if parsing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse resume: {str(e)}"
        )
    
    # Update or create user profile
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = models.UserProfile(user_id=current_user.id)
        db.add(profile)
    
    profile.resume_location = file_path
    profile.resume_parsed = resume_data
    profile.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(profile)
    
    return schemas.ResumeUploadResponse(
        message="Resume uploaded and parsed successfully",
        resume_location=file_path,
        status="success"
    )


@router.get("/", response_model=schemas.UserProfileOut)
async def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get user profile with user information."""
    
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        # Create empty profile if it doesn't exist
        profile = models.UserProfile(
            user_id=current_user.id,
            query=None,
            location=None,
            mode_of_job=None,
            work_experience=None,
            employment_types=None,
            company_types=None,
            job_requirements=None,
            resume_location=None,
            resume_parsed=None
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    # Create profile response with user information
    profile_dict = {
        "id": profile.id,
        "user_id": profile.user_id,
        "user_email": current_user.user_id,  # user_id field contains email
        "user_name": None,  # Extract from resume if available
        "query": profile.query,
        "location": profile.location,
        "mode_of_job": profile.mode_of_job,
        "work_experience": profile.work_experience,
        "employment_types": profile.employment_types,
        "company_types": profile.company_types,
        "job_requirements": profile.job_requirements,
        "resume_location": profile.resume_location,
        "resume_parsed": profile.resume_parsed,
        "last_updated": profile.last_updated
    }
    
    # Extract name from resume if available
    if profile.resume_parsed and isinstance(profile.resume_parsed, dict):
        personal_info = profile.resume_parsed.get("personal_info", {})
        if personal_info and personal_info.get("name"):
            profile_dict["user_name"] = personal_info["name"]
    
    return profile_dict


@router.get("/complete", response_model=schemas.CompleteUserProfile)
async def get_complete_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get complete user profile including user details."""
    
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        # Create empty profile if it doesn't exist
        profile = models.UserProfile(
            user_id=current_user.id,
            query=None,
            location=None,
            mode_of_job=None,
            work_experience=None,
            employment_types=None,
            company_types=None,
            job_requirements=None,
            resume_location=None,
            resume_parsed=None
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    # Create complete profile response
    complete_profile = {
        "id": profile.id,
        "user_id": profile.user_id,
        "user_email": current_user.user_id,  # user_id field contains email
        "user_name": None,  # Extract from resume if available
        "query": profile.query,
        "location": profile.location,
        "mode_of_job": profile.mode_of_job,
        "work_experience": profile.work_experience,
        "employment_types": profile.employment_types,
        "company_types": profile.company_types,
        "job_requirements": profile.job_requirements,
        "resume_location": profile.resume_location,
        "resume_parsed": profile.resume_parsed,
        "last_updated": profile.last_updated
    }
    
    # Extract name from resume if available
    if profile.resume_parsed and isinstance(profile.resume_parsed, dict):
        personal_info = profile.resume_parsed.get("personal_info", {})
        if personal_info and personal_info.get("name"):
            complete_profile["user_name"] = personal_info["name"]
    
    return complete_profile


@router.put("/", response_model=schemas.UserProfileOut)
async def update_profile(
    profile_update: schemas.UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update user profile."""
    
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update only provided fields
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    profile.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(profile)
    
    return profile


@router.delete("/")
async def delete_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete user profile and associated resume file."""
    
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Delete resume file if it exists
    if profile.resume_location and os.path.exists(profile.resume_location):
        try:
            os.remove(profile.resume_location)
        except Exception as e:
            print(f"Failed to delete resume file: {e}")
    
    db.delete(profile)
    db.commit()
    
    return {"message": "Profile deleted successfully"}
    if profile.resume_data and profile.resume_data.strip():
        try:
            import json
            parsed_data = json.loads(profile.resume_data)
            return {
                "status": "completed",
                "filename": profile.resume_filename,
                "message": "Resume processed successfully",
                "has_parsed_data": True
            }
        except:
            return {
                "status": "completed",
                "filename": profile.resume_filename,
                "message": "Resume processed successfully",
                "has_parsed_data": False
            }
    
    return {
        "status": "unknown",
        "filename": profile.resume_filename,
        "message": "Resume processing status unknown"
    }


@router.delete("/resume")
def delete_resume(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete uploaded resume and parsed data."""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile.resume_filename = None
    profile.resume_data = None
    db.commit()
    
    return {"message": "Resume deleted successfully"}
