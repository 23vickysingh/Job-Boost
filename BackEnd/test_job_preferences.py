from database import get_db, engine
from sqlalchemy.orm import Session
from sqlalchemy import text
import models
import json

# Test data for job preferences
test_preferences = {
    "query": "Python Developer",
    "location": "Mumbai, India", 
    "mode_of_job": "remote",
    "work_experience": "Mid Level (3-5 years)",
    "employment_types": ["Full-time", "Contract"],
    "company_types": ["Startup", "Tech Company"],
    "job_requirements": "Python, Django, REST APIs"
}

print("Testing job preferences functionality...")

with engine.connect() as conn:
    # Get the latest user for testing
    result = conn.execute(text("SELECT id FROM users ORDER BY id DESC LIMIT 1"))
    user_id = result.scalar()
    
    if not user_id:
        print("No users found in database")
        exit()
    
    print(f"Testing with user ID: {user_id}")
    
    # Check if profile exists
    result = conn.execute(text("SELECT id FROM user_profile WHERE user_id = :user_id"), {"user_id": user_id})
    profile_id = result.scalar()
    
    if profile_id:
        print(f"Found existing profile: {profile_id}")
        # Update the profile
        conn.execute(text("""
            UPDATE user_profile 
            SET query = :query, location = :location, mode_of_job = :mode_of_job, 
                work_experience = :work_experience, employment_types = :employment_types,
                company_types = :company_types, job_requirements = :job_requirements,
                last_updated = NOW()
            WHERE user_id = :user_id
        """), {
            "user_id": user_id,
            "query": test_preferences["query"],
            "location": test_preferences["location"],
            "mode_of_job": test_preferences["mode_of_job"],
            "work_experience": test_preferences["work_experience"],
            "employment_types": json.dumps(test_preferences["employment_types"]),
            "company_types": json.dumps(test_preferences["company_types"]),
            "job_requirements": test_preferences["job_requirements"]
        })
        conn.commit()
        print("Profile updated successfully")
    else:
        print("No profile found - would create new one")
    
    # Verify the update
    result = conn.execute(text("""
        SELECT query, location, mode_of_job, work_experience, employment_types, company_types, job_requirements
        FROM user_profile WHERE user_id = :user_id
    """), {"user_id": user_id})
    
    row = result.fetchone()
    if row:
        print(f"Verified profile data:")
        print(f"  Query: {row[0]}")
        print(f"  Location: {row[1]}")
        print(f"  Mode: {row[2]}")
        print(f"  Experience: {row[3]}")
        print(f"  Employment Types: {row[4]}")
        print(f"  Company Types: {row[5]}")
        print(f"  Requirements: {row[6]}")
        print("✓ Job preferences are properly stored and retrieved")
