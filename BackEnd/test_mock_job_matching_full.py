#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
sys.path.append('.')

def test_job_matching_with_mock_api():
    """Test job matching with mock API responses"""
    print("🔍 Testing Job Matching with Mock API Responses...")
    
    try:
        from services.job_matcher import JobMatchingService
        from database import SessionLocal
        import models
        from auth.hashing import Hash
        from datetime import datetime
        
        print("✅ Modules imported successfully")
        
        # Create a custom job matching service that uses mock data
        class MockJobMatchingService(JobMatchingService):
            def search_jobs(self, query: str, location: str = "USA", employment_type: str = None):
                """Return mock job data instead of calling real API"""
                print(f"🎭 Mock API: Searching for '{query}' in '{location}'")
                return {
                    "status": "OK",
                    "request_id": "mock-request-123",
                    "parameters": {
                        "query": query,
                        "page": 1,
                        "num_pages": 1
                    },
                    "data": [
                        {
                            "job_id": "mock_001",
                            "job_title": "Senior Python Developer",
                            "employer_name": "TechCorp Inc",
                            "job_description": "We are seeking a Senior Python Developer with 5+ years of experience in building scalable web applications using FastAPI, Django, and modern frameworks. Experience with PostgreSQL, Redis, and cloud technologies required.",
                            "job_required_skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
                            "job_city": "Remote",
                            "job_state": "Anywhere",
                            "job_country": "US",
                            "job_employment_type": "FULLTIME",
                            "job_max_salary": 140000,
                            "job_min_salary": 120000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-15T10:00:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-15T10:00:00Z"
                        },
                        {
                            "job_id": "mock_002", 
                            "job_title": "Full Stack Engineer",
                            "employer_name": "StartupLabs",
                            "job_description": "Looking for a Full Stack Engineer proficient in Python backend development and React frontend. Must have experience with API development, database design, and modern web technologies.",
                            "job_required_skills": ["Python", "React", "JavaScript", "PostgreSQL", "Git"],
                            "job_city": "San Francisco",
                            "job_state": "CA",
                            "job_country": "US",
                            "job_employment_type": "FULLTIME",
                            "job_max_salary": 130000,
                            "job_min_salary": 110000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-14T15:30:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-14T15:30:00Z"
                        },
                        {
                            "job_id": "mock_003",
                            "job_title": "Backend Python Developer",
                            "employer_name": "DataFlow Systems",
                            "job_description": "Backend Python Developer needed for data processing applications. Experience with FastAPI, microservices, and cloud platforms essential.",
                            "job_required_skills": ["Python", "FastAPI", "Microservices", "AWS", "SQL"],
                            "job_city": "Austin",
                            "job_state": "TX", 
                            "job_country": "US",
                            "job_employment_type": "FULLTIME",
                            "job_max_salary": 125000,
                            "job_min_salary": 105000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-13T09:00:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-13T09:00:00Z"
                        },
                        {
                            "job_id": "mock_004",
                            "job_title": "Data Engineer",
                            "employer_name": "Analytics Pro",
                            "job_description": "Data Engineer role focusing on Python-based ETL pipelines, data warehousing, and analytics infrastructure.",
                            "job_required_skills": ["Python", "Pandas", "SQL", "ETL", "Data Warehousing"],
                            "job_city": "Remote",
                            "job_state": "Anywhere",
                            "job_country": "US",
                            "job_employment_type": "FULLTIME",
                            "job_max_salary": 135000,
                            "job_min_salary": 115000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-12T14:00:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-12T14:00:00Z"
                        },
                        {
                            "job_id": "mock_005",
                            "job_title": "DevOps Engineer",
                            "employer_name": "CloudOps LLC",
                            "job_description": "DevOps Engineer with Python scripting skills. Experience with Docker, Kubernetes, CI/CD, and cloud infrastructure automation.",
                            "job_required_skills": ["Python", "Docker", "Kubernetes", "AWS", "CI/CD"],
                            "job_city": "Seattle",
                            "job_state": "WA",
                            "job_country": "US", 
                            "job_employment_type": "FULLTIME",
                            "job_max_salary": 145000,
                            "job_min_salary": 125000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-11T11:00:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-11T11:00:00Z"
                        },
                        {
                            "job_id": "mock_006",
                            "job_title": "Machine Learning Engineer",
                            "employer_name": "AI Innovations",
                            "job_description": "ML Engineer specializing in Python-based machine learning models, data preprocessing, and model deployment.",
                            "job_required_skills": ["Python", "Machine Learning", "TensorFlow", "Pandas", "NumPy"],
                            "job_city": "Boston",
                            "job_state": "MA",
                            "job_country": "US",
                            "job_employment_type": "FULLTIME",
                            "job_max_salary": 155000,
                            "job_min_salary": 135000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-10T16:00:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-10T16:00:00Z"
                        },
                        {
                            "job_id": "mock_007",
                            "job_title": "Software Engineer",
                            "employer_name": "Enterprise Solutions",
                            "job_description": "Software Engineer position requiring strong Python skills, web development experience, and database knowledge.",
                            "job_required_skills": ["Python", "Django", "PostgreSQL", "JavaScript", "HTML"],
                            "job_city": "Chicago",
                            "job_state": "IL",
                            "job_country": "US",
                            "job_employment_type": "FULLTIME",
                            "job_max_salary": 120000,
                            "job_min_salary": 100000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-09T13:00:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-09T13:00:00Z"
                        },
                        {
                            "job_id": "mock_008",
                            "job_title": "API Developer",
                            "employer_name": "Integration Hub",
                            "job_description": "API Developer focused on building RESTful APIs using Python FastAPI. Experience with API documentation and testing required.",
                            "job_required_skills": ["Python", "FastAPI", "REST APIs", "OpenAPI", "Testing"],
                            "job_city": "Denver",
                            "job_state": "CO",
                            "job_country": "US",
                            "job_employment_type": "FULLTIME",
                            "job_max_salary": 115000,
                            "job_min_salary": 95000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-08T10:30:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-08T10:30:00Z"
                        },
                        {
                            "job_id": "mock_009",
                            "job_title": "Web Developer",
                            "employer_name": "WebCraft Studios",
                            "job_description": "Web Developer with Python and frontend skills. Experience with modern web frameworks and responsive design needed.",
                            "job_required_skills": ["Python", "Flask", "React", "CSS", "HTML"],
                            "job_city": "Portland",
                            "job_state": "OR",
                            "job_country": "US",
                            "job_employment_type": "FULLTIME",
                            "job_max_salary": 105000,
                            "job_min_salary": 85000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-07T12:00:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-07T12:00:00Z"
                        },
                        {
                            "job_id": "mock_010",
                            "job_title": "Python Consultant",
                            "employer_name": "Tech Consulting Group",
                            "job_description": "Python Consultant for various client projects. Must have expertise in Python development, architecture design, and client communication.",
                            "job_required_skills": ["Python", "Architecture", "Consulting", "Communication", "Problem Solving"],
                            "job_city": "Remote",
                            "job_state": "Anywhere",
                            "job_country": "US",
                            "job_employment_type": "CONTRACT",
                            "job_max_salary": 150000,
                            "job_min_salary": 130000,
                            "job_salary_currency": "USD",
                            "job_posted_at_datetime_utc": "2024-01-06T08:00:00Z",
                            "job_offer_expiration_datetime_utc": "2024-02-06T08:00:00Z"
                        }
                    ]
                }
            
            def get_job_details(self, job_id: str):
                """Return the same mock job data for details"""
                jobs_data = self.search_jobs("mock", "mock")
                if jobs_data and 'data' in jobs_data:
                    for job in jobs_data['data']:
                        if job['job_id'] == job_id:
                            return job
                return None
        
        # Initialize mock service
        mock_service = MockJobMatchingService("mock-api-key")
        print("✅ Mock job matching service initialized")
        
        # Create database session
        db = SessionLocal()
        
        # Create or get test user
        test_user = db.query(models.User).filter(models.User.username == "test_mock_user").first()
        
        if not test_user:
            print("🔧 Creating test user...")
            test_user = models.User(
                username="test_mock_user",
                email="testmockuser@example.com",
                hashed_password=Hash.bcrypt("testpassword123"),
                is_verified=True
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"✅ Test user created: {test_user.username} (ID: {test_user.id})")
        else:
            print(f"✅ Using existing test user: {test_user.username} (ID: {test_user.id})")
        
        # Create or update test profile
        profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == test_user.id
        ).first()
        
        mock_resume_data = {
            "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "JavaScript", "AWS", "Git"],
            "experience": ["Senior Software Engineer at TechCorp - 4 years", "Full-stack Developer at StartupLabs - 3 years"],
            "education": ["Master's in Computer Science", "Bachelor's in Software Engineering"],
            "languages": ["English", "Spanish"]
        }
        
        if not profile:
            print("🔧 Creating test profile...")
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
            profile.resume_parsed = mock_resume_data
            profile.query = "Python Software Engineer"
            profile.location = "Remote"
            db.commit()
            print(f"✅ Test profile updated for user {test_user.id}")
        
        # Now test job matching with mock service
        print(f"\n🚀 Starting job matching for user {test_user.id} with mock API...")
        
        result = mock_service.process_job_matching_for_user(test_user.id, db)
        
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
        ).order_by(models.JobMatch.relevance_score.desc()).all()
        
        print(f"\n📈 Database Status:")
        print(f"   Total jobs in database: {total_jobs}")
        print(f"   Job matches for user: {len(user_matches)}")
        
        if user_matches:
            print(f"\n🎯 Top Job Matches:")
            for i, match in enumerate(user_matches[:5]):
                job = match.job
                print(f"   {i+1}. {job.job_title} at {job.employer_name}")
                print(f"      Relevance: {match.relevance_score:.2f}, Salary: ${job.job_min_salary:,}-${job.job_max_salary:,}")
        
        print(f"\n🎉 Mock job matching test completed successfully!")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error in mock job matching test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_job_matching_with_mock_api()
