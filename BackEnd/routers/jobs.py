from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

import models, schemas
from database import get_db
from auth.dependencies import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/matches", response_model=List[schemas.JobMatchOut])
async def get_job_matches(
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
    min_relevance: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get job matches for the current user."""
    
    query = db.query(models.JobMatch).filter(
        models.JobMatch.user_id == current_user.id
    )
    
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


@router.get("/matches/stats")
async def get_job_match_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get job match statistics for the current user."""
    
    # Total job matches
    total_matches = db.query(models.JobMatch).filter(
        models.JobMatch.user_id == current_user.id
    ).count()
    
    # High relevance jobs (>= 80%)
    high_relevance_jobs = db.query(models.JobMatch).filter(
        models.JobMatch.user_id == current_user.id,
        models.JobMatch.relevance_score >= 0.8
    ).count()
    
    # Jobs added in the last 24 hours
    from datetime import datetime, timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)
    
    recent_matches = db.query(models.JobMatch).filter(
        models.JobMatch.user_id == current_user.id,
        models.JobMatch.created_at >= yesterday
    ).count()
    
    return {
        "total_matches": total_matches,
        "high_relevance_jobs": high_relevance_jobs,
        "recent_matches": recent_matches
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
