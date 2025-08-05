from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db
from auth.dependencies import get_current_user
from services.job_matcher import get_job_matching_service
from services.job_scheduler import get_job_scheduler

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/match", response_model=schemas.JobMatchingResult)
async def trigger_job_matching(
    background_tasks: BackgroundTasks,
    request: schemas.JobMatchRequest = schemas.JobMatchRequest(),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Trigger job matching process for the current user or specified user.
    This will:
    1. Fetch jobs from JSearch API based on user preferences
    2. Get detailed job descriptions
    3. Calculate relevance scores against user's resume
    4. Save results to database
    """
    
    # Determine which user to process
    target_user_id = request.user_id if request.user_id else current_user.id
    
    # Verify the user has permission to trigger matching for the target user
    if request.user_id and request.user_id != current_user.id:
        # Add admin check here if needed
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to trigger job matching for other users"
        )
    
    # Get job matching service
    job_service = get_job_matching_service()
    if not job_service:
        raise HTTPException(
            status_code=500,
            detail="Job matching service not available. Please check JSEARCH_API_KEY environment variable."
        )
    
    
    # Process job matching
    result = job_service.process_job_matching_for_user(target_user_id, db)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return schemas.JobMatchingResult(
        message=result["message"],
        jobs_processed=result["jobs_processed"],
        matches_created=result["matches_created"],
        user_id=target_user_id
    )


@router.get("/matches", response_model=List[schemas.JobMatchOut])
async def get_user_job_matches(
    limit: int = 10,
    min_score: float = 0.0,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Get job matches for the current user, sorted by relevance score.
    
    Args:
        limit: Maximum number of matches to return (default: 10)
        min_score: Minimum relevance score filter (default: 0.0)
    """
    
    matches = db.query(models.JobMatch).filter(
        models.JobMatch.user_id == current_user.id,
        models.JobMatch.relevance_score >= min_score
    ).order_by(models.JobMatch.relevance_score.desc()).limit(limit).all()
    
    
    return matches


@router.get("/matches/{job_match_id}", response_model=schemas.JobMatchOut)
async def get_job_match_details(
    job_match_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get detailed information about a specific job match."""
    
    match = db.query(models.JobMatch).filter(
        models.JobMatch.id == job_match_id,
        models.JobMatch.user_id == current_user.id
    ).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Job match not found")
    
    return match


@router.delete("/matches/{job_match_id}")
async def delete_job_match(
    job_match_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete a specific job match."""
    
    match = db.query(models.JobMatch).filter(
        models.JobMatch.id == job_match_id,
        models.JobMatch.user_id == current_user.id
    ).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Job match not found")
    
    db.delete(match)
    db.commit()
    
    
    return {"message": "Job match deleted successfully"}


@router.get("/", response_model=List[schemas.JobOut])
async def get_jobs(
    limit: int = 20,
    title_search: str = None,
    company_search: str = None,
    location_search: str = None,
    db: Session = Depends(get_db),
):
    """
    Get jobs from database with optional filtering.
    
    Args:
        limit: Maximum number of jobs to return
        title_search: Filter by job title (partial match)
        company_search: Filter by company name (partial match)
        location_search: Filter by location (partial match)
    """
    
    query = db.query(models.Job)
    
    if title_search:
        query = query.filter(models.Job.title.ilike(f"%{title_search}%"))
    
    if company_search:
        query = query.filter(models.Job.company.ilike(f"%{company_search}%"))
    
    if location_search:
        query = query.filter(models.Job.location.ilike(f"%{location_search}%"))
    
    jobs = query.order_by(models.Job.created_at.desc()).limit(limit).all()
    
    
    return jobs


@router.get("/{job_id}", response_model=schemas.JobOut)
async def get_job_details(
    job_id: int,
    db: Session = Depends(get_db),
):
    """Get detailed information about a specific job."""
    
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@router.post("/test-api")
async def test_jsearch_api():
    """Test endpoint to verify JSearch API connectivity."""
    
    job_service = get_job_matching_service()
    if not job_service:
        raise HTTPException(
            status_code=500,
            detail="Job matching service not available. Please check JSEARCH_API_KEY environment variable."
        )
    
    # Test with a simple search
    test_results = job_service.search_jobs("Software Engineer", "USA")
    
    if test_results:
        return {
            "status": "success",
            "message": "JSearch API is working",
            "jobs_found": len(test_results.get("data", [])),
            "api_response_keys": list(test_results.keys())
        }
    else:
        return {
            "status": "error",
            "message": "Failed to connect to JSearch API",
            "jobs_found": 0
        }


@router.post("/scheduler/force-update-all")
async def force_update_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Force job updates for all eligible users (admin function).
    This bypasses the 24-hour threshold and updates all users immediately.
    """
    
    
    try:
        # Get job scheduler
        scheduler = get_job_scheduler()
        
        # Force update all users
        await scheduler.force_update_all_users()
        
        return {
            "status": "success",
            "message": "Force update completed for all eligible users",
            "triggered_by": current_user.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Force update failed: {str(e)}"
        )


@router.get("/scheduler/status")
async def get_scheduler_status():
    """Get the current status of the job scheduler."""
    
    scheduler = get_job_scheduler()
    
    return {
        "scheduler_running": scheduler.is_running,
        "check_interval_hours": scheduler.check_interval / 3600,
        "user_threshold_hours": scheduler.user_threshold / 3600,
        "next_check": "Every 12 hours while running"
    }


@router.get("/stats")
async def get_job_statistics(
    db: Session = Depends(get_db)
):
    """Get statistics about jobs and matches in the system."""
    
    try:
        # Count total jobs
        total_jobs = db.query(models.Job).count()
        
        # Count total matches
        total_matches = db.query(models.JobMatch).count()
        
        # Count users with matches
        users_with_matches = db.query(models.JobMatch.user_id).distinct().count()
        
        # Count users with complete profiles
        users_with_profiles = db.query(models.UserProfile).filter(
            models.UserProfile.resume_parsed.isnot(None),
            models.UserProfile.query.isnot(None),
            models.UserProfile.location.isnot(None)
        ).count()
        
        # Get average relevance score
        from sqlalchemy import func
        avg_score_result = db.query(func.avg(models.JobMatch.relevance_score)).scalar()
        avg_relevance_score = float(avg_score_result) if avg_score_result else 0.0
        
        return {
            "total_jobs": total_jobs,
            "total_matches": total_matches,
            "users_with_matches": users_with_matches,
            "users_with_complete_profiles": users_with_profiles,
            "average_relevance_score": round(avg_relevance_score, 2),
            "scheduler_running": get_job_scheduler().is_running
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting statistics: {str(e)}"
        )
