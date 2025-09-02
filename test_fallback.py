#!/usr/bin/env python3

import sys
import os
import asyncio
from dotenv import load_dotenv

# Add the BackEnd directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'BackEnd'))

# Load environment variables from the root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Test the fallback ATS scoring
async def test_fallback_scoring():
    print("Testing Fallback ATS Scoring...")
    
    # Import the ATS service
    try:
        from services.ats_service import ATSScoreCalculator
        print("✅ ATS Service imported successfully")
    except Exception as e:
        print(f"❌ Failed to import ATS service: {e}")
        return
    
    # Test with different resume samples
    samples = [
        {
            "name": "Basic Resume",
            "text": """
            John Doe
            john.doe@email.com
            (555) 123-4567
            
            EXPERIENCE
            Software Developer (2020-2023)
            - Worked on web development
            
            EDUCATION
            Computer Science Degree
            
            SKILLS
            Programming, teamwork
            """
        },
        {
            "name": "Detailed Technical Resume",
            "text": """
            Jane Smith
            jane.smith@email.com
            +1 (555) 987-6543
            
            PROFESSIONAL EXPERIENCE
            Senior Software Engineer at Tech Corp (2021-2024)
            - Developed scalable web applications using Python, JavaScript, and React
            - Implemented RESTful APIs and microservices architecture
            - Collaborated with cross-functional teams using Agile methodology
            - Led code reviews and mentored junior developers
            - Optimized database queries in PostgreSQL improving performance by 40%
            
            Software Developer at StartupCo (2019-2021)
            - Built responsive frontend applications using React, HTML5, CSS3
            - Integrated third-party APIs and payment systems
            - Implemented CI/CD pipelines using Docker and Jenkins
            - Worked with AWS services including EC2, S3, and RDS
            
            EDUCATION
            Master of Science in Computer Science
            University of Technology (2017-2019)
            
            Bachelor of Science in Software Engineering  
            State University (2013-2017)
            
            TECHNICAL SKILLS
            Languages: Python, JavaScript, TypeScript, Java, SQL
            Frameworks: React, Angular, Django, Flask, Node.js
            Databases: PostgreSQL, MongoDB, Redis
            Cloud: AWS, Azure, Docker, Kubernetes
            Tools: Git, Jenkins, JIRA, Slack
            
            SOFT SKILLS
            Leadership, Problem-solving, Communication, Analytical thinking,
            Team collaboration, Project management, Creative problem-solving
            
            PROJECTS
            E-commerce Platform (2023)
            - Built full-stack application serving 10,000+ users
            - Technologies: React, Node.js, PostgreSQL, AWS
            
            Machine Learning Recommendation System (2022)
            - Developed recommendation algorithm with 85% accuracy
            - Technologies: Python, TensorFlow, pandas, NumPy
            """
        },
        {
            "name": "Minimal Resume",
            "text": """
            Bob Wilson
            bob@email.com
            
            Work: Programmer (2022-2024)
            School: Computer Degree (2018-2022)
            Skills: Coding
            """
        }
    ]
    
    calculator = ATSScoreCalculator()
    
    for sample in samples:
        try:
            print(f"\n--- Testing: {sample['name']} ---")
            score = await calculator._fallback_ats_score(sample['text'])
            percentage = int(score * 100)
            print(f"ATS Score: {score:.2f} ({percentage}%)")
            
            if score == 1.0:
                print("⚠️  Score is exactly 1.0 - this suggests the calculation needs refinement")
            elif score > 0.8:
                print("✅ Excellent ATS compatibility")
            elif score > 0.6:
                print("✅ Good ATS compatibility") 
            elif score > 0.4:
                print("⚠️  Fair ATS compatibility")
            else:
                print("❌ Poor ATS compatibility")
                
        except Exception as e:
            print(f"❌ Failed to calculate score for {sample['name']}: {e}")

if __name__ == "__main__":
    asyncio.run(test_fallback_scoring())
