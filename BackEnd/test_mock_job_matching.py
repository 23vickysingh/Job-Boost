#!/usr/bin/env python3

import sys
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
sys.path.append('.')

def test_job_matching_with_mock_data():
    """Test job matching with mock data"""
    print("🔍 Testing Job Matching with Mock Data...")
    
    try:
        from services.job_matcher import get_job_matching_service
        from database import SessionLocal
        import models
        from datetime import datetime
        
        # Initialize service
        service = get_job_matching_service()
        if not service:
            print("❌ Failed to initialize job matching service")
            return
        
        print("✅ Job matching service initialized")
        
        # Create mock job data (similar to what would come from API)
        mock_jobs = [
            {
                "job_id": "test_001",
                "job_title": "Python Software Engineer",
                "employer_name": "Tech Corp",
                "job_description": "We are looking for a Python developer with experience in FastAPI, PostgreSQL, and modern web technologies. The ideal candidate will have 3+ years of experience.",
                "job_required_skills": ["Python", "FastAPI", "PostgreSQL", "JavaScript", "React"],
                "job_city": "Remote",
                "job_state": "Anywhere",
                "job_country": "US",
                "job_employment_type": "FULLTIME",
                "job_max_salary": 120000,
                "job_min_salary": 80000,
                "job_salary_currency": "USD"
            },
            {
                "job_id": "test_002", 
                "job_title": "Frontend Developer",
                "employer_name": "Design Studio",
                "job_description": "Looking for a frontend developer with React, TypeScript, and modern CSS frameworks.",
                "job_required_skills": ["React", "TypeScript", "CSS", "JavaScript", "HTML"],
                "job_city": "New York",
                "job_state": "NY",
                "job_country": "US",
                "job_employment_type": "FULLTIME",
                "job_max_salary": 100000,
                "job_min_salary": 70000,
                "job_salary_currency": "USD"
            },
            {
                "job_id": "test_003",
                "job_title": "Data Scientist",
                "employer_name": "Data Labs",
                "job_description": "Seeking a data scientist with Python, machine learning, and statistical analysis experience.",
                "job_required_skills": ["Python", "Machine Learning", "Pandas", "NumPy", "SQL"],
                "job_city": "San Francisco",
                "job_state": "CA", 
                "job_country": "US",
                "job_employment_type": "FULLTIME",
                "job_max_salary": 150000,
                "job_min_salary": 120000,
                "job_salary_currency": "USD"
            }
        ]
        
        # Mock resume data
        mock_resume = {
            "skills": ["Python", "FastAPI", "React", "JavaScript", "PostgreSQL", "Git"],
            "experience": ["Software Engineer at ABC Corp", "Full-stack Developer at XYZ Inc"],
            "education": ["Bachelor's in Computer Science"],
            "languages": ["English", "Spanish"]
        }
        
        print(f"\n🧪 Testing relevance scoring with {len(mock_jobs)} jobs...")
        
        for i, job in enumerate(mock_jobs):
            print(f"\n📊 Job {i+1}: {job['job_title']} at {job['employer_name']}")
            
            # Test relevance calculation
            score = service.calculate_relevance_score(mock_resume, job)
            print(f"   Relevance Score: {score:.2f}")
            
            # Test job saving
            try:
                db = SessionLocal()
                saved_job = service.save_job_to_database(job, job, db)
                if saved_job:
                    print(f"   ✅ Job saved to database with ID: {saved_job.id}")
                else:
                    print(f"   ❌ Failed to save job")
                db.close()
            except Exception as e:
                print(f"   ⚠️ Database error: {e}")
        
        print(f"\n🎉 Mock job matching test completed!")
        
    except Exception as e:
        print(f"❌ Error in mock job matching test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_job_matching_with_mock_data()
