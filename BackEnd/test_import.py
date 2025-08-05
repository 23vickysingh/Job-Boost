#!/usr/bin/env python3
"""Test script to verify backend imports and basic functionality."""

try:
    print("Testing backend imports...")
    
    # Test core imports
    import main
    print("✅ Main app imported successfully")
    
    import database
    print("✅ Database module imported")
    
    import models
    print("✅ Models imported")
    
    import schemas
    print("✅ Schemas imported")
    
    # Test service imports
    from services import job_matcher
    print("✅ Job matcher service imported")
    
    from services import job_scheduler
    print("✅ Job scheduler service imported")
    
    # Test router imports
    from routers import user, profile, user_information
    print("✅ All routers imported")
    
    print("\n🎉 All imports successful! Backend is ready to run.")
    print("💡 You can now start the server with: uvicorn main:app --reload")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ General Error: {e}")
    import traceback
    traceback.print_exc()
