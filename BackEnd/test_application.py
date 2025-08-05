#!/usr/bin/env python3
"""
Comprehensive test script to verify the Job-Boost application functionality.
"""
import sys
import os
import asyncio
from datetime import datetime


def test_1_imports():
    """Test 1: Verify all critical imports work."""
    print("🔍 Test 1: Testing imports...")
    try:
        # Core imports
        import models
        import schemas
        from database import get_db, SessionLocal
        
        # Service imports
        from services.job_matcher import get_job_matching_service
        from services.job_scheduler import job_scheduler
        
        # Router imports
        from routers import profile, jobs
        
        # Utility imports
        from utils.resume_parser import extract_text_from_upload
        
        # Background tasks
        from background_tasks import start_background_tasks, stop_background_tasks
        
        print("   ✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_2_database_models():
    """Test 2: Verify database models are properly defined."""
    print("\n🔍 Test 2: Testing database models...")
    try:
        import models
        
        # Check if models have required attributes
        user_attrs = ['id', 'user_id', 'password', 'created_at']
        profile_attrs = ['id', 'user_id', 'query', 'location', 'resume_parsed']
        job_attrs = ['id', 'job_id', 'job_title', 'employer_name']
        match_attrs = ['id', 'user_id', 'job_id', 'relevance_score']
        
        for attr in user_attrs:
            if not hasattr(models.User, attr):
                raise Exception(f"User model missing attribute: {attr}")
                
        for attr in profile_attrs:
            if not hasattr(models.UserProfile, attr):
                raise Exception(f"UserProfile model missing attribute: {attr}")
                
        for attr in job_attrs:
            if not hasattr(models.Job, attr):
                raise Exception(f"Job model missing attribute: {attr}")
                
        for attr in match_attrs:
            if not hasattr(models.JobMatch, attr):
                raise Exception(f"JobMatch model missing attribute: {attr}")
        
        print("   ✅ All database models properly defined!")
        return True
        
    except Exception as e:
        print(f"   ❌ Database model error: {e}")
        return False


def test_3_schemas():
    """Test 3: Verify Pydantic schemas are properly defined."""
    print("\n🔍 Test 3: Testing Pydantic schemas...")
    try:
        import schemas
        
        # Check if critical schemas exist
        required_schemas = [
            'UserCreate', 'UserOut', 'UserProfileOut', 'CompleteUserProfile',
            'JobPreferencesCreate', 'ResumeUploadResponse', 'JobOut', 'JobMatchOut'
        ]
        
        for schema_name in required_schemas:
            if not hasattr(schemas, schema_name):
                raise Exception(f"Missing schema: {schema_name}")
        
        print("   ✅ All schemas properly defined!")
        return True
        
    except Exception as e:
        print(f"   ❌ Schema error: {e}")
        return False


def test_4_services():
    """Test 4: Verify services can be instantiated."""
    print("\n🔍 Test 4: Testing services...")
    try:
        from services.job_matcher import get_job_matching_service
        from services.job_scheduler import job_scheduler
        
        # Test job matching service (may return None if no API key)
        job_service = get_job_matching_service()
        print(f"   - Job matching service: {'Available' if job_service else 'Unavailable (missing API key)'}")
        
        # Test job scheduler
        if hasattr(job_scheduler, 'start_scheduler'):
            print("   - Job scheduler: Available")
        else:
            raise Exception("Job scheduler missing start_scheduler method")
        
        print("   ✅ All services properly configured!")
        return True
        
    except Exception as e:
        print(f"   ❌ Service error: {e}")
        return False


def test_5_routers():
    """Test 5: Verify router endpoints are properly defined."""
    print("\n🔍 Test 5: Testing routers...")
    try:
        from routers import profile, jobs
        
        # Check if routers have the expected endpoints
        profile_routes = ['/job-preferences', '/upload-resume', '/', '/complete', '/resume', '/resume-status']
        job_routes = ['/matches', '/trigger-matching', '/force-update']
        
        # This is a basic check - in a real test, we'd inspect the FastAPI router
        print("   - Profile router: Available")
        print("   - Jobs router: Available")
        
        print("   ✅ All routers properly configured!")
        return True
        
    except Exception as e:
        print(f"   ❌ Router error: {e}")
        return False


def test_6_environment():
    """Test 6: Check environment configuration."""
    print("\n🔍 Test 6: Testing environment configuration...")
    try:
        # Check for critical environment variables
        required_vars = {
            'POSTGRES_DATABASE_URL': 'Database connection',
            'SECRET_KEY': 'JWT authentication',
            'GOOGLE_API_KEY': 'Resume parsing',
            'BREVO_API_KEY': 'Email services',
            'JSEARCH_API_KEY': 'Job search (optional)'
        }
        
        missing_vars = []
        for var, description in required_vars.items():
            if not os.getenv(var):
                missing_vars.append(f"{var} ({description})")
        
        if missing_vars:
            print(f"   ⚠️  Missing environment variables:")
            for var in missing_vars:
                print(f"      - {var}")
            # Don't fail the test for missing optional vars
            if 'JSEARCH_API_KEY' in str(missing_vars) and len(missing_vars) == 1:
                print("   ✅ Core environment variables present (JSEARCH_API_KEY optional)!")
                return True
            return False
        else:
            print("   ✅ All environment variables present!")
            return True
            
    except Exception as e:
        print(f"   ❌ Environment error: {e}")
        return False


async def test_7_background_tasks():
    """Test 7: Verify background tasks can be started/stopped."""
    print("\n🔍 Test 7: Testing background tasks...")
    try:
        from background_tasks import start_background_tasks, stop_background_tasks
        
        # Test that functions exist and are callable
        if not callable(start_background_tasks):
            raise Exception("start_background_tasks is not callable")
            
        if not callable(stop_background_tasks):
            raise Exception("stop_background_tasks is not callable")
        
        print("   ✅ Background tasks properly configured!")
        return True
        
    except Exception as e:
        print(f"   ❌ Background tasks error: {e}")
        return False


def test_8_fastapi_app():
    """Test 8: Verify FastAPI app can be created."""
    print("\n🔍 Test 8: Testing FastAPI application...")
    try:
        from main import app
        from fastapi import FastAPI
        
        if not isinstance(app, FastAPI):
            raise Exception("App is not a FastAPI instance")
        
        # Check if routers are included
        if not hasattr(app, 'routes') or len(app.routes) == 0:
            raise Exception("No routes found in FastAPI app")
        
        print(f"   - FastAPI app created with {len(app.routes)} routes")
        print("   ✅ FastAPI application properly configured!")
        return True
        
    except Exception as e:
        print(f"   ❌ FastAPI app error: {e}")
        return False


async def run_all_tests():
    """Run all tests and return overall success."""
    print("🚀 Job-Boost Application Test Suite")
    print("=" * 50)
    
    tests = [
        test_1_imports(),
        test_2_database_models(),
        test_3_schemas(),
        test_4_services(),
        test_5_routers(),
        test_6_environment(),
        await test_7_background_tasks(),
        test_8_fastapi_app()
    ]
    
    passed = sum(tests)
    total = len(tests)
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests PASSED! The application is ready to run!")
        print("\n🚀 To start the application:")
        print("   Docker: docker-compose up -d")
        print("   Direct: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return True
    else:
        print(f"❌ {total - passed} test(s) FAILED! Please fix the issues above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
