import requests
import json
import re
import os
from collections import Counter
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas
from database import SessionLocal


class JobMatchingService:
    """Service for fetching jobs from JSearch API and matching them with user resumes."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://jsearch.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        self.max_jobs_for_storage = 10  # Store 10 jobs in database
        self.max_jobs_for_matching = 3  # Only match first 3 for relevance scoring
    
    def search_jobs(self, query: str, location: str = "USA", employment_type: str = None) -> Optional[Dict]:
        """
        Fetch jobs from JSearch API using search parameters.
        
        Args:
            query: Job title/query (e.g., "Software Engineer")
            location: Job location (e.g., "USA", "New York")
            employment_type: Employment type filter (optional)
        
        Returns:
            Dictionary containing job search results or None if failed
        """
        url = f"{self.base_url}/search"
        
        # Build search parameters
        params = {
            "query": f"{query} in {location}",
            "page": "1",
            "num_pages": "1"
        }
        
        if employment_type:
            params["employment_types"] = employment_type
        
        try:
            print(f"🔍 Searching for jobs: {params['query']}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Found {len(data.get('data', []))} jobs from search")
            return data
            
        except requests.exceptions.HTTPError as http_err:
            print(f"❌ HTTP error during job search: {http_err}")
            print(f"Response content: {response.text}")
        except requests.exceptions.RequestException as err:
            print(f"❌ Request error during job search: {err}")
        except Exception as e:
            print(f"❌ Unexpected error during job search: {e}")
        
        return None
    
    def get_job_details(self, job_id: str) -> Optional[Dict]:
        """
        Fetch detailed information for a specific job using its job_id.
        
        Args:
            job_id: The unique job identifier from JSearch
        
        Returns:
            Dictionary containing detailed job information or None if failed
        """
        url = f"{self.base_url}/job-details"
        params = {"job_id": job_id}
        
        try:
            print(f"📄 Fetching details for job_id: {job_id}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Successfully fetched job details for {job_id}")
            return data
            
        except requests.exceptions.HTTPError as http_err:
            print(f"❌ HTTP error fetching job details for {job_id}: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"❌ Request error fetching job details for {job_id}: {err}")
        except Exception as e:
            print(f"❌ Unexpected error fetching job details for {job_id}: {e}")
        
        return None
    
    def calculate_relevance_score(self, resume_data: Dict, job_details: Dict) -> float:
        """
        Calculate relevance score between resume and job description.
        Based on the algorithm from two.py with improvements.
        
        Args:
            resume_data: Parsed resume data
            job_details: Detailed job information from JSearch API
        
        Returns:
            Relevance score between 0-100
        """
        try:
            # Extract resume skills and keywords
            parsed_data = resume_data.get("parsed_data", {})
            resume_skills = set(skill.lower() for skill in parsed_data.get("skills", []))
            
            # Extract keywords from resume projects and courses
            resume_keywords = set()
            
            # Add project keywords
            for project in parsed_data.get("projects", []):
                if project.get("name"):
                    resume_keywords.update(word.lower() for word in re.findall(r'\w+', project["name"]))
                if project.get("description"):
                    resume_keywords.update(word.lower() for word in re.findall(r'\w+', project["description"]))
                for tech in project.get("technologies", []):
                    resume_keywords.update(word.lower() for word in re.findall(r'\w+', tech))
            
            # Add course keywords
            for course in parsed_data.get("courses_undertaken", []):
                resume_keywords.update(word.lower() for word in re.findall(r'\w+', course))
            
            # Add experience keywords
            for exp in parsed_data.get("experience", []):
                if exp.get("role"):
                    resume_keywords.update(word.lower() for word in re.findall(r'\w+', exp["role"]))
                for desc in exp.get("description", []):
                    resume_keywords.update(word.lower() for word in re.findall(r'\w+', desc))
            
            # Extract job data
            if not job_details or 'data' not in job_details or not job_details['data']:
                print("⚠️ No job data available for scoring")
                return 0
            
            job_data = job_details['data'][0]
            job_description_text = job_data.get('job_description', '').lower()
            
            # Extract job skills and keywords
            job_skills = set()
            job_keywords = set()
            
            # Extract from job highlights if available
            job_highlights = job_data.get('job_highlights', {})
            if job_highlights:
                # Extract from qualifications
                for qualification in job_highlights.get('Qualifications', []):
                    job_skills.update(word.lower() for word in re.findall(r'\w+', qualification))
                    job_keywords.update(word.lower() for word in re.findall(r'\w+', qualification))
                
                # Extract from responsibilities
                for responsibility in job_highlights.get('Responsibilities', []):
                    job_keywords.update(word.lower() for word in re.findall(r'\w+', responsibility))
            
            # Extract from job title and description
            job_title = job_data.get('job_title', '').lower()
            job_keywords.update(word.lower() for word in re.findall(r'\w+', job_title))
            job_keywords.update(word.lower() for word in re.findall(r'\w+', job_description_text))
            
            # If no specific skills found, use all job keywords as potential skills
            if not job_skills:
                job_skills = job_keywords.copy()
            
            # Calculate scores
            # 1. Skills Score (Weight: 70%)
            matching_skills = resume_skills.intersection(job_skills)
            skill_score = (len(matching_skills) / len(resume_skills)) * 100 if resume_skills else 0
            
            # 2. Keyword Score (Weight: 30%)
            matching_keywords = resume_keywords.intersection(job_keywords)
            keyword_score = (len(matching_keywords) / len(resume_keywords)) * 100 if resume_keywords else 0
            
            # Weighted average for final relevance score
            relevance_score = (0.7 * skill_score) + (0.3 * keyword_score)
            
            # Cap score at 100 and ensure minimum is 0
            final_score = max(0, min(relevance_score, 100))
            
            print(f"📊 Relevance Score Calculation:")
            print(f"   Skills Match: {len(matching_skills)}/{len(resume_skills)} = {skill_score:.2f}%")
            print(f"   Keywords Match: {len(matching_keywords)}/{len(resume_keywords)} = {keyword_score:.2f}%")
            print(f"   Final Score: {final_score:.2f}%")
            
            return final_score
            
        except Exception as e:
            print(f"❌ Error calculating relevance score: {e}")
            return 0
    
    def save_job_to_database(self, job_summary: Dict, job_details: Dict, db: Session) -> Optional[models.Job]:
        """
        Save job information to database.
        
        Args:
            job_summary: Basic job information from search
            job_details: Detailed job information
            db: Database session
        
        Returns:
            Saved Job model instance or None if failed
        """
        try:
            job_data = job_details['data'][0] if job_details.get('data') else {}
            
            # Check if job already exists
            existing_job = db.query(models.Job).filter(
                models.Job.job_id == job_summary.get('job_id')
            ).first()
            
            if existing_job:
                print(f"💾 Job {job_summary.get('job_id')} already exists in database")
                return existing_job
            
            # Create new job record
            new_job = models.Job(
                job_id=job_summary.get('job_id'),
                title=job_summary.get('job_title', ''),
                company=job_summary.get('employer_name', ''),
                location=f"{job_summary.get('job_city', '')}, {job_summary.get('job_state', '')}, {job_summary.get('job_country', '')}".strip(', '),
                description=job_data.get('job_description', ''),
                apply_link=job_summary.get('job_apply_link', ''),
                
                # Additional fields from JSearch API
                job_employment_type=job_summary.get('job_employment_type'),
                job_city=job_summary.get('job_city'),
                job_state=job_summary.get('job_state'),
                job_country=job_summary.get('job_country'),
                job_latitude=job_summary.get('job_latitude'),
                job_longitude=job_summary.get('job_longitude'),
                job_benefits=job_summary.get('job_benefits'),
                job_google_link=job_summary.get('job_google_link'),
                job_offer_expiration_datetime_utc=job_summary.get('job_offer_expiration_datetime_utc'),
                job_required_experience=job_summary.get('job_required_experience'),
                job_required_skills=job_summary.get('job_required_skills'),
                job_required_education=job_summary.get('job_required_education'),
                job_experience_in_place_of_education=job_summary.get('job_experience_in_place_of_education'),
                job_min_salary=job_summary.get('job_min_salary'),
                job_max_salary=job_summary.get('job_max_salary'),
                job_salary_currency=job_summary.get('job_salary_currency'),
                job_salary_period=job_summary.get('job_salary_period'),
                job_highlights=job_data.get('job_highlights'),
                job_job_title=job_data.get('job_title'),
                job_posting_language=job_summary.get('job_posting_language'),
                job_onet_soc=job_summary.get('job_onet_soc'),
                job_onet_job_zone=job_summary.get('job_onet_job_zone'),
                job_naics_code=job_summary.get('job_naics_code'),
                job_naics_name=job_summary.get('job_naics_name'),
                employer_logo=job_summary.get('employer_logo'),
                employer_website=job_summary.get('employer_website'),
                employer_company_type=job_summary.get('employer_company_type'),
                employer_reviews_count=job_summary.get('employer_reviews_count'),
                employer_rating=job_summary.get('employer_rating')
            )
            
            db.add(new_job)
            db.commit()
            db.refresh(new_job)
            
            print(f"💾 Successfully saved job {new_job.job_id} to database")
            return new_job
            
        except Exception as e:
            print(f"❌ Error saving job to database: {e}")
            db.rollback()
            return None
    
    def save_job_match(self, user_id: int, job: models.Job, relevance_score: float, db: Session) -> Optional[models.JobMatch]:
        """
        Save job match result to database.
        
        Args:
            user_id: User ID
            job: Job model instance
            relevance_score: Calculated relevance score
            db: Database session
        
        Returns:
            Saved JobMatch model instance or None if failed
        """
        try:
            # Check if match already exists
            existing_match = db.query(models.JobMatch).filter(
                models.JobMatch.user_id == user_id,
                models.JobMatch.job_id == job.id
            ).first()
            
            if existing_match:
                # Update existing match with new score
                existing_match.relevance_score = relevance_score
                db.commit()
                print(f"🔄 Updated existing job match for user {user_id} and job {job.job_id}")
                return existing_match
            
            # Create new job match
            new_match = models.JobMatch(
                user_id=user_id,
                job_id=job.id,
                relevance_score=relevance_score
            )
            
            db.add(new_match)
            db.commit()
            db.refresh(new_match)
            
            print(f"💾 Saved job match: User {user_id} <-> Job {job.job_id} (Score: {relevance_score:.2f}%)")
            return new_match
            
        except Exception as e:
            print(f"❌ Error saving job match: {e}")
            db.rollback()
            return None
    
    def process_job_matching_for_user(self, user_id: int, db: Session) -> Dict:
        """
        Complete job matching workflow for a user.
        
        Process:
        1. Fetch 10 jobs and store all in database
        2. Calculate relevance for first 3 jobs only
        3. Store job matches for those 3 jobs
        
        Args:
            user_id: User ID to process job matching for
            db: Database session
        
        Returns:
            Dictionary with processing results
        """
        print(f"\n🚀 STARTING JOB MATCHING PROCESS FOR USER {user_id}")
        print("=" * 70)
        
        try:
            # Get user profile
            profile = db.query(models.UserProfile).filter(
                models.UserProfile.user_id == user_id
            ).first()
            
            if not profile:
                print("❌ User profile not found")
                return {
                    "success": False,
                    "message": "User profile not found",
                    "jobs_processed": 0,
                    "jobs_stored": 0,
                    "matches_created": 0
                }
            
            # Check if user has resume parsed data
            if not profile.resume_parsed or not profile.resume_parsed.get("parsed_data"):
                print("❌ No parsed resume data found")
                return {
                    "success": False,
                    "message": "No parsed resume data found. Please upload and parse resume first.",
                    "jobs_processed": 0,
                    "jobs_stored": 0,
                    "matches_created": 0
                }
            
            # Check if user has job preferences
            if not profile.query or not profile.location:
                print("❌ Job preferences incomplete")
                return {
                    "success": False,
                    "message": "Job preferences not set. Please set job title and location preferences.",
                    "jobs_processed": 0,
                    "jobs_stored": 0,
                    "matches_created": 0
                }
            
            print(f"📋 User Profile Information:")
            print(f"   User ID: {user_id}")
            print(f"   Query: {profile.query}")
            print(f"   Location: {profile.location}")
            print(f"   Work Experience: {profile.work_experience}")
            print(f"   Employment Types: {profile.employment_types}")
            
            # Extract user skills for logging
            user_skills = profile.resume_parsed.get("parsed_data", {}).get("skills", [])
            print(f"   Resume Skills Count: {len(user_skills)}")
            print(f"   Resume Skills: {', '.join(user_skills[:10])}...")
            
            print(f"\n🔍 STEP 1: SEARCHING FOR JOBS")
            print("-" * 40)
            
            # Search for jobs based on user preferences
            employment_type = None
            if profile.employment_types and len(profile.employment_types) > 0:
                employment_type = profile.employment_types[0]  # Use first preference
            
            search_query = f"{profile.query} in {profile.location}"
            print(f"🔍 Search Query: {search_query}")
            print(f"🔍 Employment Type Filter: {employment_type or 'None'}")
            
            job_search_results = self.search_jobs(
                query=profile.query,
                location=profile.location,
                employment_type=employment_type
            )
            
            if not job_search_results or not job_search_results.get('data'):
                print("❌ No jobs found from JSearch API")
                return {
                    "success": False,
                    "message": "No jobs found for the given preferences",
                    "jobs_processed": 0,
                    "jobs_stored": 0,
                    "matches_created": 0
                }
            
            all_jobs = job_search_results['data']
            print(f"✅ JSearch API returned {len(all_jobs)} jobs")
            
            # Take first 10 jobs for storage
            jobs_to_store = all_jobs[:self.max_jobs_for_storage]
            # Take first 3 jobs for matching
            jobs_to_match = all_jobs[:self.max_jobs_for_matching]
            
            print(f"� Jobs to store in database: {len(jobs_to_store)}")
            print(f"📊 Jobs to calculate relevance: {len(jobs_to_match)}")
            
            print(f"\n💾 STEP 2: STORING JOBS IN DATABASE")
            print("-" * 40)
            
            jobs_stored = 0
            stored_job_objects = []
            
            # Store all 10 jobs in database
            for i, job_summary in enumerate(jobs_to_store, 1):
                job_id = job_summary.get('job_id')
                if not job_id:
                    print(f"⚠️ Job {i}: Missing job_id, skipping")
                    continue
                
                job_title = job_summary.get('job_title', 'Unknown')
                company = job_summary.get('employer_name', 'Unknown')
                print(f"💾 Storing Job {i}: {job_title} at {company}")
                
                # Get detailed job information for storage
                job_details = self.get_job_details(job_id)
                if not job_details:
                    print(f"   ⚠️ Could not fetch details for job {job_id}, storing basic info only")
                    # Create minimal job details for storage
                    job_details = {"data": [job_summary]}
                
                # Save job to database
                saved_job = self.save_job_to_database(job_summary, job_details, db)
                if saved_job:
                    jobs_stored += 1
                    stored_job_objects.append(saved_job)
                    print(f"   ✅ Job {i} stored successfully (DB ID: {saved_job.id})")
                else:
                    print(f"   ❌ Failed to store job {i}")
            
            print(f"\n✅ STORED {jobs_stored} JOBS IN DATABASE")
            
            print(f"\n🎯 STEP 3: CALCULATING RELEVANCE SCORES")
            print("-" * 40)
            
            matches_created = 0
            
            # Calculate relevance only for first 3 jobs
            for i, job_summary in enumerate(jobs_to_match, 1):
                job_id = job_summary.get('job_id')
                if not job_id:
                    print(f"⚠️ Match Job {i}: Missing job_id, skipping")
                    continue
                
                job_title = job_summary.get('job_title', 'Unknown')
                company = job_summary.get('employer_name', 'Unknown')
                print(f"\n🎯 Calculating Relevance for Job {i}: {job_title} at {company}")
                
                # Get detailed job information for relevance calculation
                job_details = self.get_job_details(job_id)
                if not job_details:
                    print(f"   ❌ Could not fetch details for relevance calculation, skipping")
                    continue
                
                # Calculate relevance score
                print(f"   📊 Calculating relevance score...")
                relevance_score = self.calculate_relevance_score(
                    profile.resume_parsed,
                    job_details
                )
                
                print(f"   🎯 Relevance Score: {relevance_score:.2f}%")
                
                # Find the stored job object
                stored_job = None
                for job_obj in stored_job_objects:
                    if job_obj.job_id == job_id:
                        stored_job = job_obj
                        break
                
                if not stored_job:
                    print(f"   ⚠️ Could not find stored job object for {job_id}")
                    continue
                
                # Save job match
                job_match = self.save_job_match(user_id, stored_job, relevance_score, db)
                if job_match:
                    matches_created += 1
                    print(f"   ✅ Job match created (Match ID: {job_match.id})")
                else:
                    print(f"   ❌ Failed to create job match")
            
            print(f"\n🎉 JOB MATCHING COMPLETED!")
            print("=" * 70)
            print(f"📊 FINAL RESULTS:")
            print(f"   Jobs Found from API: {len(all_jobs)}")
            print(f"   Jobs Stored in Database: {jobs_stored}")
            print(f"   Jobs Processed for Relevance: {len(jobs_to_match)}")
            print(f"   Job Matches Created: {matches_created}")
            
            # Update last job search timestamp
            try:
                profile.last_job_search = datetime.utcnow()
                db.commit()
                print(f"   ✅ Updated last_job_search timestamp for user {user_id}")
            except Exception as e:
                print(f"   ⚠️ Failed to update last_job_search timestamp: {e}")
            
            return {
                "success": True,
                "message": f"Successfully stored {jobs_stored} jobs and created {matches_created} matches",
                "jobs_processed": len(jobs_to_match),
                "jobs_stored": jobs_stored,
                "matches_created": matches_created,
                "user_id": user_id
            }
            
        except Exception as e:
            print(f"❌ Error in job matching process: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "message": f"Error during job matching: {str(e)}",
                "jobs_processed": 0,
                "jobs_stored": 0,
                "matches_created": 0
            }


def get_job_matching_service() -> Optional[JobMatchingService]:
    """
    Get JobMatchingService instance with API key from environment.
    
    Returns:
        JobMatchingService instance or None if API key not found
    """
    api_key = os.getenv("JSEARCH_API_KEY")
    if not api_key:
        print("❌ JSEARCH_API_KEY environment variable not found")
        return None
    
    return JobMatchingService(api_key)
