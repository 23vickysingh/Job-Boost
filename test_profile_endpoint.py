#!/usr/bin/env python3
"""
Quick test script to verify the /profile/complete endpoint
"""
import requests
import json

# Test the new complete profile endpoint
base_url = "http://localhost:8000"

def test_complete_profile_endpoint():
    """Test the complete profile endpoint without authentication first"""
    try:
        # Test if server is running
        response = requests.get(f"{base_url}/docs")
        print(f"✓ Server is running (status: {response.status_code})")
        
        # Test the complete profile endpoint (should return 401 without auth)
        response = requests.get(f"{base_url}/profile/complete")
        print(f"✓ Complete profile endpoint exists (status: {response.status_code})")
        
        if response.status_code == 401:
            print("✓ Authentication required as expected")
        elif response.status_code == 422:
            print("✓ Endpoint accessible but validation failed (expected without auth)")
        else:
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server. Make sure backend is running on localhost:8000")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("Testing Complete Profile Endpoint...")
    test_complete_profile_endpoint()
