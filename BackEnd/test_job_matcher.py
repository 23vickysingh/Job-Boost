#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from services.job_matcher import get_job_matching_service
from database import SessionLocal

def test_job_matching_service():
    """Test the job matching service initialization"""
    print("🧪 Testing Job Matching Service...")
    
    # Test service initialization
    service = get_job_matching_service()
    if service:
        print('✅ Job matching service initialized successfully')
        print(f'   API Key configured: {"Yes" if service.api_key else "No"}')
        
        # Test database connection
        try:
            db = SessionLocal()
            print('✅ Database connection successful')
            db.close()
        except Exception as e:
            print(f'❌ Database connection failed: {e}')
            
        return True
    else:
        print('❌ Failed to initialize job matching service')
        return False

if __name__ == "__main__":
    test_job_matching_service()
