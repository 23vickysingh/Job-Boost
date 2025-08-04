#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
sys.path.append('.')

def test_manual_job_matching():
    """Test job matching by creating a user manually in the database"""
    print("🔍 Testing Manual Job Matching...")
    
    try:
        from services.job_matcher import get_job_matching_service
        from database import SessionLocal
        import models
        from auth.hashing import Hash
        from datetime import datetime
        
        print("✅ Modules imported successfully")
        
        # Create database session
        db = SessionLocal()
        
        # Check if there are existing users
        existing_users = db.query(models.User).all()
        print(f"📊 Found {len(existing_users)} existing users")
        
        test_user = None
        
        if existing_users:
            # Use the first existing user
            test_user = existing_users[0]
            print(f"🎯 Using existing user: {test_user.username} (ID: {test_user.id})")
        else:
            # Create a test user
            print("🔧 Creating test user...")
            test_user = models.User(
                username="test_job_matcher_db",
                email="testjobmatcher_db@example.com",
                hashed_password=Hash.bcrypt("testpassword123"),
                is_verified=True
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"✅ Test user created: {test_user.username} (ID: {test_user.id})")
        
        # Check if user has a profile
        profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == test_user.id
        ).first()
        
        if not profile:
            # Create a test profile
            print("🔧 Creating test profile...")
            mock_resume_data = {
                "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "JavaScript"],
                "experience": ["Software Engineer at ABC Corp - 3 years", "Full-stack Developer at XYZ Inc - 2 years"],
                "education": ["Bachelor's in Computer Science"],
                "languages": ["English", "Spanish"]
            }
            
            profile = models.UserProfile(
                user_id=test_user.id,
                query="Python Software Engineer",
                location="Remote",
                resume_parsed=mock_resume_data,
                resume_location="/test/resume.pdf",
                last_updated=datetime.utcnow()
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
            print(f"✅ Test profile created for user {test_user.id}")
        else:
            print(f"✅ Found existing profile for user {test_user.id}")
            print(f"   Query: {profile.query}")
            print(f"   Location: {profile.location}")
            print(f"   Has resume: {'Yes' if profile.resume_parsed else 'No'}")
        
        # Now test job matching
        print(f"\n🚀 Starting job matching for user {test_user.id}...")
        
        job_service = get_job_matching_service()
        if job_service:
            print("✅ Job matching service initialized")
            
            # Process job matching
            result = job_service.process_job_matching_for_user(test_user.id, db)
            
            print(f"\n📊 Job matching results:")
            print(f"   Success: {result.get('success', False)}")
            print(f"   Message: {result.get('message', 'N/A')}")
            print(f"   Jobs Processed: {result.get('jobs_processed', 0)}")
            print(f"   Jobs Stored: {result.get('jobs_stored', 0)}")
            print(f"   Matches Created: {result.get('matches_created', 0)}")
            
            # Check database for results
            total_jobs = db.query(models.Job).count()
            user_matches = db.query(models.JobMatch).filter(
                models.JobMatch.user_id == test_user.id
            ).count()
            
            print(f"\n📈 Database Status:")
            print(f"   Total jobs in database: {total_jobs}")
            print(f"   Job matches for user: {user_matches}")
            
        else:
            print("❌ Failed to initialize job matching service")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error in manual job matching test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_manual_job_matching()
