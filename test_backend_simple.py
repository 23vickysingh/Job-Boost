#!/usr/bin/env python3
"""
Simple test to verify the backend profile endpoints are working
"""
import subprocess
import time
import requests
import sys
import os

def test_backend():
    """Test if backend is running and endpoints work"""
    backend_url = "http://localhost:8000"
    
    print("Testing Job-Boost Backend...")
    print("=" * 50)
    
    try:
        # Test if server is running
        response = requests.get(f"{backend_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            print("✅ FastAPI docs accessible at http://localhost:8000/docs")
        else:
            print(f"❌ Backend server responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("Please start the backend server with:")
        print("cd BackEnd")
        print("uvicorn main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False
    
    try:
        # Test profile endpoint (should return 401 without auth)
        response = requests.get(f"{backend_url}/profile/")
        if response.status_code == 401:
            print("✅ Profile endpoint exists and requires authentication")
        elif response.status_code == 422:
            print("✅ Profile endpoint exists (validation error expected)")
        else:
            print(f"⚠️  Profile endpoint returned unexpected status: {response.status_code}")
            
        # Test complete profile endpoint
        response = requests.get(f"{backend_url}/profile/complete")
        if response.status_code == 401:
            print("✅ Complete profile endpoint exists and requires authentication")
        elif response.status_code == 404:
            print("❌ Complete profile endpoint not found (404)")
        elif response.status_code == 422:
            print("✅ Complete profile endpoint exists (validation error expected)")
        else:
            print(f"⚠️  Complete profile endpoint returned unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("Backend test completed!")
    print("If all tests passed, the backend should work with the frontend.")
    print("\nNext steps:")
    print("1. Make sure backend is running: uvicorn main:app --reload --port 8000")
    print("2. Start frontend: npm run dev (from FrontEnd directory)")
    print("3. Test the profile section in the dashboard")
    
    return True

if __name__ == "__main__":
    test_backend()
