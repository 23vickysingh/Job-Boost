#!/usr/bin/env python3

import sys
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_jsearch_api():
    """Test JSearch API directly"""
    print("🔍 Testing JSearch API directly...")
    
    api_key = os.getenv("JSEARCH_API_KEY")
    if not api_key:
        print("❌ API key not found")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    
    # Test API call
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": "Python developer",
        "page": "1",
        "num_pages": "1"
    }
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    
    try:
        print("📡 Making API request...")
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API call successful!")
            print(f"   Data keys: {list(data.keys())}")
            
            if 'data' in data and data['data']:
                print(f"   Found {len(data['data'])} jobs")
                first_job = data['data'][0]
                print(f"   First job: {first_job.get('job_title', 'N/A')} at {first_job.get('employer_name', 'N/A')}")
                return True
            else:
                print("   No job data found")
                print(f"   Response: {data}")
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    test_jsearch_api()
