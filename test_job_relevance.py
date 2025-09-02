#!/usr/bin/env python3

import sys
import os
import asyncio
from dotenv import load_dotenv

# Add the BackEnd directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'BackEnd'))

# Load environment variables from the root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Test the job relevance service for new job matching only
async def test_new_job_relevance_service():
    print("Testing Job Relevance Service for New Jobs Only...")
    print("=" * 55)
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key present: {bool(api_key)}")
    print(f"API Key length: {len(api_key) if api_key else 0}")
    
    if not api_key:
        print("❌ No Google API key found!")
        print("ℹ️  Fallback scoring will be used instead")
    
    # Import the job relevance service
    try:
        from services.job_relevance_service import JobRelevanceCalculator, calculate_relevance_on_job_creation
        print("✅ Job Relevance Service imported successfully")
    except Exception as e:
        print(f"❌ Failed to import Job Relevance service: {e}")
        return
    
    # Test with sample resume and job data
    sample_resume_data = {
        "personal_info": {
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "(555) 123-4567"
        },
        "summary": "Experienced software engineer with 5 years of experience in full-stack web development using Python, JavaScript, and React. Passionate about building scalable applications and working with agile teams.",
        "experience": [
            {
                "role": "Senior Software Engineer",
                "company": "Tech Solutions Inc",
                "dates": "2021-2024",
                "description": [
                    "Developed and maintained web applications using Python Django and React",
                    "Led a team of 3 junior developers and conducted code reviews",
                    "Implemented CI/CD pipelines using Docker and Jenkins",
                    "Optimized database queries resulting in 40% performance improvement"
                ]
            },
            {
                "role": "Full Stack Developer",
                "company": "StartupCorp",
                "dates": "2019-2021",
                "description": [
                    "Built responsive web applications using JavaScript, HTML, CSS",
                    "Integrated RESTful APIs and third-party services",
                    "Worked closely with product team using Agile methodology"
                ]
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "institution": "University of Technology",
                "dates": "2015-2019"
            }
        ],
        "skills": [
            "Python", "JavaScript", "React", "Django", "HTML", "CSS", "PostgreSQL",
            "Docker", "Jenkins", "Git", "Agile", "Scrum", "REST APIs", "AWS"
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "technologies": ["React", "Node.js", "PostgreSQL"],
                "description": "Built full-stack e-commerce application with payment integration"
            }
        ],
        "certifications": [
            "AWS Certified Developer Associate",
            "Scrum Master Certification"
        ]
    }
    
    # Test different new job scenarios
    new_job_opportunities = [
        {
            "title": "Senior Full Stack Developer",
            "description": """
            We are looking for a Senior Full Stack Developer to join our growing team.
            
            Responsibilities:
            - Develop and maintain web applications using modern frameworks
            - Work with Python/Django backend and React frontend
            - Collaborate with cross-functional teams in an Agile environment
            - Mentor junior developers and conduct code reviews
            - Optimize application performance and scalability
            
            Required Skills:
            - 4+ years of experience in full-stack development
            - Strong proficiency in Python, JavaScript, React
            - Experience with databases (PostgreSQL/MySQL)
            - Knowledge of DevOps practices (Docker, CI/CD)
            - Experience with cloud platforms (AWS preferred)
            - Strong communication and leadership skills
            
            Nice to have:
            - Django framework experience
            - Agile/Scrum methodology experience
            - AWS certifications
            """,
            "requirements": "4+ years full-stack development, Python, JavaScript, React, PostgreSQL, Docker",
            "expected_score": "High (0.8+) - Perfect match"
        },
        {
            "title": "Frontend Developer",
            "description": """
            Join our team as a Frontend Developer to create amazing user experiences.
            
            Responsibilities:
            - Develop responsive web applications using React
            - Collaborate with UI/UX designers
            - Optimize applications for maximum speed and scalability
            - Ensure cross-browser compatibility
            - Write clean, maintainable code
            
            Required Skills:
            - 3+ years of frontend development experience
            - Expert knowledge of JavaScript, HTML5, CSS3
            - Strong experience with React and modern JavaScript frameworks
            - Experience with responsive design and CSS frameworks
            - Knowledge of version control systems (Git)
            """,
            "requirements": "3+ years frontend development, JavaScript, React, HTML5, CSS3",
            "expected_score": "Good (0.6-0.8) - Strong frontend match"
        },
        {
            "title": "Product Manager",
            "description": """
            We are seeking a Product Manager to lead our product development initiatives.
            
            Responsibilities:
            - Define product strategy and roadmap
            - Gather and prioritize product requirements
            - Work closely with engineering and design teams
            - Analyze market trends and competitor products
            - Manage product launches and go-to-market strategies
            
            Required Skills:
            - 5+ years of product management experience
            - Strong analytical and problem-solving skills
            - Excellent communication and leadership abilities
            - Experience with agile development methodologies
            - Bachelor's degree in Business, Engineering, or related field
            """,
            "requirements": "5+ years product management, analytical skills, leadership, agile experience",
            "expected_score": "Low (0.2-0.4) - Different career path"
        }
    ]
    
    calculator = JobRelevanceCalculator()
    
    print("\n🎯 Testing New Job Opportunities vs Candidate Resume:")
    print("-" * 60)
    
    for i, job in enumerate(new_job_opportunities, 1):
        try:
            print(f"\n--- New Job Opportunity {i}: {job['title']} ---")
            print(f"Expected Match: {job['expected_score']}")
            
            # Test direct calculation
            score = await calculator.calculate_relevance_score(
                resume_data=sample_resume_data,
                job_description=job['description'],
                job_title=job['title'],
                job_requirements=job['requirements']
            )
            
            percentage = int(score * 100)
            print(f"📊 Calculated Relevance: {score:.2f} ({percentage}%)")
            
            # Provide hiring recommendation
            if score >= 0.8:
                print("🟢 RECOMMENDATION: Excellent candidate - Highly recommended for interview")
            elif score >= 0.6:
                print("🟡 RECOMMENDATION: Good candidate - Consider for interview") 
            elif score >= 0.4:
                print("🟠 RECOMMENDATION: Potential candidate - Review qualifications")
            elif score >= 0.2:
                print("🔴 RECOMMENDATION: Poor match - Significant skill gaps")
            else:
                print("⚫ RECOMMENDATION: Not suitable - Different career background")
            
            print(f"💡 API Calls Used: {'1 Gemini call' if api_key else '0 - Using fallback scoring'}")
                
        except Exception as e:
            print(f"❌ Failed to calculate relevance for {job['title']}: {e}")
    
    print(f"\n🎉 New Job Relevance Testing Completed!")
    print(f"🔑 Total Gemini API calls made: {len(new_job_opportunities) if api_key else 0}")
    print("💰 API calls are only used for new job-candidate matching")

if __name__ == "__main__":
    asyncio.run(test_new_job_relevance_service())
