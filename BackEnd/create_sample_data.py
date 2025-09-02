#!/usr/bin/env python3
"""
Script to create sample job data for testing
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_database_url
import models
from datetime import datetime

def create_sample_data():
    """Create sample job matches data for testing."""
    
    # Get database URL
    database_url = get_database_url()
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = SessionLocal()
    
    try:
        print("Creating sample job data...")
        
        # Check if we have any users
        user = session.query(models.User).first()
        if not user:
            print("No users found in database. Please create a user first.")
            return
        
        print(f"Found user: {user.user_id}")
        
        # Create sample jobs
        sample_jobs = [
            {
                "job_id": "test_job_1",
                "job_title": "Senior Software Engineer",
                "employer_name": "Tech Corp",
                "job_description": "Looking for a senior software engineer with Python experience",
                "job_city": "San Francisco",
                "job_country": "USA",
                "job_employment_type": "fulltime",
                "job_min_salary": 120000,
                "job_max_salary": 180000,
                "job_salary_currency": "USD",
                "job_salary_period": "YEAR"
            },
            {
                "job_id": "test_job_2", 
                "job_title": "Frontend Developer",
                "employer_name": "StartupXYZ",
                "job_description": "React developer needed for exciting startup",
                "job_city": "New York",
                "job_country": "USA",
                "job_employment_type": "fulltime",
                "job_min_salary": 90000,
                "job_max_salary": 140000,
                "job_salary_currency": "USD",
                "job_salary_period": "YEAR"
            },
            {
                "job_id": "test_job_3",
                "job_title": "Data Scientist",
                "employer_name": "AI Innovations",
                "job_description": "Machine learning and data analysis role",
                "job_city": "Boston",
                "job_country": "USA", 
                "job_employment_type": "fulltime",
                "job_min_salary": 110000,
                "job_max_salary": 160000,
                "job_salary_currency": "USD",
                "job_salary_period": "YEAR"
            }
        ]
        
        # Create job records
        created_jobs = []
        for job_data in sample_jobs:
            # Check if job already exists
            existing_job = session.query(models.Job).filter(models.Job.job_id == job_data["job_id"]).first()
            if existing_job:
                print(f"Job {job_data['job_id']} already exists, using existing record")
                created_jobs.append(existing_job)
            else:
                job = models.Job(**job_data)
                session.add(job)
                session.flush()  # To get the ID
                created_jobs.append(job)
                print(f"Created job: {job.job_title} at {job.employer_name}")
        
        # Create job matches for the user
        for i, job in enumerate(created_jobs):
            # Check if job match already exists
            existing_match = session.query(models.JobMatch).filter(
                models.JobMatch.user_id == user.id,
                models.JobMatch.job_id == job.id
            ).first()
            
            if existing_match:
                print(f"Job match already exists for {job.job_title}")
            else:
                relevance_scores = [0.95, 0.85, 0.75]  # Different relevance scores
                statuses = [models.JobMatchStatus.pending, models.JobMatchStatus.applied, models.JobMatchStatus.pending]
                
                job_match = models.JobMatch(
                    user_id=user.id,
                    job_id=job.id,
                    relevance_score=relevance_scores[i],
                    status=statuses[i],
                    created_at=datetime.utcnow()
                )
                session.add(job_match)
                print(f"Created job match for {job.job_title} with {int(relevance_scores[i]*100)}% relevance")
        
        session.commit()
        print("✅ Sample data created successfully!")
        
        # Show counts
        job_count = session.query(models.Job).count()
        match_count = session.query(models.JobMatch).count()
        print(f"Total jobs: {job_count}")
        print(f"Total job matches: {match_count}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error creating sample data: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    create_sample_data()
