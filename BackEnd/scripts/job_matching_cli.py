#!/usr/bin/env python3
"""
Job Matching CLI Tool

This script demonstrates the job matching functionality by:
1. Using the provided resume data from two.py
2. Fetching jobs from JSearch API
3. Calculating relevance scores
4. Displaying results

Usage:
    python job_matching_cli.py --api-key YOUR_API_KEY --query "Software Engineer" --location "USA"
"""

import argparse
import asyncio
import os
import sys
from typing import Dict, Any

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.job_matcher import JobMatchingService


# Resume data from two.py for testing
SAMPLE_RESUME_DATA = {
    "parsed_data": {
        "personal_info": {
            "name": "Vivek Singh",
            "email": "23vickysingh@gmail.com",
            "phone": "+91 9991348092",
            "linkedin": "linkedin.com/in/23vickysingh",
            "github": "github.com/CoderVicky23",
            "location": None
        },
        "summary": None,
        "experience": [],
        "education": [
            {"degree": "Masters in Computer Applications", "institution": "National Institute of Technology, Raipur", "dates": "2026", "gpa": "8.38 *", "location": "NIT Raipur"},
            {"degree": "Graduation", "institution": "University of Delhi", "dates": "2022", "gpa": "8.67", "location": "Dyal Singh College"},
            {"degree": "Intermediate", "institution": "CBSE", "dates": "2019", "gpa": "94.6%", "location": "Gurukul Kurukshetra"},
            {"degree": "Matriculation", "institution": "CBSE", "dates": "2016", "gpa": "9.8", "location": "Golaya Progressive Public School"}
        ],
        "skills": [
            "C", "C++", "Python", "Java", "HTML", "CSS", "JavaScript", "MySQL", "MongoDB", "Github", "VSCode",
            "UNIX", "Postman", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "React", "FastAPI", "Node JS", "MERN Stack"
        ],
        "projects": [
            {"name": "Research Scholars Conclave 2025 – Official Website Deployment", "technologies": ["HTML", "CSS", "JavaScript"], "description": "Designed and developed an interactive and responsive frontend using HTML, CSS, and vanilla JavaScript, tailored to showcase event schedules, registrations, and key updates. Successfully deployed the official event website on the NIT Raipur domain.", "link": None},
            {"name": "Resume-Based Job Finder Web Application", "technologies": ["React", "FastAPI", "MySQL", "Python", "API"], "description": "Engineered a dynamic full-stack web application that intelligently matches users to relevant job listings based on their uploaded resumes, improving job discovery efficiency. Integrated Python-based resume parsing and automated web scraping to collect and preprocess job descriptions across multiple platforms. Leveraged the generative AI APIs to semantically compare resumes with job descriptions for achieving high accuracy for relevance scoring and delivering personalized job recommendations.", "link": None},
            {"name": "MERN Stack E-COMMERCE Platform", "technologies": ["MongoDB", "Express", "React", "Node JS"], "description": "Designed and developed a fully responsive and scalable e-commerce web application with modern UI/UX to enhance customer experience across devices. Implemented essential features including secure user authentication, shopping cart management, and integrated payment gateway along with email facilitation. Ensured robust backend architecture and RESTful API design to support seamless product transactions and real-time data updates.", "link": None},
            {"name": "Chrome Extension for ChatGPT", "technologies": ["HTML", "CSS", "JavaScript"], "description": "Created a lightweight chrome extension to display the prompts of opened chat in a side panel and quickly navigate to a prompt by just clicking. Utilized the browser storage to implement the feature of star and renaming a prompt.", "link": None},
            {"name": "Intrusion Detection System using SVM", "technologies": ["Scikit-learn", "PyTorch", "CIC-IDS-2017 Dataset"], "description": "Pre-processed and trained dataset having 28,30,743 instances with 79 features and 15 classes. Built an IDS using SVM and optimized hyperparameters using Grid and Random Search. Improved classification accuracy from 91.33% to 94.31% on the test dataset.", "link": None},
            {"name": "TCP/IP Protocol Suite Implementation", "technologies": ["C++"], "description": "Simulated core components of TCP/IP including TLS handshake, key exchange, and session management. Gained deep understanding of OSI layers and secure communication protocols.", "link": None},
            {"name": "CPU Process Scheduling Simulator", "technologies": ["C++"], "description": "Designed and tested safe resource allocation with Banker's algorithm. Implemented various CPU scheduling strategies.", "link": None}
        ],
        "courses_undertaken": [
            "Data Structures & Algorithms", "Object-Oriented Programming", "Operating Systems", "DBMS", "Networks",
            "Computer Architecture", "Compilers", "Front End for web applications", "Back End and Database Management Systems",
            "Supervised/Unsupervised Learning", "Model Designing & Evaluation", "Feature Engineering"
        ]
    }
}


def display_job_comparison(job_summary: Dict[str, Any], relevance_score: float):
    """Display job information and relevance score."""
    print("-" * 60)
    print(f"🏢 Job Title: {job_summary.get('job_title', 'N/A')}")
    print(f"🏛️ Company: {job_summary.get('employer_name', 'N/A')}")
    
    # Format location
    location_parts = [
        job_summary.get('job_city', ''),
        job_summary.get('job_state', ''),
        job_summary.get('job_country', '')
    ]
    location = ', '.join(filter(None, location_parts))
    print(f"📍 Location: {location or 'N/A'}")
    
    # Display employment type
    employment_type = job_summary.get('job_employment_type', 'N/A')
    print(f"💼 Employment Type: {employment_type}")
    
    # Display salary if available
    min_salary = job_summary.get('job_min_salary')
    max_salary = job_summary.get('job_max_salary')
    currency = job_summary.get('job_salary_currency', '')
    period = job_summary.get('job_salary_period', '')
    
    if min_salary or max_salary:
        if min_salary and max_salary:
            salary_info = f"{currency}{min_salary:,.0f} - {currency}{max_salary:,.0f}"
        elif min_salary:
            salary_info = f"{currency}{min_salary:,.0f}+"
        else:
            salary_info = f"Up to {currency}{max_salary:,.0f}"
        
        if period:
            salary_info += f" per {period.lower()}"
        
        print(f"💰 Salary: {salary_info}")
    
    # Display relevance score with color coding
    if relevance_score >= 70:
        score_emoji = "🟢"
    elif relevance_score >= 50:
        score_emoji = "🟡"
    else:
        score_emoji = "🔴"
    
    print(f"⭐ Relevance Score: {score_emoji} {relevance_score:.2f}%")
    
    # Display apply link
    apply_link = job_summary.get('job_apply_link', 'N/A')
    print(f"🔗 Apply Link: {apply_link}")
    
    print("-" * 60 + "\n")


async def main():
    """Main function to run job matching demonstration."""
    parser = argparse.ArgumentParser(description="Job Matching CLI Tool")
    parser.add_argument("--api-key", required=True, help="JSearch API key")
    parser.add_argument("--query", default="Software Engineer", help="Job search query")
    parser.add_argument("--location", default="USA", help="Job location")
    parser.add_argument("--employment-type", help="Employment type filter")
    parser.add_argument("--max-jobs", type=int, default=3, help="Maximum number of jobs to process")
    
    args = parser.parse_args()
    
    print("🚀 Job Matching CLI Tool")
    print("=" * 60)
    print(f"📋 Search Parameters:")
    print(f"   Query: {args.query}")
    print(f"   Location: {args.location}")
    print(f"   Employment Type: {args.employment_type or 'Any'}")
    print(f"   Max Jobs: {args.max_jobs}")
    print("=" * 60)
    
    # Initialize job matching service
    job_service = JobMatchingService(args.api_key)
    job_service.max_jobs = args.max_jobs
    
    try:
        # Search for jobs
        print(f"\n🔍 Searching for jobs...")
        job_search_results = job_service.search_jobs(
            query=args.query,
            location=args.location,
            employment_type=args.employment_type
        )
        
        if not job_search_results or not job_search_results.get('data'):
            print("❌ No jobs found for the given search criteria")
            return
        
        # Limit jobs to process
        jobs_to_process = job_search_results['data'][:args.max_jobs]
        print(f"✅ Found {len(job_search_results['data'])} jobs, processing top {len(jobs_to_process)}")
        
        print(f"\n📊 Resume Analysis:")
        resume_skills = SAMPLE_RESUME_DATA['parsed_data']['skills']
        print(f"   Skills: {', '.join(resume_skills[:10])}...")
        print(f"   Total Skills: {len(resume_skills)}")
        print(f"   Projects: {len(SAMPLE_RESUME_DATA['parsed_data']['projects'])}")
        print(f"   Education: {len(SAMPLE_RESUME_DATA['parsed_data']['education'])}")
        
        print(f"\n🎯 Processing Jobs and Calculating Relevance Scores:")
        print("=" * 60)
        
        job_results = []
        
        for i, job_summary in enumerate(jobs_to_process, 1):
            job_id = job_summary.get('job_id')
            if not job_id:
                print(f"⚠️ Job {i}: Missing job_id, skipping")
                continue
            
            print(f"\n📌 Processing Job {i}/{len(jobs_to_process)}: {job_summary.get('job_title', 'Unknown')}")
            
            # Get detailed job information
            job_details = job_service.get_job_details(job_id)
            if not job_details:
                print(f"❌ Could not fetch details for job {job_id}")
                continue
            
            # Calculate relevance score
            relevance_score = job_service.calculate_relevance_score(
                SAMPLE_RESUME_DATA,
                job_details
            )
            
            job_results.append((job_summary, relevance_score))
            print(f"✅ Job {i} processed successfully")
        
        # Sort jobs by relevance score (highest first)
        job_results.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n🏆 Job Matching Results (Sorted by Relevance):")
        print("=" * 60)
        
        for i, (job_summary, relevance_score) in enumerate(job_results, 1):
            print(f"\n🥇 Rank {i}:")
            display_job_comparison(job_summary, relevance_score)
        
        # Summary statistics
        if job_results:
            scores = [score for _, score in job_results]
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)
            
            print("📈 Summary Statistics:")
            print("=" * 60)
            print(f"   Jobs Processed: {len(job_results)}")
            print(f"   Average Relevance Score: {avg_score:.2f}%")
            print(f"   Highest Score: {max_score:.2f}%")
            print(f"   Lowest Score: {min_score:.2f}%")
            print(f"   Jobs with >70% relevance: {sum(1 for score in scores if score >= 70)}")
            print(f"   Jobs with >50% relevance: {sum(1 for score in scores if score >= 50)}")
        
        print("\n🎉 Job matching completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during job matching: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
