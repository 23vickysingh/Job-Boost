#!/usr/bin/env python3

import sys
import os
sys.path.append('/app')

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
        
        if profile.query and profile.location:
            result = service.process_job_matching_for_user(user_id, db)
            print(f'📊 Job matching result:')
            print(f'   Success: {result.get("success", False)}')
            print(f'   Jobs Processed: {result.get("jobs_processed", 0)}')
            print(f'   Jobs Stored: {result.get("jobs_stored", 0)}')
            print(f'   Matches Created: {result.get("matches_created", 0)}')
            print(f'   Message: {result.get("message", "N/A")}')
        else:
            print('   ⚠️ User missing job preferences (query/location)')
    else:
        print('   ⚠️ No users/profiles found to test with')
    
    db.close()
    print('\n🎉 Docker container test completed!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
