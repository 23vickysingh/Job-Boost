#!/usr/bin/env python3

import requests
import json
import os

def test_complete_job_matching_workflow():
    """Test the complete job matching workflow by uploading a resume"""
    print("🔍 Testing Complete Job Matching Workflow...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test user registration
        test_user_data = {
            "username": "test_job_matcher_2",
            "email": "testjobmatcher2@example.com", 
            "password": "testpassword123"
        }
        
        print(f"🔑 Registering test user...")
        response = requests.post(f"{base_url}/user/register", json=test_user_data)
        print(f"   Registration response: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ User registered successfully")
        elif response.status_code == 400:
            print(f"   ℹ️ User may already exist, continuing...")
        else:
            print(f"   Response: {response.text}")
        
        # Test login
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        
        print(f"\n🔐 Logging in...")
        response = requests.post(f"{base_url}/user/login", data=login_data)
        print(f"   Login response: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print(f"   ✅ Login successful")
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # First, set job preferences
            preferences_data = {
                "query": "Python Software Engineer",
                "location": "Remote",
                "experience_level": "Mid",
                "job_type": "Full-time"
            }
            
            print(f"\n📋 Setting job preferences...")
            response = requests.post(f"{base_url}/profile/preferences", json=preferences_data, headers=headers)
            print(f"   Preferences response: {response.status_code}")
            if response.status_code != 200:
                print(f"   Response: {response.text}")
            
            # Create a mock resume file
            mock_resume_content = """
John Doe
Software Engineer

EXPERIENCE:
- 3+ years of Python development
- Experience with FastAPI, Django, Flask
- Database: PostgreSQL, MongoDB
- Frontend: React, JavaScript, TypeScript
- DevOps: Docker, AWS, CI/CD

SKILLS:
Python, FastAPI, React, PostgreSQL, Docker, AWS, JavaScript, TypeScript, Git, Linux

EDUCATION:
Bachelor's in Computer Science
            """.strip()
            
            # Create temporary resume file
            resume_filename = "test_resume.txt"
            with open(resume_filename, "w") as f:
                f.write(mock_resume_content)
            
            print(f"\n📄 Uploading resume...")
            with open(resume_filename, "rb") as f:
                files = {"file": (resume_filename, f, "text/plain")}
                response = requests.post(f"{base_url}/profile/upload-resume", files=files, headers=headers)
                
            print(f"   Resume upload response: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Resume uploaded successfully")
                print(f"   Resume parsing: {result.get('resume_parsing', {}).get('status', 'N/A')}")
                print(f"   Job matching: {result.get('job_matching', {}).get('status', 'N/A')}")
                print(f"   Matches found: {result.get('job_matching', {}).get('matches_found', 0)}")
                
                # Check job matches
                print(f"\n📊 Checking job matches...")
                response = requests.get(f"{base_url}/profile/job-matches", headers=headers)
                print(f"   Job matches response: {response.status_code}")
                
                if response.status_code == 200:
                    matches = response.json()
                    print(f"   Found {len(matches)} job matches")
                    for i, match in enumerate(matches[:3]):  # Show first 3
                        print(f"   Match {i+1}: {match.get('job_title', 'N/A')} at {match.get('company', 'N/A')} ({match.get('relevance_score', 0):.2f})")
                
            else:
                print(f"   Resume upload failed: {response.text}")
            
            # Clean up
            if os.path.exists(resume_filename):
                os.remove(resume_filename)
                
        else:
            print(f"   Login failed: {response.text}")
    
    except Exception as e:
        print(f"❌ Error testing workflow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_job_matching_workflow()
