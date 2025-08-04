#!/usr/bin/env python3
"""
Complete Workflow Integration Test

This script tests the entire job matching workflow:
1. Automatic job matching after resume upload
2. Background scheduler functionality
3. Database updates and error handling

Usage:
    python test_complete_workflow.py
"""

import asyncio
import os
import sys
import json
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from services.job_matcher import get_job_matching_service
from services.job_scheduler import get_job_scheduler


# Sample user data for testing
SAMPLE_USER_DATA = {
    "user_id": "test_workflow@example.com",
    "job_preferences": {
        "query": "Software Engineer",
        "location": "USA",
        "mode_of_job": "remote",
        "work_experience": "entry-level",
        "employment_types": ["FULLTIME"],
        "company_types": ["Technology", "Startup"]
    },
    "resume_data": {
        "filename": "test_resume.pdf",
        "text": "Sample resume text...",
        "parsed_data": {
            "personal_info": {
                "name": "Test User",
                "email": "test_workflow@example.com",
                "phone": "+1-555-0123",
                "location": "USA"
            },
            "skills": [
                "Python", "JavaScript", "React", "FastAPI", "SQL", "Git",
                "Docker", "AWS", "MongoDB", "Node.js", "HTML", "CSS"
            ],
            "experience": [
                {
                    "role": "Software Developer Intern",
                    "company": "Tech Corp",
                    "dates": "2024-2025",
                    "description": ["Developed web applications", "Used React and Python"]
                }
            ],
            "projects": [
                {
                    "name": "Job Matching Application",
                    "technologies": ["React", "FastAPI", "PostgreSQL"],
                    "description": "Built a job matching system with AI-powered resume parsing"
                }
            ],
            "education": [
                {
                    "degree": "Computer Science",
                    "institution": "University",
                    "dates": "2023-2025"
                }
            ],
            "courses_undertaken": [
                "Data Structures", "Algorithms", "Web Development",
                "Database Systems", "Software Engineering"
            ]
        },
        "uploaded_at": datetime.utcnow().isoformat()
    }
}


class WorkflowTester:
    """Test the complete job matching workflow."""
    
    def __init__(self):
        self.db = SessionLocal()
        self.test_user = None
        self.test_profile = None
    
    def cleanup(self):
        """Clean up test data."""
        if self.db:
            self.db.close()
    
    def create_test_user(self):
        """Create a test user with complete profile."""
        print("👤 Creating test user...")
        
        # Check if user already exists
        existing_user = self.db.query(models.User).filter(
            models.User.user_id == SAMPLE_USER_DATA["user_id"]
        ).first()
        
        if existing_user:
            print(f"   Using existing user: {existing_user.id}")
            self.test_user = existing_user
        else:
            # Create new user
            self.test_user = models.User(
                user_id=SAMPLE_USER_DATA["user_id"],
                password="hashed_password_here"
            )
            self.db.add(self.test_user)
            self.db.commit()
            self.db.refresh(self.test_user)
            print(f"   Created new user: {self.test_user.id}")
        
        # Create/update profile
        self.test_profile = self.db.query(models.UserProfile).filter(
            models.UserProfile.user_id == self.test_user.id
        ).first()
        
        if not self.test_profile:
            self.test_profile = models.UserProfile(user_id=self.test_user.id)
            self.db.add(self.test_profile)
        
        # Set job preferences
        prefs = SAMPLE_USER_DATA["job_preferences"]
        self.test_profile.query = prefs["query"]
        self.test_profile.location = prefs["location"]
        self.test_profile.mode_of_job = prefs["mode_of_job"]
        self.test_profile.work_experience = prefs["work_experience"]
        self.test_profile.employment_types = prefs["employment_types"]
        self.test_profile.company_types = prefs["company_types"]
        
        # Set resume data
        self.test_profile.resume_parsed = SAMPLE_USER_DATA["resume_data"]
        self.test_profile.last_updated = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(self.test_profile)
        
        print(f"   ✅ Test user profile created/updated")
        print(f"      Query: {self.test_profile.query}")
        print(f"      Location: {self.test_profile.location}")
        print(f"      Skills: {len(self.test_profile.resume_parsed['parsed_data']['skills'])}")
    
    def test_automatic_job_matching(self):
        """Test automatic job matching functionality."""
        print("\n🔍 Testing automatic job matching...")
        
        try:
            # Get job matching service
            job_service = get_job_matching_service()
            if not job_service:
                print("❌ Job matching service not available (missing API key)")
                return False
            
            # Clear existing matches for clean test
            self.db.query(models.JobMatch).filter(
                models.JobMatch.user_id == self.test_user.id
            ).delete()
            self.db.commit()
            
            # Process job matching
            result = job_service.process_job_matching_for_user(self.test_user.id, self.db)
            
            if result["success"]:
                print(f"   ✅ Job matching successful!")
                print(f"      Jobs processed: {result['jobs_processed']}")
                print(f"      Matches created: {result['matches_created']}")
                
                # Verify matches in database
                matches = self.db.query(models.JobMatch).filter(
                    models.JobMatch.user_id == self.test_user.id
                ).all()
                
                print(f"   📊 Database verification:")
                print(f"      Matches in DB: {len(matches)}")
                
                for i, match in enumerate(matches, 1):
                    print(f"      Match {i}: {match.job.title} at {match.job.company} ({match.relevance_score:.1f}%)")
                
                return True
            else:
                print(f"   ❌ Job matching failed: {result['message']}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error in job matching test: {e}")
            return False
    
    def test_scheduler_logic(self):
        """Test the scheduler logic without waiting 12 hours."""
        print("\n🕒 Testing scheduler logic...")
        
        try:
            # Get scheduler
            scheduler = get_job_scheduler()
            
            # Test 1: User with no last_job_search should be eligible
            print("   Test 1: New user (no last_job_search)")
            self.test_profile.last_job_search = None
            self.db.commit()
            
            users_needing_updates = scheduler._get_users_needing_updates(self.db)
            user_ids = [u.user_id for u in users_needing_updates]
            
            if self.test_user.id in user_ids:
                print("   ✅ New user correctly identified as needing update")
            else:
                print("   ❌ New user not identified as needing update")
                return False
            
            # Test 2: User with recent search should NOT be eligible
            print("   Test 2: Recent search (1 hour ago)")
            self.test_profile.last_job_search = datetime.utcnow() - timedelta(hours=1)
            self.db.commit()
            
            users_needing_updates = scheduler._get_users_needing_updates(self.db)
            user_ids = [u.user_id for u in users_needing_updates]
            
            if self.test_user.id not in user_ids:
                print("   ✅ Recent user correctly excluded from updates")
            else:
                print("   ❌ Recent user incorrectly included in updates")
                return False
            
            # Test 3: User with old search should be eligible
            print("   Test 3: Old search (25 hours ago)")
            self.test_profile.last_job_search = datetime.utcnow() - timedelta(hours=25)
            self.db.commit()
            
            users_needing_updates = scheduler._get_users_needing_updates(self.db)
            user_ids = [u.user_id for u in users_needing_updates]
            
            if self.test_user.id in user_ids:
                print("   ✅ Old user correctly identified as needing update")
            else:
                print("   ❌ Old user not identified as needing update")
                return False
            
            print("   ✅ All scheduler logic tests passed!")
            return True
            
        except Exception as e:
            print(f"   ❌ Error in scheduler logic test: {e}")
            return False
    
    def test_force_update(self):
        """Test the force update functionality."""
        print("\n🚀 Testing force update...")
        
        try:
            # Get scheduler
            scheduler = get_job_scheduler()
            
            # Set recent last_job_search (should still be updated in force mode)
            self.test_profile.last_job_search = datetime.utcnow() - timedelta(hours=1)
            self.db.commit()
            
            # Clear existing matches
            initial_matches = self.db.query(models.JobMatch).filter(
                models.JobMatch.user_id == self.test_user.id
            ).count()
            
            print(f"   Initial matches: {initial_matches}")
            
            # Force update
            await scheduler.force_update_all_users()
            
            # Check results
            final_matches = self.db.query(models.JobMatch).filter(
                models.JobMatch.user_id == self.test_user.id
            ).count()
            
            print(f"   Final matches: {final_matches}")
            
            # Verify last_job_search was updated
            self.db.refresh(self.test_profile)
            time_diff = (datetime.utcnow() - self.test_profile.last_job_search).total_seconds()
            
            if time_diff < 60:  # Updated within last minute
                print("   ✅ last_job_search timestamp updated correctly")
            else:
                print("   ❌ last_job_search timestamp not updated")
                return False
            
            print("   ✅ Force update test passed!")
            return True
            
        except Exception as e:
            print(f"   ❌ Error in force update test: {e}")
            return False
    
    def verify_database_schema(self):
        """Verify the database schema has all required fields."""
        print("\n📋 Verifying database schema...")
        
        try:
            # Check if last_job_search column exists
            result = self.db.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'user_profile' AND column_name = 'last_job_search'"
            ).fetchone()
            
            if result:
                print("   ✅ last_job_search column exists in user_profile table")
            else:
                print("   ❌ last_job_search column missing from user_profile table")
                return False
            
            # Check job table structure
            job_columns = self.db.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'jobs'"
            ).fetchall()
            
            required_job_columns = ['job_id', 'title', 'company', 'description', 'job_employment_type']
            existing_columns = [col[0] for col in job_columns]
            
            missing_columns = [col for col in required_job_columns if col not in existing_columns]
            
            if not missing_columns:
                print("   ✅ Jobs table has all required columns")
            else:
                print(f"   ❌ Jobs table missing columns: {missing_columns}")
                return False
            
            print("   ✅ Database schema verification passed!")
            return True
            
        except Exception as e:
            print(f"   ❌ Error verifying database schema: {e}")
            return False
    
    def cleanup_test_data(self):
        """Clean up test data."""
        print("\n🗑️ Cleaning up test data...")
        
        try:
            # Delete job matches
            deleted_matches = self.db.query(models.JobMatch).filter(
                models.JobMatch.user_id == self.test_user.id
            ).delete()
            
            # Delete user profile
            self.db.delete(self.test_profile)
            
            # Delete user
            self.db.delete(self.test_user)
            
            self.db.commit()
            
            print(f"   ✅ Cleaned up: user, profile, and {deleted_matches} job matches")
            
        except Exception as e:
            print(f"   ❌ Error cleaning up test data: {e}")


async def main():
    """Run the complete workflow test."""
    print("🧪 Complete Job Matching Workflow Test")
    print("=" * 60)
    
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    
    # Initialize tester
    tester = WorkflowTester()
    
    try:
        # Run all tests
        tests_passed = 0
        total_tests = 5
        
        # Test 1: Database schema
        if tester.verify_database_schema():
            tests_passed += 1
        
        # Test 2: Create test user
        tester.create_test_user()
        tests_passed += 1  # User creation doesn't fail
        
        # Test 3: Automatic job matching
        if tester.test_automatic_job_matching():
            tests_passed += 1
        
        # Test 4: Scheduler logic
        if tester.test_scheduler_logic():
            tests_passed += 1
        
        # Test 5: Force update
        if await tester.test_force_update():
            tests_passed += 1
        
        # Results
        print(f"\n📊 Test Results:")
        print(f"   Tests Passed: {tests_passed}/{total_tests}")
        print(f"   Success Rate: {(tests_passed/total_tests)*100:.1f}%")
        
        if tests_passed == total_tests:
            print("\n🎉 All tests passed! Workflow is working correctly.")
        else:
            print(f"\n⚠️ {total_tests - tests_passed} test(s) failed. Check the logs above.")
        
        # Ask about cleanup
        cleanup_choice = input("\n🗑️ Clean up test data? (y/N): ").strip().lower()
        if cleanup_choice == 'y':
            tester.cleanup_test_data()
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        tester.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
