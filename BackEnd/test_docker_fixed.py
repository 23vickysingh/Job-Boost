#!/usr/bin/env python3

import sys
import os
sys.path.append('/usr/src/app')

# Test basic functionality
print('🔍 Testing inside Docker container...')

try:
    from services.job_matcher import get_job_matching_service
    print('✅ Job matcher imported successfully')
    
    service = get_job_matching_service()
    if service:
        print('✅ Job matching service created')
        print(f'   API key present: {len(service.api_key) > 0}')
    else:
        print('❌ Job matching service not created')
        
    from database import SessionLocal
    db = SessionLocal()
    print('✅ Database connection successful')
    
    # Check existing data
    from models import User, UserProfile, Job, JobMatch
    user_count = db.query(User).count()
    profile_count = db.query(UserProfile).count()
    job_count = db.query(Job).count()
    match_count = db.query(JobMatch).count()
    
    print(f'📊 Database stats:')
    print(f'   Users: {user_count}')
    print(f'   Profiles: {profile_count}') 
    print(f'   Jobs: {job_count}')
    print(f'   Matches: {match_count}')
    
    # If there are existing users, test job matching
    if user_count > 0 and profile_count > 0:
        print('\n🚀 Testing job matching with existing user...')
        profile = db.query(UserProfile).first()
        user_id = profile.user_id
        
        print(f'   Testing with user ID: {user_id}')
        print(f'   User query: {profile.query}')
        print(f'   User location: {profile.location}')
        print(f'   User resume skills: {profile.resume_parsed.get("skills", [])[:5] if profile.resume_parsed else "None"}')
        
        if profile.query and profile.location:
            print('\n📡 Starting job matching process...')
            result = service.process_job_matching_for_user(user_id, db)
            print(f'📊 Job matching result:')
            print(f'   Success: {result.get("success", False)}')
            print(f'   Jobs Processed: {result.get("jobs_processed", 0)}')
            print(f'   Jobs Stored: {result.get("jobs_stored", 0)}')
            print(f'   Matches Created: {result.get("matches_created", 0)}')
            print(f'   Message: {result.get("message", "N/A")}')
            
            # Check updated database stats
            new_job_count = db.query(Job).count()
            new_match_count = db.query(JobMatch).filter(JobMatch.user_id == user_id).count()
            print(f'\n📈 Updated Database stats:')
            print(f'   Total jobs now: {new_job_count} (was {job_count})')
            print(f'   User matches now: {new_match_count}')
            
            # Show top matches
            if new_match_count > 0:
                matches = db.query(JobMatch).filter(JobMatch.user_id == user_id).order_by(JobMatch.relevance_score.desc()).limit(3).all()
                print(f'\n🎯 Top 3 job matches:')
                for i, match in enumerate(matches):
                    job = match.job
                    print(f'   {i+1}. {job.job_title} at {job.employer_name}')
                    print(f'      Relevance: {match.relevance_score:.2f}, Location: {job.job_city}, {job.job_state}')
        else:
            print('   ⚠️ User missing job preferences (query/location)')
    else:
        print('   ⚠️ No users/profiles found to test with')
        print('   Creating a test user for demonstration...')
        
        # Create test user and profile
        from auth.hashing import Hash
        from datetime import datetime
        
        test_user = User(
            username="test_job_matcher_docker",
            email="testjobmatcher_docker@example.com",
            hashed_password=Hash.bcrypt("testpassword123"),
            is_verified=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        mock_resume_data = {
            "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "JavaScript", "AWS", "Git"],
            "experience": ["Senior Software Engineer at TechCorp - 4 years", "Full-stack Developer at StartupLabs - 3 years"],
            "education": ["Master's in Computer Science"],
            "languages": ["English"]
        }
        
        test_profile = UserProfile(
            user_id=test_user.id,
            query="Python Software Engineer",
            location="Remote",
            resume_parsed=mock_resume_data,
            resume_location="/test/resume.pdf",
            last_updated=datetime.utcnow()
        )
        db.add(test_profile)
        db.commit()
        db.refresh(test_profile)
        
        print(f'   ✅ Created test user {test_user.id} with profile')
        
        # Test job matching
        print('\n📡 Testing job matching with new test user...')
        result = service.process_job_matching_for_user(test_user.id, db)
        print(f'📊 Job matching result:')
        print(f'   Success: {result.get("success", False)}')
        print(f'   Jobs Processed: {result.get("jobs_processed", 0)}')
        print(f'   Jobs Stored: {result.get("jobs_stored", 0)}')
        print(f'   Matches Created: {result.get("matches_created", 0)}')
        print(f'   Message: {result.get("message", "N/A")}')
    
    db.close()
    print('\n🎉 Docker container test completed!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
