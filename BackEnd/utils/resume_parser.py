import re
import json
import os
from io import BytesIO
from typing import Dict, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

import google.generativeai as genai
from pdfminer.high_level import extract_text
import docx2txt
import fitz  # PyMuPDF
from docx import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: GOOGLE_API_KEY not found. Resume parsing will use fallback method.")


def fallback_resume_parsing(resume_text: str) -> Dict:
    """Basic fallback parsing when Gemini API is not available."""
    return {
        "personal_info": {
            "name": "Not extracted (API unavailable)",
            "email": extract_email(resume_text),
            "phone": extract_phone(resume_text),
            "linkedin": None,
            "github": None,
            "location": None
        },
        "summary": "Resume parsing requires Google API key",
        "experience": [],
        "education": [],
        "skills": [],
        "projects": [],
        "courses_undertaken": [],
        "achievements": [],
        "certifications": []
    }


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group() if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(phone_pattern, text)
    return match.group() if match else None


def extract_text_from_upload(file_bytes: bytes, filename: str) -> str:
    """Return plain text from an uploaded resume."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text(BytesIO(file_bytes))
    elif lower.endswith(".docx"):
        # Using python-docx for better text extraction
        try:
            doc = Document(BytesIO(file_bytes))
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        except:
            # Fallback to docx2txt
            return docx2txt.process(BytesIO(file_bytes))
    elif lower.endswith(".doc"):
        # Handle .doc files using docx2txt
        return docx2txt.process(BytesIO(file_bytes))
    else:
        return file_bytes.decode("utf-8", errors="ignore")


async def parse_resume_with_analysis(resume_text: str) -> Dict:
    """Enhanced resume parser with validation and analysis."""
    if not api_key:
        print("No API key found, using fallback parsing")
        return {"parsed_data": fallback_resume_parsing(resume_text), "analysis": None}
    
    if not resume_text.strip():
        return {"error": "Empty resume text provided"}
    
    try:
        print("Starting enhanced Gemini API resume parsing and validation...")
        
        # Configure the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # First check if the document is actually a resume
        prompt = f"""
        You are an expert document analyzer, resume parser and career advisor. Please analyze the following text and determine if it's a legitimate resume/CV document.
        
        Check for:
        1. Personal information (name, contact details)
        2. Professional experience or work history
        3. Educational background
        4. Skills section
        5. Overall structure typical of a resume
        
        If this is NOT a resume or contains irrelevant content (like random text, advertisements, etc.), respond with a json exactly having parsed_data : "resume unfit"
        
        If this IS a legitimate resume, 
        
        1. Parse the resume into structured JSON format
        2. Provide detailed analysis and feedback
        
        Please extract information into structured JSON with two main sections: 'parsed_data' and 'analysis'.
        
        The 'parsed_data' should follow this schema:
        {{
          "personal_info": {{
            "name": "string",
            "email": "string",
            "phone": "string",
            "linkedin": "string",
            "github": "string",
            "location": "string"
          }},
          "summary": "string",
          "experience": [
            {{
              "role": "string",
              "company": "string",
              "dates": "string",
              "location": "string",
              "description": ["string"]
            }}
          ],
          "education": [
            {{
              "degree": "string",
              "institution": "string",
              "dates": "string",
              "gpa": "string",
              "location": "string"
            }}
          ],
          "skills": ["string"],
          "projects": [
            {{
              "name": "string",
              "technologies": ["string"],
              "description": "string",
              "dates": "string",
              "link": "string"
            }}
          ],
          "courses_undertaken": ["string"],
          "achievements": ["string"],
          "certifications": ["string"]
        }}
        
        The 'analysis' should include:
        {{
          "good_points": ["List of strengths and positive aspects"],
          "weak_points": ["List of areas that need improvement"],
          "missing_things": ["List of important resume elements that are missing"],
          "redundancy": ["List of redundant or unnecessary content"],
          "improvements": ["List of specific suggestions for improvement"]
        }}
        
        Return ONLY the JSON object with both 'parsed_data' and 'analysis' sections, no additional text.
        
        Resume text to analyze:
        ---
        {resume_text}
        ---
        """
        
        def sync_parse():
            try:
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Gemini parsing call failed: {e}")
                raise
        
        # Run parsing in thread pool with timeout
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            try:
                response_text = await asyncio.wait_for(
                    loop.run_in_executor(executor, sync_parse),
                    timeout=90.0
                )
                print("Gemini API parsing completed successfully")
            except asyncio.TimeoutError:
                print("Gemini API call timed out, using fallback parsing")
                return {"parsed_data": fallback_resume_parsing(resume_text), "analysis": None}
        
        # Clean and parse the JSON response
        cleaned_response = response_text.strip().replace('```json', '').replace('```', '').strip()
        
        parsed_result = json.loads(cleaned_response)
        
        # Check if resume was deemed unfit
        if isinstance(parsed_result.get("parsed_data"), str) and "resume unfit" in parsed_result.get("parsed_data", "").lower():
            return {"error": "resume_unfit", "message": "Document is not a valid resume"}
        
        print("Resume parsing and analysis JSON decoded successfully")
        return parsed_result
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {
            "error": "Failed to decode JSON from the API response.",
            "details": str(e),
            "raw_response": response_text[:500] + "..." if len(response_text) > 500 else response_text
        }
    except Exception as e:
        print(f"Resume parsing error: {e}")
        return {"error": f"An unexpected error occurred: {str(e)}"}


def validate_file_constraints(file_content: bytes, filename: str) -> Dict[str, str]:
    """Validate file size and type constraints."""
    errors = []
    
    # Check file size (1 MB = 1,048,576 bytes)
    max_size = 1 * 1024 * 1024  # 1 MB
    if len(file_content) > max_size:
        errors.append(f"File size ({len(file_content) / 1024 / 1024:.2f} MB) exceeds maximum allowed size of 1 MB")
    
    # Check file extension
    allowed_extensions = ['.pdf', '.docx']
    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension not in allowed_extensions:
        errors.append(f"File type '{file_extension}' not allowed. Please upload PDF or DOCX files only")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }