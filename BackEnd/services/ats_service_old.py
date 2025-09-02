"""
ATS (Applicant Tracking System) Score Service

This service calculates ATS scores using Google Gemini API to provide
accurate assessment of resume compatibility with ATS systems.
"""

import re
import json
import os
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
    print("WARNING: GOOGLE_API_KEY not found. ATS scoring will use fallback method.")


class ATSScoreCalculator:
    """Calculate ATS scores using Google Gemini API for accurate assessment."""
    
    def __init__(self):
        self.api_key = api_key

    async def calculate_ats_score(self, resume_text: str, resume_parsed: Optional[Dict] = None, 
                           job_requirements: Optional[str] = None) -> float:
        """
        Calculate ATS score using Google Gemini API for accurate assessment.
        
        Args:
            resume_text: Raw text from resume
            resume_parsed: Parsed resume data (optional)
            job_requirements: Job requirements text (optional)
            
        Returns:
            ATS score between 0.0 and 1.0
        """
        if not self.api_key:
            print("WARNING: No Google API key found, using fallback scoring")
            return await self._fallback_ats_score(resume_text, job_requirements)
        
        if not resume_text or not resume_text.strip():
            return 0.0
        
        try:
            # Configure the Gemini model
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            # Create comprehensive ATS assessment prompt
            prompt = f"""
            You are an expert ATS (Applicant Tracking System) evaluator. Analyze the following resume and provide an ATS compatibility score.

            Your task is to evaluate how well this resume would perform in ATS systems based on these criteria:

            1. **Format & Structure (25%)**: 
               - Standard section headers (Experience, Education, Skills, etc.)
               - Clean, simple formatting without complex layouts
               - Proper use of bullet points
               - Contact information clearly visible

            2. **Keyword Optimization (30%)**:
               - Presence of relevant industry keywords
               - Technical skills and tools mentioned
               - Job-relevant terminology
               - Skills mentioned multiple times appropriately

            3. **Content Quality (25%)**:
               - Complete sections (no major gaps)
               - Quantified achievements and results  
               - Clear job titles and company names
               - Relevant experience descriptions

            4. **ATS Technical Compatibility (20%)**:
               - Readable text format
               - Standard file format compatibility
               - No complex graphics or tables that ATS can't parse
               - Proper date formats and clear chronology

            {f"**Job Requirements Context**: {job_requirements}" if job_requirements else ""}

            **Resume Content:**
            ---
            {resume_text}
            ---

            **Instructions:**
            - Evaluate the resume against each criterion
            - Provide a final ATS compatibility score as a decimal between 0.0 and 1.0
            - 0.0 = Very poor ATS compatibility (likely to be filtered out)
            - 0.3 = Poor compatibility (significant issues)
            - 0.5 = Fair compatibility (some issues to address) 
            - 0.7 = Good compatibility (minor improvements needed)
            - 0.9-1.0 = Excellent ATS compatibility

            Return ONLY a JSON object in this exact format:
            {{
                "ats_score": 0.XX,
                "format_score": 0.XX,
                "keyword_score": 0.XX, 
                "content_score": 0.XX,
                "technical_compatibility": 0.XX,
                "key_strengths": ["strength1", "strength2", "strength3"],
                "improvement_areas": ["area1", "area2", "area3"],
                "overall_assessment": "brief summary of ATS readiness"
            }}
            """
            
            # Make API call using ThreadPoolExecutor
            def sync_generate():
                response = model.generate_content(prompt)
                return response.text
            
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                response_text = await loop.run_in_executor(executor, sync_generate)
            
            # Parse the JSON response
            cleaned_response = response_text.strip().replace('```json', '').replace('```', '').strip()
            ats_result = json.loads(cleaned_response)
            
            # Extract and validate the ATS score
            ats_score = float(ats_result.get('ats_score', 0.0))
            ats_score = max(0.0, min(1.0, ats_score))  # Ensure score is between 0.0 and 1.0
            
            print(f"Gemini ATS Assessment: Score={ats_score}, Strengths={ats_result.get('key_strengths', [])}")
            return ats_score
            
        except json.JSONDecodeError as e:
            print(f"Error parsing Gemini ATS response: {e}")
            return await self._fallback_ats_score(resume_text, job_requirements)
        except Exception as e:
            print(f"Error calculating ATS score with Gemini: {e}")
            return await self._fallback_ats_score(resume_text, job_requirements)

    async def _fallback_ats_score(self, resume_text: str, job_requirements: Optional[str] = None) -> float:
        """Fallback ATS scoring when Gemini API is not available."""
        if not resume_text or len(resume_text.strip()) < 50:
            return 0.0
            
        score = 0.0
        text_lower = resume_text.lower()
        
        # Basic format check (0.3)
        basic_sections = ['experience', 'education', 'skills']
        section_count = sum(1 for section in basic_sections if section in text_lower)
        score += (section_count / len(basic_sections)) * 0.3
        
        # Contact info check (0.2)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, resume_text):
            score += 0.1
        
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,15}'
        if re.search(phone_pattern, resume_text):
            score += 0.1
        
        # Content length check (0.2)
        if len(resume_text) > 500:
            score += 0.2
        elif len(resume_text) > 200:
            score += 0.1
            
        # Basic keyword presence (0.3)
        common_keywords = ['experience', 'skills', 'work', 'education', 'project', 'team']
        keyword_count = sum(1 for keyword in common_keywords if keyword in text_lower)
        score += min(0.3, (keyword_count / len(common_keywords)) * 0.3)
        
        return min(1.0, score)

    def _calculate_format_score(self, resume_text: str) -> float:
        """Calculate score based on ATS-friendly formatting."""
        score = 0.0
        
        # Check for proper section headers (0.3)
        text_lower = resume_text.lower()
        header_matches = sum(1 for header in self.section_headers if header in text_lower)
        score += min(0.3, header_matches / len(self.section_headers) * 0.3)
        
        # Check for bullet points (0.2)
        bullet_patterns = ['•', '·', '-', '*']
        has_bullets = any(bullet in resume_text for bullet in bullet_patterns)
        if has_bullets:
            score += 0.2
        
        # Check for email and phone (0.2)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,15}'
        
        if re.search(email_pattern, resume_text):
            score += 0.1
        if re.search(phone_pattern, resume_text):
            score += 0.1
        
        # Check for dates (0.2)
        date_patterns = [r'\d{4}', r'\d{1,2}/\d{4}', r'\d{1,2}/\d{1,2}/\d{4}']
        has_dates = any(re.search(pattern, resume_text) for pattern in date_patterns)
        if has_dates:
            score += 0.2
        
        # Avoid complex formatting issues (0.1)
        if len(resume_text.strip()) > 100:  # Basic content check
            score += 0.1
        
        return score

    def _calculate_keyword_score(self, resume_text: str, job_requirements: Optional[str] = None) -> float:
        """Calculate score based on keyword matching."""
        resume_lower = resume_text.lower()
        score = 0.0
        
        # Technical keywords score (0.6)
        tech_matches = sum(1 for keyword in self.technical_keywords if keyword in resume_lower)
        tech_score = min(0.6, tech_matches / 20 * 0.6)  # Cap at 20 keywords for max score
        score += tech_score
        
        # Soft skills score (0.2)
        soft_matches = sum(1 for skill in self.soft_skills if skill in resume_lower)
        soft_score = min(0.2, soft_matches / 5 * 0.2)
        score += soft_score
        
        # Job-specific keywords (0.2)
        if job_requirements:
            job_keywords = self._extract_keywords_from_text(job_requirements.lower())
            job_matches = sum(1 for keyword in job_keywords if keyword in resume_lower)
            job_score = min(0.2, job_matches / max(1, len(job_keywords)) * 0.2)
            score += job_score
        else:
            score += 0.1  # Partial score if no job requirements
        
        return score

    def _calculate_content_score(self, resume_parsed: Dict) -> float:
        """Calculate score based on resume content quality."""
        score = 0.0
        
        # Check for experience section (0.4)
        experience = resume_parsed.get('experience', [])
        if experience and len(experience) > 0:
            score += 0.4
        
        # Check for education section (0.2)
        education = resume_parsed.get('education', [])
        if education and len(education) > 0:
            score += 0.2
        
        # Check for skills section (0.2)
        skills = resume_parsed.get('skills', [])
        if skills and len(skills) > 0:
            score += 0.2
        
        # Check for projects or achievements (0.2)
        projects = resume_parsed.get('projects', [])
        achievements = resume_parsed.get('achievements', [])
        if projects or achievements:
            score += 0.2
        
        return score

    def _calculate_skills_score(self, resume_text: str, job_requirements: Optional[str] = None) -> float:
        """Calculate score based on skills matching."""
        resume_lower = resume_text.lower()
        score = 0.0
        
        # Programming languages (0.5)
        prog_languages = ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby']
        prog_matches = sum(1 for lang in prog_languages if lang in resume_lower)
        score += min(0.5, prog_matches / 3 * 0.5)
        
        # Tools and technologies (0.3)
        tools = ['git', 'docker', 'aws', 'azure', 'jenkins', 'kubernetes']
        tool_matches = sum(1 for tool in tools if tool in resume_lower)
        score += min(0.3, tool_matches / 3 * 0.3)
        
        # Certifications and degrees (0.2)
        cert_keywords = ['certified', 'certification', 'degree', 'bachelor', 'master', 'phd']
        cert_matches = sum(1 for cert in cert_keywords if cert in resume_lower)
        score += min(0.2, cert_matches / 2 * 0.2)
        
        return score

    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract relevant keywords from job requirements text."""
        # Remove common stop words and extract meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return [word for word in words if word not in stop_words][:20]  # Limit to 20 keywords


async def calculate_and_update_ats_score(user_id: int, db: Session) -> Optional[float]:
    """
    Calculate ATS score for a user and update their profile.
    
    Args:
        user_id: User ID to calculate ATS score for
        db: Database session
        
    Returns:
        Calculated ATS score or None if calculation failed
    """
    try:
        # Get user profile
        profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == user_id
        ).first()
        
        if not profile:
            return None
        
        # Check if we have resume data
        if not profile.resume_text and not profile.resume_parsed:
            return None
        
        # Initialize calculator
        calculator = ATSScoreCalculator()
        
        # Calculate ATS score
        ats_score = calculator.calculate_ats_score(
            resume_text=profile.resume_text or "",
            resume_parsed=profile.resume_parsed,
            job_requirements=profile.job_requirements
        )
        
        # Update profile with new ATS score
        profile.ats_score = ats_score
        profile.ats_score_calculated_at = datetime.utcnow()
        profile.last_updated = datetime.utcnow()
        
        db.commit()
        db.refresh(profile)
        
        return ats_score
        
    except Exception as e:
        print(f"Error calculating ATS score for user {user_id}: {e}")
        db.rollback()
        return None


def get_or_calculate_ats_score(user_id: int, db: Session) -> Optional[float]:
    """
    Get existing ATS score or calculate new one if null.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        ATS score or None if calculation not possible
    """
    try:
        # Get user profile
        profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == user_id
        ).first()
        
        if not profile:
            return None
        
        # Return existing score if available and recent (within 24 hours)
        if (profile.ats_score is not None and 
            profile.ats_score_calculated_at and 
            (datetime.utcnow() - profile.ats_score_calculated_at).days < 1):
            return profile.ats_score
        
        # Calculate new score if null or outdated
        from asyncio import run
        return run(calculate_and_update_ats_score(user_id, db))
        
    except Exception as e:
        print(f"Error getting/calculating ATS score for user {user_id}: {e}")
        return None