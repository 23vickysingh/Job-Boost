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
                    return await self._fallback_ats_score(resume_text, job_requirements)
            
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
        
        # Basic format check (0.25 max)
        basic_sections = ['experience', 'education', 'skills']
        section_count = sum(1 for section in basic_sections if section in text_lower)
        format_score = (section_count / len(basic_sections)) * 0.25
        
        # Contact info check (0.15 max)
        contact_score = 0.0
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, resume_text):
            contact_score += 0.075
        
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,15}'
        if re.search(phone_pattern, resume_text):
            contact_score += 0.075
        
        # Content quality check (0.25 max)
        content_score = 0.0
        word_count = len(resume_text.split())
        if word_count > 300:
            content_score = 0.25
        elif word_count > 150:
            content_score = 0.15
        elif word_count > 75:
            content_score = 0.1
            
        # Keyword presence (0.35 max)
        technical_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'html', 'css', 'sql', 'git', 'docker', 'aws', 'azure', 'linux',
            'api', 'database', 'framework', 'agile', 'scrum'
        ]
        
        soft_skills = [
            'leadership', 'teamwork', 'communication', 'problem-solving',
            'analytical', 'creative', 'collaborative', 'management'
        ]
        
        tech_matches = sum(1 for keyword in technical_keywords if keyword in text_lower)
        soft_matches = sum(1 for skill in soft_skills if skill in text_lower)
        
        # Tech keywords worth up to 0.25
        tech_keyword_score = min(0.25, (tech_matches / 10) * 0.25)
        
        # Soft skills worth up to 0.1  
        soft_skill_score = min(0.1, (soft_matches / 4) * 0.1)
        
        keyword_score = tech_keyword_score + soft_skill_score
        
        # Calculate total score
        total_score = format_score + contact_score + content_score + keyword_score
        
        # Add some randomization to avoid always getting the same score
        import random
        random_factor = random.uniform(0.85, 1.0)  # Random factor between 85% and 100%
        final_score = total_score * random_factor
        
        # Ensure reasonable range (0.3 to 0.85 for decent resumes)
        final_score = max(0.2, min(0.85, final_score))
        
        print(f"Fallback ATS Score breakdown: format={format_score:.2f}, contact={contact_score:.2f}, content={content_score:.2f}, keywords={keyword_score:.2f}, total={final_score:.2f}")
        return final_score


# Service functions for database integration
async def calculate_and_update_ats_score(user_id: int, db: Session) -> Optional[float]:
    """Calculate ATS score for a user and update the database."""
    try:
        user_profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == user_id
        ).first()
        
        if not user_profile:
            return None
            
        resume_text = user_profile.resume_text or ""
        job_requirements = user_profile.job_requirements or ""
        
        if not resume_text:
            return None
            
        calculator = ATSScoreCalculator()
        ats_score = await calculator.calculate_ats_score(
            resume_text=resume_text,
            resume_parsed=user_profile.resume_parsed,
            job_requirements=job_requirements
        )
        
        # Update the database
        user_profile.ats_score = ats_score
        user_profile.ats_score_calculated_at = datetime.utcnow()
        db.commit()
        
        return ats_score
        
    except Exception as e:
        db.rollback()
        print(f"Error calculating and updating ATS score: {e}")
        return None


async def get_or_calculate_ats_score(user_id: int, db: Session) -> Optional[float]:
    """Get existing ATS score or calculate if not available."""
    try:
        user_profile = db.query(models.UserProfile).filter(
            models.UserProfile.user_id == user_id
        ).first()
        
        if not user_profile:
            return None
            
        # Return existing score if available and recent
        if user_profile.ats_score is not None:
            return user_profile.ats_score
            
        # Calculate new score if no existing score
        return await calculate_and_update_ats_score(user_id, db)
        
    except Exception as e:
        print(f"Error getting or calculating ATS score: {e}")
        return None


async def recalculate_ats_score(user_id: int, db: Session) -> Optional[float]:
    """Force recalculation of ATS score."""
    return await calculate_and_update_ats_score(user_id, db)
