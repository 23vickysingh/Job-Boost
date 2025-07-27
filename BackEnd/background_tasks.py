import asyncio
import json
import os
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import models
from database import SessionLocal
from utils.resume_parser import process_resume_upload, format_parsed_data_for_database


class ResumeProcessor:
    """Handle background processing of uploaded resumes."""
    
    def __init__(self):
        self.processing_queue = asyncio.Queue()
        self.is_running = False
    
    async def start_processor(self):
        """Start the background resume processor."""
        if self.is_running:
            return
        
        self.is_running = True
        print("Resume processor started...")
        
        while self.is_running:
            try:
                # Wait for a resume processing task
                task = await asyncio.wait_for(self.processing_queue.get(), timeout=1.0)
                await self._process_resume_task(task)
                self.processing_queue.task_done()
            except asyncio.TimeoutError:
                # No task in queue, continue waiting
                continue
            except Exception as e:
                print(f"Error in resume processor: {e}")
                continue
    
    async def stop_processor(self):
        """Stop the background resume processor."""
        self.is_running = False
        print("Resume processor stopped.")
    
    async def add_resume_to_queue(self, user_id: int, file_bytes: bytes, filename: str):
        """Add a resume processing task to the queue."""
        task = {
            "user_id": user_id,
            "file_bytes": file_bytes,
            "filename": filename
        }
        await self.processing_queue.put(task)
        print(f"Added resume processing task for user {user_id}")
    
    async def _process_resume_task(self, task: dict):
        """Process a single resume parsing task."""
        user_id = task["user_id"]
        file_bytes = task["file_bytes"]
        filename = task["filename"]
        
        try:
            print(f"Processing resume for user {user_id}: {filename}")
            
            # Parse the resume
            parsed_result = await process_resume_upload(file_bytes, filename, use_gemini=True)
            
            if not parsed_result.get("success"):
                print(f"Failed to parse resume for user {user_id}: {parsed_result.get('error')}")
                return
            
            # Format data for database
            db_data = format_parsed_data_for_database(parsed_result)
            
            # Update database
            await self._update_user_profile(user_id, db_data, filename)
            
            print(f"Successfully processed resume for user {user_id}")
            
        except Exception as e:
            print(f"Error processing resume for user {user_id}: {e}")
    
    async def _update_user_profile(self, user_id: int, profile_data: dict, filename: str):
        """Update user profile with parsed resume data."""
        db = SessionLocal()
        try:
            # Get existing profile
            profile = db.query(models.UserProfile).filter(
                models.UserProfile.user_id == user_id
            ).first()
            
            if not profile:
                # Create new profile if it doesn't exist
                profile = models.UserProfile(user_id=user_id)
                db.add(profile)
            
            # Update profile with parsed data
            profile.experiences = profile_data.get("experiences", "")
            profile.skills = profile_data.get("skills", "")
            profile.projects = profile_data.get("projects", "")
            profile.education = profile_data.get("education", "")
            profile.courses = profile_data.get("courses", "")
            profile.achievements = profile_data.get("achievements", "")
            profile.resume_filename = filename
            profile.resume_data = profile_data.get("resume_data", "")
            
            db.commit()
            print(f"Updated profile for user {user_id}")
            
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Database error updating profile for user {user_id}: {e}")
            raise
        finally:
            db.close()


# Global resume processor instance
resume_processor = ResumeProcessor()


async def start_background_tasks():
    """Start all background tasks."""
    asyncio.create_task(resume_processor.start_processor())


async def stop_background_tasks():
    """Stop all background tasks."""
    await resume_processor.stop_processor()


def get_resume_processor() -> ResumeProcessor:
    """Get the global resume processor instance."""
    return resume_processor
