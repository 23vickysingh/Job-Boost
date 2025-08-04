#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

def main():
    print("🔍 Debugging Job Matching Service...")
    
    # Check environment variables
    api_key = os.getenv("JSEARCH_API_KEY")
    print(f"API Key present: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"API Key length: {len(api_key)} characters")
    
    try:
        from services.job_matcher import get_job_matching_service
        print("✅ Successfully imported job_matcher module")
        
        service = get_job_matching_service()
        if service:
            print("✅ Job matching service created successfully")
            
            # Test basic functionality
            print("\n🧪 Testing job search functionality...")
            jobs = service.search_jobs("software engineer", "Remote")
            if jobs and 'data' in jobs:
                print(f"✅ Job search successful - found {len(jobs['data'])} jobs")
                if jobs['data']:
                    first_job = jobs['data'][0]
                    print(f"   First job: {first_job.get('job_title', 'N/A')} at {first_job.get('employer_name', 'N/A')}")
            else:
                print("❌ Job search failed or returned no data")
                print(f"Response: {jobs}")
        else:
            print("❌ Failed to create job matching service")
            
    except Exception as e:
        print(f"❌ Error importing or testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
