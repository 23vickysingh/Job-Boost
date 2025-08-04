#!/usr/bin/env python3
"""
Complete Job Matching Test

This script tests the complete job matching workflow:
1. Creates a test user profile with resume data and job preferences
2. Triggers job matching process
3. Retrieves and displays matched jobs

Usage:
    python complete_test.py --api-key YOUR_API_KEY
"""

import argparse
import asyncio
import os
import sys
import json
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from services.job_matcher import JobMatchingService


# Sample resume data for testing
SAMPLE_RESUME_DATA = {
    "filename": "test_resume.pdf",
    "text": "Sample resume text...",
    "parsed_data": {
        "personal_info": {
            "name": "Vivek Singh",
            "email": "23vickysingh@gmail.com",
            "phone": "+91 9991348092",
            "linkedin": "linkedin.com/in/23vickysingh",
            "github": "github.com/CoderVicky23",
            "location": "India"
        },
        "summary": "Aspiring software engineer with strong programming skills and project experience in full-stack development.",
        "experience": [
            {
                "role": "Software Development Intern",
                "company": "Tech Solutions",
                "dates": "2024-2025",
                "location": "Remote",
                "description": [
                    "Developed web applications using React and FastAPI",
                    "Implemented RESTful APIs and database integration",
                    "Collaborated with cross-functional teams"
                ]
            }
        ],
        "education": [
            {"degree": "Masters in Computer Applications", "institution": "National Institute of Technology, Raipur", "dates": "2026", "gpa": "8.38", "location": "NIT Raipur"},
            {"degree": "Graduation", "institution": "University of Delhi", "dates": "2022", "gpa": "8.67", "location": "Dyal Singh College"}
        ],
        "skills": [
            "C", "C++", "Python", "Java", "HTML", "CSS", "JavaScript", "MySQL", "MongoDB", "Github", "VSCode",
            "UNIX", "Postman", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "React", "FastAPI", "Node JS", "MERN Stack"
        ],
        "projects": [
            {
                "name": "Resume-Based Job Finder Web Application",
                "technologies": ["React", "FastAPI", "MySQL", "Python", "API"],
                "description": "Engineered a dynamic full-stack web application that intelligently matches users to relevant job listings based on their uploaded resumes.",
                "link": None
            },
            {
                "name": "MERN Stack E-COMMERCE Platform",
                "technologies": ["MongoDB", "Express", "React", "Node JS"],
                "description": "Designed and developed a fully responsive and scalable e-commerce web application with modern UI/UX.",
                "link": None
            }
        ],
        "courses_undertaken": [
            "Data Structures & Algorithms", "Object-Oriented Programming", "Operating Systems", "DBMS", "Networks",
            "Computer Architecture", "Front End for web applications", "Back End and Database Management Systems"
        ],
        "achievements": [
            "Dean's List for Academic Excellence",
            "Winner of Coding Competition 2024"
        ],
        "certifications": [
            "AWS Cloud Practitioner",
            "Python Programming Certification"
        ]
    },
    "uploaded_at": datetime.utcnow().isoformat()
}


def create_test_user_profile(db: Session, user_email: str = "test@example.com") -> models.User:
    """Create a test user with complete profile and resume data."""
    
    print(f"👤 Creating test user: {user_email}")
    
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.user_id == user_email).first()
    if existing_user:
        print(f"   User already exists with ID: {existing_user.id}")
        return existing_user
    
    # Create new user
    new_user = models.User(
        user_id=user_email,
        password="hashed_password_here"  # In real app, this would be properly hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"   ✅ Created user with ID: {new_user.id}")
    
    # Create or update user profile with job preferences
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == new_user.id
    ).first()
    
    if not profile:
        profile = models.UserProfile(user_id=new_user.id)
        db.add(profile)
    
    # Set job preferences
    profile.query = "Software Engineer"
    profile.location = "USA"
    profile.mode_of_job = "remote"
    profile.work_experience = "entry-level"
    profile.employment_types = ["FULLTIME", "PARTTIME"]
    profile.company_types = ["Technology", "Startup"]
    profile.job_requirements = "Looking for full-stack development roles with growth opportunities"
    
    # Set resume data
    profile.resume_location = "uploads/test_resume.pdf"
    profile.resume_parsed = SAMPLE_RESUME_DATA
    
    db.commit()
    db.refresh(profile)
    
    print(f"   ✅ Created/updated profile with job preferences and resume data")
    print(f"      Query: {profile.query}")
    print(f"      Location: {profile.location}")
    print(f"      Experience: {profile.work_experience}")
    print(f"      Employment Types: {profile.employment_types}")
    
    return new_user


def display_job_matches(db: Session, user_id: int):
    """Display all job matches for a user."""
    
    matches = db.query(models.JobMatch).filter(
        models.JobMatch.user_id == user_id
    ).order_by(models.JobMatch.relevance_score.desc()).all()
    
    if not matches:
        print("❌ No job matches found")
        return
    
    print(f"🎯 Found {len(matches)} job matches:")
    print("=" * 80)
    
    for i, match in enumerate(matches, 1):
        job = match.job
        
        # Score color coding
        if match.relevance_score >= 70:
            score_emoji = "🟢"
        elif match.relevance_score >= 50:
            score_emoji = "🟡"
        else:
            score_emoji = "🔴"
        
        print(f"\n🏆 Match #{i}:")
        print(f"   Job ID: {job.job_id}")
        print(f"   Title: {job.title}")
        print(f"   Company: {job.company}")
        print(f"   Location: {job.location}")
        print(f"   Employment Type: {job.job_employment_type or 'N/A'}")
        
        # Salary information
        if job.job_min_salary or job.job_max_salary:
            salary_parts = []
            if job.job_min_salary:
                salary_parts.append(f"{job.job_salary_currency or '$'}{job.job_min_salary:,.0f}")
            if job.job_max_salary:
                if job.job_min_salary:
                    salary_parts.append(f"- {job.job_salary_currency or '$'}{job.job_max_salary:,.0f}")
                else:
                    salary_parts.append(f"Up to {job.job_salary_currency or '$'}{job.job_max_salary:,.0f}")
            
            salary_info = " ".join(salary_parts)
            if job.job_salary_period:
                salary_info += f" per {job.job_salary_period.lower()}"
            
            print(f"   Salary: {salary_info}")
        
        print(f"   Relevance Score: {score_emoji} {match.relevance_score:.2f}%")
        print(f"   Apply Link: {job.apply_link}")
        
        # Job highlights
        if job.job_highlights:
            highlights = job.job_highlights
            if highlights.get('Qualifications'):
                print(f"   Key Qualifications: {', '.join(highlights['Qualifications'][:3])}...")
        
        print("-" * 80)
    
    # Summary statistics
    scores = [match.relevance_score for match in matches]
    avg_score = sum(scores) / len(scores)
    
    print(f"\n📊 Summary:")
    print(f"   Total Matches: {len(matches)}")
    print(f"   Average Score: {avg_score:.2f}%")
    print(f"   Highest Score: {max(scores):.2f}%")
    print(f"   Matches >70%: {sum(1 for score in scores if score >= 70)}")
    print(f"   Matches >50%: {sum(1 for score in scores if score >= 50)}")


async def main():
    """Main function to run complete job matching test."""
    
    parser = argparse.ArgumentParser(description="Complete Job Matching Test")
    parser.add_argument("--api-key", required=True, help="JSearch API key")
    parser.add_argument("--user-email", default="test@example.com", help="Test user email")
    parser.add_argument("--query", default="Software Engineer", help="Job search query")
    parser.add_argument("--location", default="USA", help="Job location")
    parser.add_argument("--skip-matching", action="store_true", help="Skip job matching, only show existing matches")
    
    args = parser.parse_args()
    
    print("🚀 Complete Job Matching Test")
    print("=" * 80)
    
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Step 1: Create test user with profile and resume data
        print("\n📋 Step 1: Setting up test user profile...")
        test_user = create_test_user_profile(db, args.user_email)
        
        if not args.skip_matching:
            # Step 2: Initialize job matching service
            print(f"\n🔧 Step 2: Initializing job matching service...")
            job_service = JobMatchingService(args.api_key)
            
            # Step 3: Process job matching
            print(f"\n🎯 Step 3: Processing job matching for user {test_user.id}...")
            result = job_service.process_job_matching_for_user(test_user.id, db)
            
            if result["success"]:
                print(f"✅ Job matching completed successfully!")
                print(f"   Jobs Processed: {result['jobs_processed']}")
                print(f"   Matches Created: {result['matches_created']}")
            else:
                print(f"❌ Job matching failed: {result['message']}")
                return
        
        # Step 4: Display results
        print(f"\n📊 Step 4: Displaying job matching results...")
        display_job_matches(db, test_user.id)
        
        print(f"\n🎉 Test completed successfully!")
        
        # Cleanup option
        cleanup = input("\n🗑️ Delete test user and data? (y/N): ").strip().lower()
        if cleanup == 'y':
            # Delete job matches
            db.query(models.JobMatch).filter(models.JobMatch.user_id == test_user.id).delete()
            
            # Delete user profile
            db.query(models.UserProfile).filter(models.UserProfile.user_id == test_user.id).delete()
            
            # Delete user
            db.delete(test_user)
            db.commit()
            
            print("✅ Test data cleaned up successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
