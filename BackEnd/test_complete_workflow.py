#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
sys.path.append('.')

def test_complete_job_matching():
    """Test the complete job matching workflow"""
    print("🔍 Testing Complete Job Matching Workflow...")
    
    try:
        # Import required modules
        from services.job_matcher import get_job_matching_service
        from database import SessionLocal
        import models
        
        print("✅ Successfully imported modules")
        
        # Test database connection
        try:
            db = SessionLocal()
            print("✅ Database connection successful")
            
            # Check for existing users with profiles
            users_with_profiles = db.query(models.UserProfile).limit(5).all()
            print(f"📊 Found {len(users_with_profiles)} user profiles in database")
            
            if users_with_profiles:
                # Get the first user
                test_user = users_with_profiles[0]
                print(f"🎯 Testing with user ID: {test_user.user_id}")
                print(f"   User has resume: {'Yes' if test_user.resume_parsed else 'No'}")
                print(f"   Job preferences: {test_user.job_preferences}")
                
                # Initialize job matching service
                service = get_job_matching_service()
                if service:
                    print("✅ Job matching service initialized")
                    
                    # Test job matching for this user
                    print("\n🚀 Starting job matching process...")
                    result = service.process_job_matching_for_user(test_user.user_id, db)
                    
                    print(f"📊 Job matching result:")
                    print(f"   Success: {result.get('success', False)}")
                    print(f"   Message: {result.get('message', 'N/A')}")
                    print(f"   Jobs Processed: {result.get('jobs_processed', 0)}")
                    print(f"   Jobs Stored: {result.get('jobs_stored', 0)}")
                    print(f"   Matches Created: {result.get('matches_created', 0)}")
                    
                    # Check job matches in database
                    matches = db.query(models.JobMatch).filter(
                        models.JobMatch.user_id == test_user.user_id
                    ).all()
                    print(f"📈 Total job matches for user: {len(matches)}")
                    
                    # Check jobs in database
                    total_jobs = db.query(models.Job).count()
                    print(f"💼 Total jobs in database: {total_jobs}")
                    
                else:
                    print("❌ Failed to initialize job matching service")
            else:
                print("⚠️ No user profiles found in database")
                print("   Please upload a resume first to test job matching")
            
            db.close()
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            import traceback
            traceback.print_exc()
    
    except Exception as e:
        print(f"❌ Error in job matching test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_job_matching()
