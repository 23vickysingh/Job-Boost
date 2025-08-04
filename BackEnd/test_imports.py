#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
sys.path.append('.')

def test_imports():
    """Test all imports to identify any issues"""
    print("🔍 Testing all imports...")
    
    try:
        print("   Importing database...")
        from database import SessionLocal
        print("   ✅ Database imported successfully")
        
        print("   Importing models...")
        import models
        print("   ✅ Models imported successfully")
        
        print("   Importing job_matcher...")
        from services.job_matcher import get_job_matching_service
        print("   ✅ Job matcher imported successfully")
        
        print("   Testing job service initialization...")
        service = get_job_matching_service()
        if service:
            print("   ✅ Job matching service created")
            print(f"   API Key length: {len(service.api_key) if service.api_key else 0}")
        else:
            print("   ❌ Job matching service not created")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()
