#!/usr/bin/env python3
"""
Simple API Test Script

Tests the JSearch API integration without database dependencies.
Based on the logic from two.py.

Usage:
    python simple_api_test.py YOUR_API_KEY
"""

import sys
import json
import requests
import re
from collections import Counter


# Resume data from two.py
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
        ],
        "skills": [
            "C", "C++", "Python", "Java", "HTML", "CSS", "JavaScript", "MySQL", "MongoDB", "Github", "VSCode",
            "UNIX", "Postman", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "React", "FastAPI", "Node JS", "MERN Stack"
        ],
        "projects": [
            {"name": "Resume-Based Job Finder Web Application", "technologies": ["React", "FastAPI", "MySQL", "Python", "API"], "description": "Engineered a dynamic full-stack web application that intelligently matches users to relevant job listings based on their uploaded resumes, improving job discovery efficiency."},
            {"name": "MERN Stack E-COMMERCE Platform", "technologies": ["MongoDB", "Express", "React", "Node JS"], "description": "Designed and developed a fully responsive and scalable e-commerce web application with modern UI/UX to enhance customer experience across devices."},
        ],
        "courses_undertaken": [
            "Data Structures & Algorithms", "Object-Oriented Programming", "Operating Systems", "DBMS", "Networks",
            "Computer Architecture", "Compilers", "Front End for web applications", "Back End and Database Management Systems",
        ]
    }
}


def search_jobs(api_key, params):
    """Search for jobs using JSearch API."""
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
    
    try:
        print(f"🔍 Searching for jobs: {params['query']}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred during job search: {http_err}")
        print(f"Response content: {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"❌ An error occurred during job search: {err}")
    return None


def get_job_details(api_key, job_id):
    """Get detailed job information."""
    url = "https://jsearch.p.rapidapi.com/job-details"
    params = {"job_id": job_id}
    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
    
    try:
        print(f"📄 Fetching details for job_id: {job_id}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred fetching details for job_id {job_id}: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"❌ An error occurred fetching details for job_id {job_id}: {err}")
    return None


def calculate_relevance_score(resume_data, job_details):
    """Calculate relevance score between resume and job description."""
    resume_skills = set(skill.lower() for skill in resume_data['parsed_data']['skills'])
    
    # Extract keywords from resume projects and courses
    resume_keywords = set()
    for project in resume_data['parsed_data']['projects']:
        resume_keywords.update(word.lower() for word in re.findall(r'\w+', project['name']))
        resume_keywords.update(word.lower() for word in re.findall(r'\w+', project['description']))
        for tech in project.get('technologies', []):
            resume_keywords.update(word.lower() for word in re.findall(r'\w+', tech))
    
    for course in resume_data['parsed_data']['courses_undertaken']:
        resume_keywords.update(word.lower() for word in re.findall(r'\w+', course))

    # Job Data Extraction
    if not job_details or 'data' not in job_details or not job_details['data']:
        return 0
    
    job_data = job_details['data'][0]
    job_description_text = job_data.get('job_description', '').lower()
    
    # Extract skills from job qualifications if available
    job_skills = set()
    if job_data.get('job_highlights') and job_data['job_highlights'].get('Qualifications'):
        for qualification in job_data['job_highlights']['Qualifications']:
            job_skills.update(word.lower() for word in re.findall(r'\w+', qualification))
    
    # Fallback to parsing the whole description
    if not job_skills:
        job_skills.update(word.lower() for word in re.findall(r'\w+', job_description_text))

    # Scoring
    # 1. Skills Score (Weight: 70%)
    matching_skills = resume_skills.intersection(job_skills)
    skill_score = (len(matching_skills) / len(resume_skills)) * 100 if resume_skills else 0

    # 2. Keyword Score (Weight: 30%)
    job_description_words = set(re.findall(r'\w+', job_description_text))
    matching_keywords = resume_keywords.intersection(job_description_words)
    keyword_score = (len(matching_keywords) / len(resume_keywords)) * 100 if resume_keywords else 0

    # Weighted average
    relevance_score = (0.7 * skill_score) + (0.3 * keyword_score)
    
    print(f"📊 Scoring Details:")
    print(f"   Resume Skills: {len(resume_skills)}")
    print(f"   Matching Skills: {len(matching_skills)} ({skill_score:.2f}%)")
    print(f"   Resume Keywords: {len(resume_keywords)}")
    print(f"   Matching Keywords: {len(matching_keywords)} ({keyword_score:.2f}%)")
    print(f"   Final Score: {min(relevance_score, 100):.2f}%")
    
    return min(relevance_score, 100)


def display_job_comparison(job_summary, job_details, relevance_score):
    """Display job summary and relevance score."""
    job_title = job_summary.get('job_title', 'N/A')
    employer_name = job_summary.get('employer_name', 'N/A')
    location = f"{job_summary.get('job_city', '')}, {job_summary.get('job_state', '')}, {job_summary.get('job_country', '')}"
    
    print("-" * 60)
    print(f"🏢 Job Title: {job_title}")
    print(f"🏛️ Company: {employer_name}")
    print(f"📍 Location: {location}")
    print(f"💼 Employment Type: {job_summary.get('job_employment_type', 'N/A')}")
    
    # Salary info
    min_salary = job_summary.get('job_min_salary')
    max_salary = job_summary.get('job_max_salary')
    if min_salary or max_salary:
        salary_info = []
        if min_salary:
            salary_info.append(f"${min_salary:,.0f}")
        if max_salary:
            if min_salary:
                salary_info.append(f"- ${max_salary:,.0f}")
            else:
                salary_info.append(f"Up to ${max_salary:,.0f}")
        
        salary_str = " ".join(salary_info)
        if job_summary.get('job_salary_period'):
            salary_str += f" per {job_summary['job_salary_period'].lower()}"
        print(f"💰 Salary: {salary_str}")
    
    # Score with color coding
    if relevance_score >= 70:
        score_emoji = "🟢"
    elif relevance_score >= 50:
        score_emoji = "🟡"
    else:
        score_emoji = "🔴"
    
    print(f"⭐ Relevance Score: {score_emoji} {relevance_score:.2f}%")
    print(f"🔗 Apply: {job_summary.get('job_apply_link', 'N/A')}")
    
    # Job highlights
    if job_details and job_details.get('data') and job_details['data'][0].get('job_highlights'):
        highlights = job_details['data'][0]['job_highlights']
        if highlights.get('Qualifications'):
            print(f"📋 Key Qualifications:")
            for qual in highlights['Qualifications'][:3]:  # Show first 3
                print(f"   • {qual}")
    
    print("-" * 60 + "\n")


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python simple_api_test.py YOUR_API_KEY")
        sys.exit(1)
    
    API_KEY = sys.argv[1]
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("❌ Please replace 'YOUR_API_KEY_HERE' with your actual JSearch API key.")
        sys.exit(1)
    
    print("🚀 Simple Job Matching Test")
    print("=" * 60)
    
    # Search parameters
    search_parameters = {
        "query": "Software Engineer in USA",
        "page": "1",
        "num_pages": "1"
    }
    
    print(f"🔍 Search Query: {search_parameters['query']}")
    print("=" * 60)
    
    # Search for jobs
    job_search_results = search_jobs(API_KEY, search_parameters)

    if job_search_results and job_search_results.get('data'):
        # Limit to first 3 jobs
        top_jobs = job_search_results['data'][:3]
        print(f"\n✅ Found {len(job_search_results['data'])} jobs, processing top {len(top_jobs)}")
        
        print(f"\n📊 Resume Summary:")
        skills = SAMPLE_RESUME_DATA['parsed_data']['skills']
        print(f"   Skills: {', '.join(skills[:8])}...")
        print(f"   Total Skills: {len(skills)}")
        print(f"   Projects: {len(SAMPLE_RESUME_DATA['parsed_data']['projects'])}")
        
        print(f"\n🎯 Processing Jobs:")
        print("=" * 60)
        
        job_scores = []
        
        for i, job_summary in enumerate(top_jobs, 1):
            job_id = job_summary.get('job_id')
            if not job_id:
                print(f"⚠️ Job {i}: No job_id, skipping")
                continue
            
            print(f"\n📌 Processing Job {i}: {job_summary.get('job_title', 'Unknown')}")
            
            # Fetch full details
            job_details_data = get_job_details(API_KEY, job_id)
            
            if job_details_data:
                # Calculate relevance score
                score = calculate_relevance_score(SAMPLE_RESUME_DATA, job_details_data)
                job_scores.append((job_summary, job_details_data, score))
                print(f"✅ Job {i} processed successfully")
            else:
                print(f"❌ Failed to get details for job {i}")
        
        # Sort by score and display
        job_scores.sort(key=lambda x: x[2], reverse=True)
        
        print(f"\n🏆 Results (Sorted by Relevance):")
        print("=" * 60)
        
        for i, (job_summary, job_details, score) in enumerate(job_scores, 1):
            print(f"\n🥇 Rank {i}:")
            display_job_comparison(job_summary, job_details, score)
        
        # Summary
        if job_scores:
            scores = [score for _, _, score in job_scores]
            print(f"📈 Summary:")
            print(f"   Jobs Processed: {len(job_scores)}")
            print(f"   Average Score: {sum(scores)/len(scores):.2f}%")
            print(f"   Highest Score: {max(scores):.2f}%")
            print(f"   Jobs >70%: {sum(1 for s in scores if s >= 70)}")
            print(f"   Jobs >50%: {sum(1 for s in scores if s >= 50)}")
        
        print("\n🎉 Test completed successfully!")
        
    else:
        print("❌ No jobs found or API error occurred")


if __name__ == "__main__":
    main()
