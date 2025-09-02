#!/usr/bin/env python3

import sys
import os
import asyncio
from dotenv import load_dotenv

# Add the BackEnd directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'BackEnd'))

# Load environment variables from the root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Test the ATS service
async def test_ats_service():
    print("Testing ATS Service with Gemini API...")
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key present: {bool(api_key)}")
    print(f"API Key length: {len(api_key) if api_key else 0}")
    
    if not api_key:
        print("❌ No Google API key found!")
        return
    
    # Import the ATS service
    try:
        from services.ats_service import ATSScoreCalculator
        print("✅ ATS Service imported successfully")
    except Exception as e:
        print(f"❌ Failed to import ATS service: {e}")
        return
    
    # Test with sample resume text
    sample_resume = """
    John Doe
    Software Engineer
    john.doe@email.com
    (555) 123-4567
    
    EXPERIENCE
    Software Developer at Tech Company (2020-2023)
    - Developed web applications using Python, JavaScript, React
    - Worked with databases like PostgreSQL and MongoDB
    - Implemented CI/CD pipelines using Docker and Jenkins
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology (2016-2020)
    
    SKILLS
    Python, JavaScript, React, Node.js, Docker, Git, AWS, PostgreSQL
    """
    
    try:
        calculator = ATSScoreCalculator()
        score = await calculator.calculate_ats_score(sample_resume)
        print(f"✅ ATS Score calculated: {score}")
        print(f"ATS Percentage: {int(score * 100)}%")
        
        if score == 1.0:
            print("⚠️  Score is exactly 1.0 - this might indicate an issue with the calculation")
        else:
            print("✅ Score looks reasonable")
            
    except Exception as e:
        print(f"❌ Failed to calculate ATS score: {e}")

if __name__ == "__main__":
    asyncio.run(test_ats_service())
