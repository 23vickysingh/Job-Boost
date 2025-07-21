import re
from io import BytesIO
from typing import Dict

from pdfminer.high_level import extract_text
import docx2txt


def extract_text_from_upload(file_bytes: bytes, filename: str) -> str:
    """Return plain text from an uploaded resume."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text(BytesIO(file_bytes))
    if lower.endswith(".docx"):
        # docx2txt expects a file path so we use an in-memory buffer
        return docx2txt.process(BytesIO(file_bytes))
    return file_bytes.decode("utf-8", errors="ignore")


def parse_resume_details(text: str) -> Dict[str, str]:
    """Very naive parser that extracts common resume sections."""
    details = {"skills": "", "projects": "", "experiences_detail": "", "achievements": ""}
    current = None
    for line in text.splitlines():
        l = line.strip().lower()
        if not l:
            continue
        if "skill" in l:
            current = "skills"
            continue
        if "project" in l:
            current = "projects"
            continue
        if "experience" in l:
            current = "experiences_detail"
            continue
        if "achievement" in l or "accomplishment" in l:
            current = "achievements"
            continue
        if current:
            details[current] += line.strip() + "\n"
    return {k: v.strip() for k, v in details.items()}
