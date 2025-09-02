"""
Job Relevance Matching Service

This service calculates semantic similarity between resume content and job descriptions
using Google Gemini API to provide accurate job-candidate relevance scores.
"""

import re
import json
import os
import random
import asyncio
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor

import google.generativeai as genai
from dotenv import load_dotenv

import models
from database import get_db

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: GOOGLE_API_KEY not found. Job relevance matching will use fallback method.")


class JobRelevanceCalculator:
    """Calculate job-resume relevance scores using Google Gemini API for semantic analysis."""
    
    def __init__(self):
        self.api_key = api_key

    async def calculate_relevance_score(self, resume_data: Dict, job_description: str, 
                                      job_title: str = "", job_requirements: str = "") -> float:
        """
        Calculate semantic similarity score between resume and job using Gemini API.
        
        Args:
            resume_data: Parsed resume data (from resume_parsed field)
            job_description: Job description text
            job_title: Job title (optional)
            job_requirements: Job requirements text (optional)
            
        Returns:
            Relevance score between 0.0 and 1.0
        """
        if not self.api_key:
            print("WARNING: No Google API key found, using fallback scoring")
            return await self._fallback_relevance_score(resume_data, job_description, job_title)
        
        if not resume_data or not job_description:
            return 0.0
        
        try:
            # Configure the Gemini model
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            # Extract resume information for comparison
            resume_summary = self._extract_resume_summary(resume_data)
            
            # Create comprehensive job matching prompt
            prompt = f"""
            You are an expert HR recruiter specializing in job-candidate matching. Your task is to analyze how well a candidate's resume matches a specific job opportunity and provide a detailed relevance score.

            **EVALUATION CRITERIA:**

            1. **Skills Match (35%)**:
               - Technical skills overlap
               - Required vs. actual skill proficiency
               - Technology stack alignment
               - Domain expertise relevance

            2. **Experience Relevance (30%)**:
               - Years of experience in similar roles
               - Industry experience alignment
               - Company size/type compatibility
               - Leadership/seniority level match

            3. **Educational Background (15%)**:
               - Degree relevance to job requirements
               - Educational institution quality
               - Certifications and specialized training
               - Continuous learning indicators

            4. **Role Compatibility (20%)**:
               - Job title/function alignment
               - Career progression logic
               - Responsibilities match
               - Work style/culture fit indicators

            **JOB OPPORTUNITY:**
            Job Title: {job_title}
            
            Job Description:
            {job_description}
            
            {f"Specific Requirements: {job_requirements}" if job_requirements else ""}

            **CANDIDATE RESUME SUMMARY:**
            {resume_summary}

            **INSTRUCTIONS:**
            - Evaluate each criterion carefully
            - Consider both direct matches and transferable skills
            - Account for career progression and growth potential
            - Provide a final relevance score as a decimal between 0.0 and 1.0
            - 0.0 = No match (completely unrelated)
            - 0.2 = Poor match (major gaps in requirements)
            - 0.4 = Fair match (some relevant experience but significant gaps)
            - 0.6 = Good match (meets most requirements with minor gaps)
            - 0.8 = Excellent match (meets all key requirements)
            - 1.0 = Perfect match (exceeds all requirements)

            Return ONLY a JSON object in this exact format:
            {{
                "relevance_score": 0.XX,
                "skills_match": 0.XX,
                "experience_relevance": 0.XX,
                "education_match": 0.XX,
                "role_compatibility": 0.XX,
                "key_matches": ["match1", "match2", "match3"],
                "missing_requirements": ["requirement1", "requirement2"],
                "transferable_skills": ["skill1", "skill2"],
                "overall_assessment": "Brief explanation of the match quality and hiring recommendation"
            }}
            """
            
            # Make API call using ThreadPoolExecutor with timeout
            def sync_generate():
                response = model.generate_content(prompt)
                return response.text
            
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                try:
                    # Add 30 second timeout for Gemini API call
                    response_text = await asyncio.wait_for(
                        loop.run_in_executor(executor, sync_generate),
                        timeout=30.0
                    )
                except asyncio.TimeoutError:
                    print("Gemini API call timed out, using fallback scoring")
                    return await self._fallback_relevance_score(resume_data, job_description, job_title)
            
            # Parse the JSON response
            cleaned_response = response_text.strip().replace('```json', '').replace('```', '').strip()
            relevance_result = json.loads(cleaned_response)
            
            # Extract and validate the relevance score
            relevance_score = float(relevance_result.get('relevance_score', 0.0))
            relevance_score = max(0.0, min(1.0, relevance_score))  # Ensure score is between 0.0 and 1.0
            
            print(f"Gemini Job Relevance: Score={relevance_score}, Matches={relevance_result.get('key_matches', [])}")
            print(f"Assessment: {relevance_result.get('overall_assessment', 'No assessment provided')}")
            
            return relevance_score
            
        except json.JSONDecodeError as e:
            print(f"Error parsing Gemini relevance response: {e}")
            return await self._fallback_relevance_score(resume_data, job_description, job_title)
        except Exception as e:
            print(f"Error calculating job relevance with Gemini: {e}")
            return await self._fallback_relevance_score(resume_data, job_description, job_title)

    def _extract_resume_summary(self, resume_data: Dict) -> str:
        """Extract key information from parsed resume data for matching."""
        if not resume_data:
            return "No resume data available"
        
        summary_parts = []
        
        # Personal info
        personal_info = resume_data.get('personal_info', {})
        if personal_info and isinstance(personal_info, dict):
            name = personal_info.get('name', 'Candidate')
            summary_parts.append(f"Candidate: {name}")
        
        # Summary
        if resume_data.get('summary'):
            summary_parts.append(f"Professional Summary: {resume_data['summary']}")
        
        # Experience
        experience = resume_data.get('experience', [])
        if experience and isinstance(experience, list):
            summary_parts.append("WORK EXPERIENCE:")
            for exp in experience[:3]:  # Top 3 experiences
                if isinstance(exp, dict):
                    role = exp.get('role', 'Unknown Role')
                    company = exp.get('company', 'Unknown Company')
                    dates = exp.get('dates', 'Unknown Duration')
                    description = exp.get('description', [])
                    desc_text = '; '.join(description[:2]) if isinstance(description, list) else str(description)[:200]
                    summary_parts.append(f"- {role} at {company} ({dates}): {desc_text}")
        
        # Education
        education = resume_data.get('education', [])
        if education and isinstance(education, list):
            summary_parts.append("EDUCATION:")
            for edu in education[:2]:  # Top 2 educations
                if isinstance(edu, dict):
                    degree = edu.get('degree', 'Degree')
                    institution = edu.get('institution', 'Institution')
                    summary_parts.append(f"- {degree} from {institution}")
        
        # Skills
        skills = resume_data.get('skills', [])
        if skills and isinstance(skills, list):
            skills_text = ', '.join(skills[:15])  # Top 15 skills
            summary_parts.append(f"KEY SKILLS: {skills_text}")
        
        # Projects
        projects = resume_data.get('projects', [])
        if projects and isinstance(projects, list):
            summary_parts.append("NOTABLE PROJECTS:")
            for proj in projects[:2]:  # Top 2 projects
                if isinstance(proj, dict):
                    name = proj.get('name', 'Project')
                    tech = proj.get('technologies', [])
                    tech_text = ', '.join(tech) if isinstance(tech, list) else str(tech)
                    summary_parts.append(f"- {name} (Technologies: {tech_text})")
        
        # Certifications
        certifications = resume_data.get('certifications', [])
        if certifications and isinstance(certifications, list):
            cert_text = ', '.join(certifications[:5])  # Top 5 certifications
            summary_parts.append(f"CERTIFICATIONS: {cert_text}")
        
        return '\n'.join(summary_parts)

    async def _fallback_relevance_score(self, resume_data: Dict, job_description: str, job_title: str = "") -> float:
        """Fallback relevance scoring when Gemini API is not available."""
        if not resume_data or not job_description:
            return 0.0
        
        score = 0.0
        job_lower = job_description.lower()
        job_title_lower = job_title.lower()
        
        # Skills matching (40% weight)
        skills = resume_data.get('skills', [])
        if skills and isinstance(skills, list):
            skill_matches = sum(1 for skill in skills if isinstance(skill, str) and skill.lower() in job_lower)
            skills_score = min(0.4, (skill_matches / max(1, len(skills))) * 0.6)
            score += skills_score
        
        # Experience matching (30% weight)
        experience = resume_data.get('experience', [])
        if experience and isinstance(experience, list):
            exp_score = 0.0
            for exp in experience:
                if isinstance(exp, dict):
                    role = exp.get('role', '').lower()
                    company = exp.get('company', '').lower()
                    description = exp.get('description', [])
                    
                    # Role title similarity
                    if role and any(word in job_title_lower for word in role.split() if len(word) > 2):
                        exp_score += 0.1
                    
                    # Description keyword matches
                    if isinstance(description, list):
                        desc_text = ' '.join(description).lower()
                        common_words = set(job_lower.split()) & set(desc_text.split())
                        exp_score += min(0.1, len(common_words) / 100)
            
            score += min(0.3, exp_score)
        
        # Education relevance (15% weight)
        education = resume_data.get('education', [])
        if education and isinstance(education, list):
            edu_score = 0.0
            for edu in education:
                if isinstance(edu, dict):
                    degree = edu.get('degree', '').lower()
                    # Basic education relevance check
                    if any(word in job_lower for word in degree.split() if len(word) > 3):
                        edu_score += 0.05
            score += min(0.15, edu_score)
        
        # General keyword matching (15% weight)
        resume_text = str(resume_data).lower()
        job_words = set(word for word in job_lower.split() if len(word) > 3)
        resume_words = set(word for word in resume_text.split() if len(word) > 3)
        common_words = job_words & resume_words
        
        keyword_score = min(0.15, len(common_words) / max(1, len(job_words)) * 0.15)
        score += keyword_score
        
        # Ensure reasonable range
        final_score = max(0.1, min(0.85, score))
        
        print(f"Fallback Relevance Score: {final_score:.2f} (Skills: {skills_score:.2f}, Experience: {min(0.3, exp_score):.2f}, Education: {min(0.15, edu_score):.2f}, Keywords: {keyword_score:.2f})")
        return final_score


# Service functions for database integration
async def calculate_job_relevance_for_new_match(job_match_id: int, db: Session) -> Optional[float]:
    """Calculate relevance score for a newly created job match."""
    try:
        # Get the job match record
        job_match = db.query(models.JobMatch).filter(
            models.JobMatch.id == job_match_id
        ).first()
        
        if not job_match:
            print(f"Job match {job_match_id} not found")
            return None
        
        # Only calculate if relevance_score is None (new match)
        if job_match.relevance_score is not None:
            print(f"Job match {job_match_id} already has relevance score: {job_match.relevance_score}")
            return job_match.relevance_score
        
        # Get user profile with resume data
        user_profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == job_match.user_id
        ).first()
        
        if not user_profile or not user_profile.resume_parsed:
            print(f"No resume data found for user {job_match.user_id}")
            return None
        
        # Get job information
        job_description = job_match.job_description or ""
        job_title = job_match.job_title or ""
        job_requirements = getattr(job_match, 'job_requirements', "") or ""
        
        if not job_description:
            print(f"No job description found for job match {job_match_id}")
            return None
        
        # Calculate relevance score
        calculator = JobRelevanceCalculator()
        relevance_score = await calculator.calculate_relevance_score(
            resume_data=user_profile.resume_parsed,
            job_description=job_description,
            job_title=job_title,
            job_requirements=job_requirements
        )
        
        # Update the database
        job_match.relevance_score = relevance_score
        db.commit()
        
        print(f"Calculated relevance score for new job match {job_match_id}: {relevance_score:.2f}")
        return relevance_score
        
    except Exception as e:
        db.rollback()
        print(f"Error calculating job relevance for match {job_match_id}: {e}")
        return None


async def calculate_relevance_on_job_creation(user_id: int, job_data: Dict, db: Session) -> Optional[float]:
    """
    Calculate relevance when a new job match is being created.
    This function can be called during job matching/creation process.
    
    Args:
        user_id: ID of the user
        job_data: Dictionary containing job information (title, description, requirements)
        db: Database session
    
    Returns:
        Calculated relevance score or None if calculation failed
    """
    try:
        # Get user profile with resume data
        user_profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == user_id
        ).first()
        
        if not user_profile or not user_profile.resume_parsed:
            print(f"No resume data found for user {user_id}")
            return None
        
        # Extract job information
        job_description = job_data.get('description', '')
        job_title = job_data.get('title', '')
        job_requirements = job_data.get('requirements', '')
        
        if not job_description:
            print("No job description provided")
            return None
        
        # Calculate relevance score
        calculator = JobRelevanceCalculator()
        relevance_score = await calculator.calculate_relevance_score(
            resume_data=user_profile.resume_parsed,
            job_description=job_description,
            job_title=job_title,
            job_requirements=job_requirements
        )
        
        print(f"Calculated relevance score for user {user_id} and job '{job_title}': {relevance_score:.2f}")
        return relevance_score
        
    except Exception as e:
        print(f"Error calculating relevance during job creation for user {user_id}: {e}")
        return None
