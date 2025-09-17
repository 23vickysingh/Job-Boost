from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta

import models, schemas
from database import get_db
from auth.dependencies import get_current_user
from tasks.job_search import find_and_match_jobs_for_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/test")
async def test_endpoint():
    """Test endpoint to check if API is working."""
    return {"message": "API is working", "status": "ok"}


@router.get("/dashboard", response_model=schemas.DashboardResponse)
async def get_dashboard_data(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Dashboard endpoint that checks if job search is needed and triggers it if required.
    Returns dashboard data with status of job search and profile completion.
    """
    try:
        # Get user profile
        user_profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == current_user.id
        ).first()
        
        if not user_profile:
            return {
                "status": "incomplete_profile",
                "message": "User profile not found",
                "needs_preferences": True,
                "needs_resume": True,
                "job_search_status": "not_started"
            }
        
        # Check if resume and preferences are set
        has_resume = user_profile.resume_parsed is not None
        has_preferences = user_profile.preferences_set and user_profile.query is not None
        
        # If either resume or preferences are missing, return incomplete status
        if not has_resume or not has_preferences:
            return {
                "status": "incomplete_profile",
                "message": "Please complete your profile to get personalized job matches",
                "needs_preferences": not has_preferences,
                "needs_resume": not has_resume,
                "job_search_status": "not_started"
            }
        
        # Both resume and preferences are set, check if job search is needed
        current_time = datetime.utcnow()
        needs_job_search = False
        
        # Check if last_job_searched is None or older than 24 hours
        if user_profile.last_job_searched is None:
            needs_job_search = True
            search_reason = "first_time"
        else:
            try:
                # Ensure we're comparing datetime objects correctly
                last_search_time = user_profile.last_job_searched
                
                # Handle different datetime types from database
                if isinstance(last_search_time, str):
                    # Parse string datetime
                    last_search_time = datetime.fromisoformat(last_search_time.replace('Z', '+00:00'))
                elif hasattr(last_search_time, 'date') and not hasattr(last_search_time, 'hour'):
                    # Convert date to datetime (add time component)
                    from datetime import time
                    last_search_time = datetime.combine(last_search_time, time.min)
                
                # Ensure both times are timezone-naive for comparison
                if last_search_time.tzinfo is not None:
                    last_search_time = last_search_time.replace(tzinfo=None)
                
                time_since_last_search = current_time - last_search_time
                if time_since_last_search > timedelta(hours=24):
                    needs_job_search = True
                    search_reason = "outdated"
                else:
                    search_reason = "recent"
            except (TypeError, ValueError, AttributeError) as date_error:
                print(f"Error handling last_job_searched datetime in dashboard: {date_error}")
                print(f" =================>       last_job_searched type: {type(user_profile.last_job_searched)}")
                print(f" =================>       last_job_searched value: {user_profile.last_job_searched}")
                # If there's an issue with datetime comparison, do not treat as first time
                needs_job_search = False
                search_reason = "system_error"
        
        if needs_job_search:
            print(f"Starting job search for user {current_user.id}, reason: {search_reason}")
            print(f"Current time: {current_time}")
            print(f"Previous last_job_searched: {user_profile.last_job_searched}")
            
            # Update last_job_searched timestamp
            user_profile.last_job_searched = current_time
            db.commit()
            
            print(f"Updated last_job_searched to: {user_profile.last_job_searched}")
            
            # Trigger background job search
            background_tasks.add_task(find_and_match_jobs_for_user, current_user.id)
            
            return {
                "status": "searching",
                "message": "Finding the best suitable jobs for you...",
                "needs_preferences": False,
                "needs_resume": False,
                "job_search_status": "in_progress",
                "search_reason": search_reason
            }
        else:
            # Get dashboard stats
            dashboard_stats = await get_job_match_stats_internal(db, current_user)
            
            return {
                "status": "ready",
                "message": "Dashboard ready",
                "needs_preferences": False,
                "needs_resume": False,
                "job_search_status": "completed",
                "search_reason": search_reason,
                "last_job_searched": user_profile.last_job_searched.isoformat(),
                "dashboard_stats": dashboard_stats
            }
            
    except Exception as e:
        print(f"Error in dashboard endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_job_match_stats_internal(db: Session, current_user: models.User) -> dict:
    """Internal function to get dashboard stats without auth dependency."""
    try:
        # Total job matches
        total_matches = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id
        ).count()
        
        # High relevance jobs (>= 70%)
        high_relevance_jobs = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id,
            models.JobMatch.relevance_score >= 0.7
        ).count()
        
        # Jobs added in the last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        recent_matches = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id,
            models.JobMatch.created_at >= yesterday
        ).count()
        
        # Applied jobs count
        applied_jobs = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id,
            models.JobMatch.status == models.JobMatchStatus.applied
        ).count()
        
        return {
            "total_matches": total_matches,
            "high_relevance_jobs": high_relevance_jobs,
            "recent_matches": recent_matches,
            "applied_jobs": applied_jobs
        }
        
    except Exception as e:
        print(f"Error in get_job_match_stats_internal: {e}")
        return {
            "total_matches": 0,
            "high_relevance_jobs": 0,
            "recent_matches": 0,
            "applied_jobs": 0
        }


@router.get("/matches", response_model=List[schemas.JobMatchOut])
async def get_job_matches(
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
    min_relevance: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get job matches for the current user."""
    
    try:
        query = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id
        ).options(joinedload(models.JobMatch.job))  # Eager load job details
        
        # Filter by minimum relevance score if provided
        if min_relevance is not None:
            query = query.filter(models.JobMatch.relevance_score >= min_relevance)
        
        # Order by relevance score (highest first) and creation date
        query = query.order_by(
            desc(models.JobMatch.relevance_score),
            desc(models.JobMatch.created_at)
        )
        
        # Apply pagination
        job_matches = query.offset(offset).limit(limit).all()
        
        return job_matches
        
    except Exception as e:
        print(f"Error in get_job_matches: {e}")
        # Return empty list if there's an error
        return []


@router.get("/matches/stats", response_model=schemas.DashboardStats)
async def get_job_match_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get job match statistics for the current user."""
    
    try:
        # Total job matches
        total_matches = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id
        ).count()
        
        # High relevance jobs (>= 70%)
        high_relevance_jobs = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id,
            models.JobMatch.relevance_score >= 0.7
        ).count()
        
        # Jobs added in the last 24 hours
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        recent_matches = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id,
            models.JobMatch.created_at >= yesterday
        ).count()
        
        # Applied jobs count
        applied_jobs = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id,
            models.JobMatch.status == models.JobMatchStatus.applied
        ).count()
        
        return {
            "total_matches": total_matches,
            "high_relevance_jobs": high_relevance_jobs,
            "recent_matches": recent_matches,
            "applied_jobs": applied_jobs
        }
        
    except Exception as e:
        # Return zeros if there's any error
        print(f"Error in get_job_match_stats: {e}")
        return {
            "total_matches": 0,
            "high_relevance_jobs": 0,
            "recent_matches": 0,
            "applied_jobs": 0
        }


@router.get("/matches/{match_id}", response_model=schemas.JobMatchOut)
async def get_job_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get a specific job match by ID."""
    
    job_match = db.query(models.JobMatch).filter(
        models.JobMatch.id == match_id,
        models.JobMatch.user_id == current_user.id
    ).first()
    
    if not job_match:
        raise HTTPException(status_code=404, detail="Job match not found")
    
    return job_match


@router.put("/matches/{match_id}/status")
async def update_job_match_status(
    match_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update the status of a job match."""
    
    # Validate status
    valid_statuses = ["pending", "applied", "not_interested"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    # Find the job match
    job_match = db.query(models.JobMatch).filter(
        models.JobMatch.id == match_id,
        models.JobMatch.user_id == current_user.id
    ).first()
    
    if not job_match:
        raise HTTPException(status_code=404, detail="Job match not found")
    
    # Update the status
    job_match.status = status
    db.commit()
    db.refresh(job_match)
    
    return {
        "message": "Job match status updated successfully",
        "match_id": match_id,
        "new_status": status
    }


@router.delete("/matches/{match_id}")
async def delete_job_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete a job match completely from the database."""
    
    # Find the job match
    job_match = db.query(models.JobMatch).filter(
        models.JobMatch.id == match_id,
        models.JobMatch.user_id == current_user.id
    ).first()
    
    if not job_match:
        raise HTTPException(status_code=404, detail="Job match not found")
    
    # Delete the job match
    db.delete(job_match)
    db.commit()
    
    return {
        "message": "Job match deleted successfully",
        "match_id": match_id
    }


@router.get("/applications", response_model=List[schemas.JobMatchOut])
async def get_applications(
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get all applied jobs (applications) for the current user."""
    
    try:
        query = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id,
            models.JobMatch.status == models.JobMatchStatus.applied
        ).options(joinedload(models.JobMatch.job))  # Eager load job details
        
        # Order by creation date (most recent first)
        query = query.order_by(desc(models.JobMatch.created_at))
        
        # Apply pagination
        applications = query.offset(offset).limit(limit).all()
        
        return applications
        
    except Exception as e:
        print(f"Error in get_applications: {e}")
        # Return empty list if there's an error
        return []


# Job Relevance Endpoint (for new matches only)
@router.post("/matches/{match_id}/calculate-relevance", response_model=schemas.RelevanceCalculationResponse)
async def calculate_job_match_relevance(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Calculate relevance score for a new job match (only if not already calculated)."""
    try:
        # Verify the job match belongs to the current user
        job_match = db.query(models.JobMatch).filter(
            models.JobMatch.id == match_id,
            models.JobMatch.user_id == current_user.id
        ).first()
        
        if not job_match:
            raise HTTPException(
                status_code=404,
                detail="Job match not found or does not belong to user"
            )
        
        # Check if relevance score already exists
        if job_match.relevance_score is not None:
            return {
                "message": "Relevance score already exists",
                "job_match_id": match_id,
                "relevance_score": job_match.relevance_score,
                "relevance_percentage": int(job_match.relevance_score * 100)
            }
        
        # Calculate relevance score only for new matches
        from services.job_relevance_service import calculate_job_relevance_for_new_match
        relevance_score = await calculate_job_relevance_for_new_match(match_id, db)
        
        if relevance_score is None:
            raise HTTPException(
                status_code=400,
                detail="Could not calculate relevance score. Check resume data and job description."
            )
        
        return {
            "message": "Relevance score calculated successfully",
            "job_match_id": match_id,
            "relevance_score": relevance_score,
            "relevance_percentage": int(relevance_score * 100)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating job relevance: {str(e)}"
        )


@router.get("/matches/high-relevance", response_model=schemas.HighRelevanceJobsResponse)
async def get_high_relevance_jobs(
    min_relevance: float = 0.7,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get job matches with high relevance scores."""
    try:
        high_relevance_jobs = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id,
            models.JobMatch.relevance_score >= min_relevance
        ).order_by(desc(models.JobMatch.relevance_score)).limit(limit).all()
        
        return {
            "message": f"Found {len(high_relevance_jobs)} high-relevance job matches",
            "min_relevance": min_relevance,
            "matches": [
                {
                    "id": job.id,
                    "job_title": job.job_title,
                    "company_name": job.company_name,
                    "relevance_score": job.relevance_score,
                    "relevance_percentage": int(job.relevance_score * 100) if job.relevance_score else 0,
                    "location": job.location,
                    "created_at": job.created_at,
                    "status": job.status
                }
                for job in high_relevance_jobs
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching high-relevance jobs: {str(e)}"
        )


@router.post("/matches/fix-zero-scores")
async def fix_zero_relevance_scores(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Fix job matches that have zero relevance scores."""
    try:
        # Find matches with zero or very low relevance scores
        zero_score_matches = db.query(models.JobMatch).filter(
            models.JobMatch.user_id == current_user.id,
            models.JobMatch.relevance_score <= 0.05  # Essentially zero
        ).options(joinedload(models.JobMatch.job)).all()
        
        if not zero_score_matches:
            return {
                "message": "No job matches with zero scores found",
                "fixed_count": 0
            }
        
        # Get user profile for relevance calculation
        user_profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == current_user.id
        ).first()
        
        if not user_profile or not user_profile.resume_parsed:
            raise HTTPException(
                status_code=400,
                detail="Resume data required for relevance calculation"
            )
        
        from services.job_relevance_service import JobRelevanceCalculator
        calculator = JobRelevanceCalculator()
        
        fixed_count = 0
        for job_match in zero_score_matches:
            if job_match.job and job_match.job.job_description:
                try:
                    # Calculate new relevance score
                    new_relevance = await calculator.calculate_relevance_score(
                        resume_data=user_profile.resume_parsed,
                        job_description=job_match.job.job_description,
                        job_title=job_match.job.job_title or "",
                        job_requirements=job_match.job.job_required_skills or ""
                    )
                    
                    # Update the job match
                    job_match.relevance_score = new_relevance
                    fixed_count += 1
                    
                    print(f"Fixed relevance score for job '{job_match.job.job_title}': 0.0 -> {new_relevance:.3f}")
                    
                except Exception as e:
                    print(f"Error calculating relevance for job match {job_match.id}: {e}")
                    continue
        
        db.commit()
        
        return {
            "message": f"Successfully fixed {fixed_count} job matches with zero relevance scores",
            "fixed_count": fixed_count,
            "total_zero_scores": len(zero_score_matches)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error fixing zero relevance scores: {str(e)}"
        )
