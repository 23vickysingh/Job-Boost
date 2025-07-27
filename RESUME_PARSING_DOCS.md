# Resume Parsing Integration Documentation

## Overview

This documentation describes the AI-powered resume parsing system integrated into the Job-Boost application. The system automatically processes uploaded resumes in PDF, DOCX, and DOC formats using Google's Gemini AI API and extracts structured information to populate user profiles.

## Features

### 1. AI-Powered Resume Parsing
- **Google Gemini Integration**: Uses Google's Gemini 1.5 Flash model for accurate resume parsing
- **Multiple Format Support**: Handles PDF, DOCX, and DOC files
- **Structured Data Extraction**: Extracts personal info, experience, education, skills, projects, courses, achievements, and certifications
- **Fallback Parser**: Basic regex-based parser as backup when AI service is unavailable

### 2. Asynchronous Processing
- **Background Processing**: Resume parsing happens asynchronously without blocking user interactions
- **Queue System**: Uses asyncio queue for managing processing tasks
- **Non-blocking Upload**: Users can continue using the app while resumes are being processed
- **Status Tracking**: Real-time status updates for resume processing

### 3. Database Integration
- **Auto-population**: Automatically updates user profile with parsed information
- **JSON Storage**: Stores complete parsed data as JSON for future use
- **Database Mapping**: Maps AI-extracted data to existing database schema

## API Endpoints

### 1. Upload Resume Only
```
POST /profile/upload-resume
```
- **Purpose**: Upload and process resume independently
- **File Types**: PDF, DOCX, DOC
- **Response**: Processing status and filename
- **Async**: Yes, processing happens in background

### 2. Create/Update Profile with Resume
```
POST /profile/
```
- **Purpose**: Update profile manually with optional resume upload
- **Fields**: All profile fields + optional resume file
- **Async**: Yes, if resume is uploaded

### 3. Get Resume Processing Status
```
GET /profile/resume-status
```
- **Purpose**: Check current status of resume processing
- **Returns**: Status, filename, completion status

### 4. Get Profile
```
GET /profile/
```
- **Purpose**: Retrieve user profile with all parsed data
- **Includes**: All profile fields and resume data

### 5. Delete Resume
```
DELETE /profile/resume
```
- **Purpose**: Remove uploaded resume and parsed data

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the BackEnd directory:

```bash
# Google AI API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Database Configuration
DOCKER_DATABASE_URL=mysql+pymysql://user:password@db:3306/fastapi_db
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=fastapi_db
MYSQL_USER=user
MYSQL_PASSWORD=password

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (Brevo)
BREVO_API_KEY=your_brevo_api_key_here
```

### 2. Google API Key Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the key to your `.env` file as `GOOGLE_API_KEY`

### 3. Install Dependencies

The following packages are added to requirements.txt:
- `google-generativeai`: Google Gemini API client
- `python-dotenv`: Environment variable management
- `PyMuPDF`: Advanced PDF text extraction
- `python-docx`: Enhanced DOCX processing

## Data Structure

### Parsed Resume JSON Structure
```json
{
  "personal_info": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "linkedin": "string",
    "github": "string",
    "location": "string"
  },
  "summary": "string",
  "experience": [
    {
      "role": "string",
      "company": "string",
      "dates": "string",
      "location": "string",
      "description": ["string"]
    }
  ],
  "education": [
    {
      "degree": "string",
      "institution": "string",
      "dates": "string",
      "gpa": "string",
      "location": "string"
    }
  ],
  "skills": ["string"],
  "projects": [
    {
      "name": "string",
      "technologies": ["string"],
      "description": "string",
      "dates": "string",
      "link": "string"
    }
  ],
  "courses_undertaken": ["string"],
  "achievements": ["string"],
  "certifications": ["string"]
}
```

## Usage Examples

### Frontend Integration

```javascript
// Upload resume only
const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('resume', file);
  
  const response = await fetch('/profile/upload-resume', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  return response.json();
};

// Check processing status
const checkStatus = async () => {
  const response = await fetch('/profile/resume-status', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.json();
};

// Get updated profile
const getProfile = async () => {
  const response = await fetch('/profile/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.json();
};
```

### Processing Status Flow

1. **Upload**: User uploads resume → Status: "processing"
2. **Processing**: AI parses resume in background → Status: "processing"
3. **Complete**: Profile updated with parsed data → Status: "completed"
4. **Error**: If parsing fails → Status: "failed"

## Error Handling

### Graceful Degradation
- If Google API is unavailable, system falls back to basic regex parsing
- If parsing completely fails, original user data is preserved
- Detailed error messages for debugging

### Common Issues
1. **Invalid API Key**: Check GOOGLE_API_KEY in .env file
2. **Unsupported File Format**: Only PDF, DOCX, DOC are supported
3. **Large Files**: Files over 10MB may timeout
4. **Network Issues**: Background processing retries failed requests

## Performance Considerations

### Background Processing
- Resume parsing doesn't block user interactions
- Queue system handles multiple uploads efficiently
- Database updates are atomic and safe

### Resource Usage
- AI API calls are rate-limited
- Large files are processed in chunks
- Memory usage is optimized for concurrent uploads

## Security

### File Validation
- File type validation before processing
- File size limits to prevent abuse
- Virus scanning recommended for production

### Data Privacy
- Resume text is not stored permanently
- Only structured data is kept in database
- API keys are properly secured

## Monitoring and Logging

### Logging Points
- Resume upload events
- Processing start/completion
- API call success/failure
- Database update events

### Metrics to Track
- Processing time per resume
- Success/failure rates
- API usage and costs
- Queue length and processing backlog

## Future Enhancements

1. **Batch Processing**: Handle multiple resume uploads
2. **Custom Templates**: Support for different resume formats
3. **Skills Matching**: Match skills with job requirements
4. **Resume Scoring**: Quality assessment and improvement suggestions
5. **Multi-language Support**: Parse resumes in different languages
6. **Integration**: Connect with job boards and ATS systems
