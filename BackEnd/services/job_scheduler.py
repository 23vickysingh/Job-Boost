import asyncio
import os
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_

import models
from database import SessionLocal
from services.job_matcher import get_job_matching_service


class JobScheduler:
    """Background scheduler for automatic job matching updates."""
    
    def __init__(self):
        self.is_running = False
        self.check_interval = 12 * 3600  # 12 hours in seconds
        self.user_threshold = 24 * 3600  # 24 hours in seconds
        
    async def start_scheduler(self):
        """Start the background job scheduler."""
        if self.is_running:
            return
            
        self.is_running = True
        
        while self.is_running:
            try:
                # Wait for the check interval (12 hours)
                await asyncio.sleep(self.check_interval)
                
                if self.is_running:  # Check if still running after sleep
                    await self._process_scheduled_job_updates()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Continue running even if one cycle fails
                continue
    
    async def stop_scheduler(self):
        """Stop the background job scheduler."""
        self.is_running = False
    
    async def _process_scheduled_job_updates(self):
        """Process job updates for users who need refreshed matches."""
        
        db = SessionLocal()
        try:
            # Get users who need job updates
            users_to_update = self._get_users_needing_updates(db)
            
            if not users_to_update:
                return
            
            
            # Get job matching service
            job_service = get_job_matching_service()
            if not job_service:
                return
            
            # Process each user
            successful_updates = 0
            failed_updates = 0
            
            for user_profile in users_to_update:
                try:
                    
                    # Process job matching for this user
                    result = job_service.process_job_matching_for_user(user_profile.user_id, db)
                    
                    if result["success"]:
                        successful_updates += 1
                        
                        # Update the last job search timestamp
                        user_profile.last_job_search = datetime.utcnow()
                        db.commit()
                        
                    else:
                        failed_updates += 1
                        
                except Exception as e:
                    failed_updates += 1
                    continue
            
        except Exception as e:
            pass
        finally:
            db.close()
    
    def _get_users_needing_updates(self, db: Session) -> List[models.UserProfile]:
        """Get users who need job updates based on time threshold."""
        
        # Calculate the cutoff time (24 hours ago)
        cutoff_time = datetime.utcnow() - timedelta(seconds=self.user_threshold)
        
        # Query for users who need updates
        users_needing_updates = db.query(models.UserProfile).filter(
            and_(
                # User has resume data
                models.UserProfile.resume_parsed.isnot(None),
                # User has job preferences
                models.UserProfile.query.isnot(None),
                models.UserProfile.location.isnot(None),
                # Either never had job search OR last search was > 24 hours ago
                models.UserProfile.last_job_search.is_(None) |
                (models.UserProfile.last_job_search < cutoff_time)
            )
        ).all()
        
        return users_needing_updates
    
    async def force_update_all_users(self):
        """Force job update for all eligible users (manual trigger)."""
        
        db = SessionLocal()
        try:
            # Get all users with resume and preferences
            all_eligible_users = db.query(models.UserProfile).filter(
                and_(
                    models.UserProfile.resume_parsed.isnot(None),
                    models.UserProfile.query.isnot(None),
                    models.UserProfile.location.isnot(None)
                )
            ).all()
            
            if not all_eligible_users:
                return
            
            
            # Get job matching service
            job_service = get_job_matching_service()
            if not job_service:
                return
            
            # Process each user
            for user_profile in all_eligible_users:
                try:
                    result = job_service.process_job_matching_for_user(user_profile.user_id, db)
                    
                    if result["success"]:
                        user_profile.last_job_search = datetime.utcnow()
                        db.commit()
                    else:
                        pass
                        
                except Exception as e:
                    continue
            
        except Exception as e:
            pass
        finally:
            db.close()


# Global scheduler instance
job_scheduler = JobScheduler()


async def start_job_scheduler():
    """Start the job scheduler."""
    await job_scheduler.start_scheduler()


async def stop_job_scheduler():
    """Stop the job scheduler."""
    await job_scheduler.stop_scheduler()


def get_job_scheduler() -> JobScheduler:
    """Get the global job scheduler instance."""
    return job_scheduler
