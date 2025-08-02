#!/usr/bin/env python3
"""
Test script to check backend endpoints
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'BackEnd'))

try:
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    print("Testing backend endpoints...")
    
    # Test root endpoint
    response = client.get("/")
    print(f"Root endpoint: {response.status_code}")
    
    # Test docs endpoint
    response = client.get("/docs")
    print(f"Docs endpoint: {response.status_code}")
    
    # Test profile endpoints (should return 401 without auth)
    response = client.get("/profile/")
    print(f"Profile endpoint: {response.status_code}")
    
    response = client.get("/profile/complete")
    print(f"Complete profile endpoint: {response.status_code}")
    
    if response.status_code == 404:
        print("❌ Complete profile endpoint not found!")
    elif response.status_code == 401:
        print("✅ Complete profile endpoint exists (requires auth)")
    else:
        print(f"Complete profile response: {response.text}")
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure FastAPI and dependencies are installed")
except Exception as e:
    print(f"Error: {e}")
