#!/usr/bin/env python3

import requests
import json

def test_job_matching_api():
    """Test job matching through the API endpoints"""
    print("🔍 Testing Job Matching through API...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test if API is accessible
        response = requests.get(f"{base_url}/")
        print(f"✅ API accessible: {response.status_code}")
        
        # Let's check what endpoints are available
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            api_spec = response.json()
            print("📊 Available endpoints:")
            for path, methods in api_spec.get('paths', {}).items():
                print(f"   {path}: {list(methods.keys())}")
        
        # Test user registration first
        test_user_data = {
            "username": "test_job_matcher",
            "email": "testjobmatcher@example.com", 
            "password": "testpassword123"
        }
        
        print(f"\n🔑 Testing user registration...")
        response = requests.post(f"{base_url}/auth/register", json=test_user_data)
        print(f"   Registration response: {response.status_code}")
        if response.status_code != 200:
            print(f"   Response: {response.text}")
        
        # Test login
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        
        print(f"\n🔐 Testing login...")
        response = requests.post(f"{base_url}/auth/login", data=login_data)
        print(f"   Login response: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print(f"   ✅ Login successful, token obtained")
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Test profile endpoints
            print(f"\n📊 Testing profile endpoints...")
            response = requests.get(f"{base_url}/profile/", headers=headers)
            print(f"   Profile fetch: {response.status_code}")
            
            if response.status_code == 200:
                profile_data = response.json()
                print(f"   Profile data keys: {list(profile_data.keys()) if profile_data else 'None'}")
            
            # Now test job matching - we need to trigger it somehow
            # Let's look for job matching related endpoints
            print(f"\n🎯 Looking for job matching endpoints...")
            
        else:
            print(f"   Login failed: {response.text}")
    
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_job_matching_api()
