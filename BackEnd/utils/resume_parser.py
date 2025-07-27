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
    model = genai.GenerativeModel('gemini-pro')
else:
    print("WARNING: GOOGLE_API_KEY not found. Resume parsing will use fallback method.")
    model = None


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


def extract_text_from_pdf_pymupdf(file_bytes: bytes) -> str:
    """Alternative PDF text extraction using PyMuPDF for better accuracy."""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"PyMuPDF extraction failed: {e}")
        return extract_text(BytesIO(file_bytes))


async def parse_resume_with_gemini(resume_text: str) -> Dict:
    """Parse resume using Google Gemini API."""
    if not api_key:
        return fallback_resume_parsing(resume_text)
    
    if not resume_text.strip():
        return {"error": "Empty resume text provided"}
    
    try:
        # Configure the Gemini model
        gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        You are an expert resume parser. Your task is to analyze the following resume text and extract the information into a structured JSON format.
        Please categorize the information under the following headings: 'personal_info', 'summary', 'experience', 'education', 'skills', 'projects', and 'courses_undertaken'.

        - For 'experience', 'education', and 'projects', create a list of objects.
        - For 'skills', create a list of strings.
        - If a section is not present in the resume, its value should be an empty list [] or null.
        - Return ONLY the JSON object, with no additional text or explanations.
        - For experience descriptions, extract key accomplishments and responsibilities as separate list items.
        - For skills, categorize them appropriately (technical skills, soft skills, tools, etc.).

        The desired JSON schema is as follows:
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

        Here is the resume text to parse:
        ---
        {resume_text}
        ---
        """
        
        # Run the API call in a thread to avoid blocking
        def generate_content():
            response = gemini_model.generate_content(prompt)
            return response.text
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            response_text = await loop.run_in_executor(executor, generate_content)
        
        # Clean and parse the JSON response
        cleaned_response = response_text.strip().replace('```json', '').replace('```', '').strip()
        
        parsed_json = json.loads(cleaned_response)
        return parsed_json
        
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to decode JSON from the API response.",
            "details": str(e),
            "raw_response": response_text[:500] + "..." if len(response_text) > 500 else response_text
        }
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


def parse_resume_details(text: str) -> Dict[str, str]:
    """Fallback parser that extracts common resume sections using regex patterns."""
    details = {
        "skills": "",
        "projects": "",
        "experiences_detail": "",
        "achievements": "",
        "education": "",
        "courses": ""
    }
    
    # Convert text to lowercase for pattern matching
    text_lower = text.lower()
    lines = text.splitlines()
    
    current_section = None
    section_patterns = {
        "skills": ["skill", "technical skill", "core competenc", "technologies"],
        "projects": ["project", "personal project", "academic project"],
        "experiences_detail": ["experience", "work experience", "professional experience", "employment"],
        "achievements": ["achievement", "accomplishment", "award", "honor", "recognition"],
        "education": ["education", "academic", "degree", "university", "college"],
        "courses": ["course", "certification", "training", "workshop"]
    }
    
    for line in lines:
        line_clean = line.strip()
        line_lower = line_clean.lower()
        
        if not line_clean:
            continue
            
        # Check if this line is a section header
        section_found = False
        for section, patterns in section_patterns.items():
            if any(pattern in line_lower for pattern in patterns):
                current_section = section
                section_found = True
                break
        
        # If it's not a section header and we have a current section, add content
        if not section_found and current_section and line_clean:
            # Skip common resume formatting patterns
            if not re.match(r'^\s*[-•▪▫◦‣⁃]\s*$', line_clean):
                details[current_section] += line_clean + "\n"
    
    return {k: v.strip() for k, v in details.items()}


async def process_resume_upload(file_bytes: bytes, filename: str, use_gemini: bool = True) -> Dict:
    """
    Process uploaded resume file and extract structured data.
    
    Args:
        file_bytes: The uploaded file content as bytes
        filename: Original filename
        use_gemini: Whether to use Gemini API for parsing (default: True)
    
    Returns:
        Dictionary containing parsed resume data
    """
    try:
        # Extract text from file
        if filename.lower().endswith('.pdf'):
            # Try PyMuPDF first, fallback to pdfminer
            resume_text = extract_text_from_pdf_pymupdf(file_bytes)
            if not resume_text.strip():
                resume_text = extract_text_from_upload(file_bytes, filename)
        else:
            resume_text = extract_text_from_upload(file_bytes, filename)
        
        if not resume_text.strip():
            return {"error": "Could not extract text from the uploaded file"}
        
        # Parse using Gemini API if available and requested
        if use_gemini and api_key:
            parsed_data = await parse_resume_with_gemini(resume_text)
            if "error" not in parsed_data:
                return {
                    "success": True,
                    "method": "gemini",
                    "data": parsed_data,
                    "raw_text": resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text
                }
            else:
                # Fallback to basic parsing if Gemini fails
                print(f"Gemini parsing failed: {parsed_data.get('error')}")
        
        # Fallback to basic regex parsing
        basic_parsed = parse_resume_details(resume_text)
        return {
            "success": True,
            "method": "basic",
            "data": basic_parsed,
            "raw_text": resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text
        }
        
    except Exception as e:
        return {"error": f"Failed to process resume: {str(e)}"}


def format_parsed_data_for_database(parsed_data: Dict) -> Dict[str, str]:
    """
    Convert parsed resume data to format suitable for database storage.
    
    Args:
        parsed_data: Parsed resume data from Gemini or basic parser
    
    Returns:
        Dictionary with keys matching database columns
    """
    if parsed_data.get("method") == "gemini" and "data" in parsed_data:
        data = parsed_data["data"]
        
        # Format experience
        experience_text = ""
        if data.get("experience"):
            for exp in data["experience"]:
                experience_text += f"{exp.get('role', '')} at {exp.get('company', '')}\n"
                experience_text += f"Duration: {exp.get('dates', '')}\n"
                if exp.get('location'):
                    experience_text += f"Location: {exp['location']}\n"
                if exp.get('description'):
                    for desc in exp['description']:
                        experience_text += f"• {desc}\n"
                experience_text += "\n"
        
        # Format education
        education_text = ""
        if data.get("education"):
            for edu in data["education"]:
                education_text += f"{edu.get('degree', '')} from {edu.get('institution', '')}\n"
                if edu.get('dates'):
                    education_text += f"Duration: {edu['dates']}\n"
                if edu.get('gpa'):
                    education_text += f"GPA: {edu['gpa']}\n"
                if edu.get('location'):
                    education_text += f"Location: {edu['location']}\n"
                education_text += "\n"
        
        # Format projects
        projects_text = ""
        if data.get("projects"):
            for proj in data["projects"]:
                projects_text += f"Project: {proj.get('name', '')}\n"
                if proj.get('technologies'):
                    projects_text += f"Technologies: {', '.join(proj['technologies'])}\n"
                if proj.get('description'):
                    projects_text += f"Description: {proj['description']}\n"
                if proj.get('dates'):
                    projects_text += f"Duration: {proj['dates']}\n"
                if proj.get('link'):
                    projects_text += f"Link: {proj['link']}\n"
                projects_text += "\n"
        
        # Format skills
        skills_text = ", ".join(data.get("skills", []))
        
        # Format courses
        courses_text = "\n".join(data.get("courses_undertaken", []))
        
        # Format achievements
        achievements_text = "\n".join(data.get("achievements", []))
        
        return {
            "experiences": experience_text.strip(),
            "skills": skills_text.strip(),
            "projects": projects_text.strip(),
            "education": education_text.strip(),
            "courses": courses_text.strip(),
            "achievements": achievements_text.strip(),
            "resume_data": json.dumps(data, indent=2)  # Store full JSON for future use
        }
    
    else:
        # Handle basic parser format
        data = parsed_data.get("data", {})
        return {
            "experiences": data.get("experiences_detail", ""),
            "skills": data.get("skills", ""),
            "projects": data.get("projects", ""),
            "education": data.get("education", ""),
            "courses": data.get("courses", ""),
            "achievements": data.get("achievements", ""),
            "resume_data": json.dumps(data, indent=2)
        }
