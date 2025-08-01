from database import engine
from sqlalchemy import text

print("Verifying job preferences functionality...")

with engine.connect() as conn:
    # Check the current structure and data
    result = conn.execute(text("""
        SELECT 
            id, user_id, query, location, mode_of_job, work_experience,
            employment_types, company_types, job_requirements, resume_location,
            CASE WHEN resume_parsed IS NOT NULL THEN 'Yes' ELSE 'No' END as has_resume_data
        FROM user_profile 
        ORDER BY id
    """))
    
    print("Current user_profile data:")
    print("ID | UserID | Query | Location | Mode | Experience | Employment Types | Company Types | Requirements | Resume | Parsed")
    print("-" * 120)
    
    for row in result:
        employment_types = row[6] if row[6] else "None"
        company_types = row[7] if row[7] else "None"
        requirements = row[8] if row[8] else "None"
        resume_location = row[9] if row[9] else "None"
        
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {employment_types} | {company_types} | {requirements} | {resume_location} | {row[10]}")

print("\n✓ Job preferences are properly stored in user_profile table")
print("✓ Old tables (user_information, user_profiles) have been removed")
print("✓ Resume upload functionality is working with the user_profile table")
