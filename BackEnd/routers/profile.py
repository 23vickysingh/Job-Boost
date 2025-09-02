from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import os
from datetime import datetime

import models, schemas
from utils.resume_parser import extract_text_from_upload, parse_resume_with_gemini
from tasks.job_search import find_and_match_jobs_for_user
from database import get_db
from auth.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/test-ats")
async def test_ats_columns(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Test endpoint to verify ATS columns are working."""
    try:
        profile = _get_or_create_profile(db, current_user)
        
        # Try to update ATS score fields
        profile.ats_score = 0.85
        profile.ats_score_calculated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(profile)
        
        return {
            "message": "ATS columns are working",
            "ats_score": profile.ats_score,
            "ats_score_calculated_at": profile.ats_score_calculated_at,
            "status": "success"
        }
    except Exception as e:
        return {
            "message": f"ATS columns test failed: {str(e)}",
            "status": "error"
        }


def _get_or_create_profile(db: Session, user: models.User) -> models.UserProfile:
    """
    Retrieves a user's profile from the database. If a profile does not exist,
    it creates a new one.
    """
    profile = (
        db.query(models.UserProfile).filter(models.UserProfile.user_id == user.id).first()
    )

    if not profile:
        profile = models.UserProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


@router.post("/job-preferences", response_model=schemas.UserProfileOut)
async def create_job_preferences(
    preferences: schemas.JobPreferencesCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create or update user job preferences."""
    
    profile = _get_or_create_profile(db, current_user)

    # Update profile with new preferences
    profile.query = preferences.query
    profile.location = preferences.location
    profile.mode_of_job = preferences.mode_of_job
    profile.work_experience = preferences.work_experience
    profile.employment_types = preferences.employment_types
    profile.company_types = preferences.company_types
    profile.job_requirements = preferences.job_requirements
    profile.last_updated = datetime.utcnow()
    
    db.commit()
    db.refresh(profile)

    find_and_match_jobs_for_user.delay(current_user.id)

    return profile


@router.post("/upload-resume", response_model=schemas.ResumeUploadResponse)
async def upload_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Upload and parse resume."""
    
    # Validate file type
    allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
    file_extension = os.path.splitext(resume.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF, DOC, DOCX, or TXT file."
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, f"{current_user.id}_{resume.filename}")
    
    try:
        # Read and save file content
        content = await resume.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Extract text from uploaded file
        resume_text = extract_text_from_upload(content, resume.filename)
        
        # Parse resume with AI
        parsed_data = await parse_resume_with_gemini(resume_text)
        
    except Exception as e:
        # Clean up file if parsing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse resume: {str(e)}"
        )
    
    # Update or create user profile
    profile = _get_or_create_profile(db, current_user)
    
    profile.resume_location = file_path
    profile.resume_text = resume_text
    profile.resume_parsed = parsed_data
    
    db.commit()
    db.refresh(profile)
    
    # Calculate ATS score after resume upload
    from services.ats_service import calculate_and_update_ats_score
    try:
        import asyncio
        ats_score = await calculate_and_update_ats_score(current_user.id, db)
        print(f"Calculated ATS score: {ats_score}")
    except Exception as e:
        print(f"Failed to calculate ATS score: {e}")
    
    return schemas.ResumeUploadResponse(
        message="Resume uploaded and parsed successfully",
        filename=resume.filename,
        status="success"
    )


@router.get("/", response_model=schemas.UserProfileOut)
async def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get user profile with ATS score calculation if needed."""
    profile = _get_or_create_profile(db, current_user)
    
    # Calculate ATS score if it's null and we have resume data
    if (profile.ats_score is None and 
        (profile.resume_text or profile.resume_parsed)):
        from services.ats_service import calculate_and_update_ats_score
        try:
            ats_score = await calculate_and_update_ats_score(current_user.id, db)
            print(f"Calculated ATS score for profile fetch: {ats_score}")
        except Exception as e:
            print(f"Failed to calculate ATS score in profile fetch: {e}")
    
    return profile


@router.get("/resume-status")
async def get_resume_status(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get resume upload status."""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile or not profile.resume_location:
        return {
            "has_resume": False,
            "message": "No resume uploaded"
        }
    
    # Check if file exists
    file_exists = os.path.exists(profile.resume_location) if profile.resume_location else False
    
    return {
        "has_resume": True,
        "file_exists": file_exists,
        "resume_parsed": profile.resume_parsed is not None,
        "message": "Resume found" if file_exists else "Resume file not found on disk"
    }


@router.delete("/resume")
async def delete_resume(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete uploaded resume."""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Delete file from disk
    if profile.resume_location and os.path.exists(profile.resume_location):
        try:
            os.remove(profile.resume_location)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to delete resume file: {e}")
    
    # Clear resume data from database
    profile.resume_location = None
    profile.resume_text = None
    profile.resume_parsed = None
    
    db.commit()
    
    return {"message": "Resume deleted successfully"}


@router.get("/complete", response_model=schemas.CompleteUserProfile)
async def get_complete_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get complete user profile including user details."""
    
    profile = _get_or_create_profile(db, current_user)
    
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
        "resume_text": profile.resume_text,
        "resume_parsed": profile.resume_parsed,
        "last_updated": profile.last_updated
    }
    
    # Extract name from resume if available
    if profile.resume_parsed:
        try:
            personal_info = profile.resume_parsed.get("personal_information", {})
            complete_profile["user_name"] = personal_info.get("name")
        except (AttributeError, TypeError):
            pass
    
    return complete_profile


@router.put("/ats-score")
async def update_ats_score(
    ats_score: float,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update user's ATS score."""
    
    # Validate ATS score range
    if not (0.0 <= ats_score <= 1.0):
        raise HTTPException(status_code=400, detail="ATS score must be between 0.0 and 1.0")
    
    profile = _get_or_create_profile(db, current_user)
    
    # Update ATS score and timestamp
    profile.ats_score = ats_score
    profile.ats_score_calculated_at = datetime.utcnow()
    profile.last_updated = datetime.utcnow()
    
    db.commit()
    db.refresh(profile)
    
    return {
        "message": "ATS score updated successfully",
        "ats_score": profile.ats_score,
        "ats_score_calculated_at": profile.ats_score_calculated_at
    }


@router.get("/ats-score")
async def get_ats_score(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get or calculate ATS score for current user."""
    
    from services.ats_service import get_or_calculate_ats_score
    
    try:
        ats_score = get_or_calculate_ats_score(current_user.id, db)
        
        if ats_score is None:
            return {
                "message": "Unable to calculate ATS score. Please upload a resume first.",
                "ats_score": None,
                "status": "no_resume"
            }
        
        # Get the updated profile
        profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == current_user.id
        ).first()
        
        return {
            "message": "ATS score retrieved successfully",
            "ats_score": ats_score,
            "ats_score_calculated_at": profile.ats_score_calculated_at,
            "ats_percentage": int(ats_score * 100),
            "status": "success"
        }
        
    except Exception as e:
        return {
            "message": f"Error getting ATS score: {str(e)}",
            "ats_score": None,
            "status": "error"
        }
