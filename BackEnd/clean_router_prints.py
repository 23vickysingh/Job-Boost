#!/usr/bin/env python3
"""
Script to remove all print statements from production router files.
"""

import os
import re

def clean_print_statements_from_file(file_path):
    """Remove all print statements from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        # Skip lines that contain print statements
        if 'print(' not in line:
            cleaned_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print(f"Cleaned print statements from {file_path}")

if __name__ == "__main__":
    # Clean production files only
    files_to_clean = [
        "routers/jobs.py",
        "routers/profile.py",
        "services/job_scheduler.py"
    ]
    
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            clean_print_statements_from_file(file_path)
        else:
            print(f"File not found: {file_path}")
