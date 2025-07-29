from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
import asyncio
import json
from datetime import datetime

import models, schemas
from utils.resume_parser import extract_text_from_upload, parse_resume_details
from database import get_db, ElasticsearchSync
from auth.dependencies import get_current_user
from background_tasks import get_resume_processor

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/", response_model=schemas.UserProfileOut)
async def create_or_update_profile(
    experiences: str = Form(""),
    skills: str = Form(""),
    projects: str = Form(""),
    education: str = Form(""),
    courses: str = Form(""),
    achievements: str = Form(""),
    extra_curricular: str = Form(""),
    resume: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create or update user profile with optional resume processing."""
    
    # Get existing profile or create new one
    existing = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if existing:
        # Update existing profile
        existing.experiences = experiences
        existing.skills = skills
        existing.projects = projects
        existing.education = education
        existing.courses = courses
        existing.achievements = achievements
        existing.extra_curricular = extra_curricular
        
        if resume:
            existing.resume_filename = resume.filename
            # Store basic file info immediately
            file_bytes = await resume.read()
            existing.resume_data = f"Processing resume: {resume.filename}"
            db.commit()
            
            # Add to background processing queue
            resume_processor = get_resume_processor()
            await resume_processor.add_resume_to_queue(
                current_user.id, file_bytes, resume.filename
            )
        else:
            db.commit()
    else:
        # Create new profile
        profile = models.UserProfile(
            user_id=current_user.id,
            experiences=experiences,
            skills=skills,
            projects=projects,
            education=education,
            courses=courses,
            achievements=achievements,
            extra_curricular=extra_curricular,
            resume_filename=resume.filename if resume else None,
            resume_data="Processing resume..." if resume else None,
        )
        db.add(profile)
        db.commit()
        
        if resume:
            # Add to background processing queue
            file_bytes = await resume.read()
            resume_processor = get_resume_processor()
            await resume_processor.add_resume_to_queue(
                current_user.id, file_bytes, resume.filename
            )
    
    # Return updated profile
    updated_profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    # Sync to Elasticsearch
    try:
        profile_data = {
            "experiences": updated_profile.experiences or "",
            "skills": updated_profile.skills or "",
            "projects": updated_profile.projects or "",
            "education": updated_profile.education or "",
            "courses": updated_profile.courses or "",
            "achievements": updated_profile.achievements or "",
            "extra_curricular": updated_profile.extra_curricular or "",
            "resume_filename": updated_profile.resume_filename,
            "updated_at": datetime.utcnow().isoformat()
        }
        es_sync = ElasticsearchSync()
        await es_sync.sync_user_profile(current_user.id, profile_data)
    except Exception as e:
        print(f"Failed to sync profile to Elasticsearch: {e}")
    
    return updated_profile


@router.post("/upload-resume", response_model=dict)
async def upload_resume_only(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Upload and process resume independently."""
    
    if not resume.filename.lower().endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF, DOCX, and DOC files are supported"
        )
    
    # Get or create profile
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = models.UserProfile(user_id=current_user.id)
        db.add(profile)
    
    # Update resume info
    profile.resume_filename = resume.filename
    profile.resume_data = "Processing resume..."
    db.commit()
    
    # Read file and add to processing queue
    file_bytes = await resume.read()
    resume_processor = get_resume_processor()
    await resume_processor.add_resume_to_queue(
        current_user.id, file_bytes, resume.filename
    )
    
    # Sync to Elasticsearch
    es_sync = ElasticsearchSync()
    try:
        await es_sync.sync_user_profile(current_user.id, {
            "user_id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "resume_filename": profile.resume_filename,
            "updated_at": datetime.utcnow().isoformat()
        })
    except Exception as e:
        print(f"Elasticsearch sync failed: {e}")
    
    return {
        "message": "Resume uploaded successfully and is being processed",
        "filename": resume.filename,
        "status": "processing"
    }


@router.get("/", response_model=schemas.UserProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get user profile."""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile


@router.get("/resume-status", response_model=dict)
def get_resume_processing_status(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Check the status of resume processing."""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile or not profile.resume_filename:
        return {"status": "no_resume", "message": "No resume uploaded"}
    
    # Check if resume is still being processed
    if profile.resume_data and "Processing" in profile.resume_data:
        return {
            "status": "processing",
            "filename": profile.resume_filename,
            "message": "Resume is being processed"
        }
    
    # Check if processing completed successfully
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
