# Job Matching System - Quick Start Guide

## Overview
The Job-Boost project has been enhanced with an intelligent job matching system that:
1. Fetches relevant jobs from JSearch API based on user preferences
2. Analyzes job descriptions against user resume data  
3. Calculates relevance scores using advanced algorithms
4. Stores results in the database for quick access

## Prerequisites
- User must have uploaded and parsed resume data
- User must have set job preferences (title, location, etc.)
- JSearch API key must be configured

## Setup Instructions

### 1. Get JSearch API Key
1. Sign up at [RapidAPI JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
2. Subscribe to a plan (free tier available)
3. Copy your API key

### 2. Configure Environment
Add to your `.env` file:
```bash
JSEARCH_API_KEY=your_actual_api_key_here
```

### 3. Database Migration
The new Job model includes many fields from JSearch API. Run database migration:
```bash
cd BackEnd
python -c "from database import engine; import models; models.Base.metadata.create_all(bind=engine)"
```

## How It Works

### User Workflow
1. **Upload Resume**: User uploads PDF/DOCX resume
2. **Resume Parsing**: AI extracts skills, experience, projects, education
3. **Set Preferences**: User sets job title, location, employment type, etc.
4. **Trigger Matching**: System fetches and matches jobs
5. **View Results**: User sees ranked job matches with relevance scores

### System Workflow
1. **Validate Prerequisites**: Check resume data and preferences exist
2. **Search Jobs**: Query JSearch API with user preferences
3. **Get Details**: Fetch detailed job descriptions (limited to 3 jobs)
4. **Calculate Scores**: Match resume against each job description
5. **Save Results**: Store jobs and match scores in database

## API Endpoints

### Trigger Job Matching
```http
POST /jobs/match
Content-Type: application/json
Authorization: Bearer <user_token>

{
  "user_id": null  // Optional, defaults to current user
}
```

Response:
```json
{
  "message": "Successfully processed 3 jobs and created 3 matches",
  "jobs_processed": 3,
  "matches_created": 3,
  "user_id": 1
}
```

### Get Job Matches
```http
GET /jobs/matches?limit=10&min_score=50.0
Authorization: Bearer <user_token>
```

Response:
```json
[
  {
    "id": 1,
    "relevance_score": 75.5,
    "job": {
      "id": 1,
      "job_id": "abc123",
      "title": "Software Engineer",
      "company": "Tech Corp",
      "location": "San Francisco, CA, USA",
      "description": "...",
      "apply_link": "https://...",
      "job_employment_type": "FULLTIME",
      "job_min_salary": 120000,
      "job_max_salary": 180000,
      "job_salary_currency": "USD",
      "job_salary_period": "YEAR",
      "created_at": "2025-01-01T00:00:00",
      "updated_at": "2025-01-01T00:00:00"
    }
  }
]
```

### Test API Connection
```http
POST /jobs/test-api
```

## Testing

### 1. Simple API Test (No Database)
```bash
cd BackEnd/scripts
python simple_api_test.py YOUR_API_KEY
```

This tests:
- JSearch API connectivity
- Job search functionality  
- Job details fetching
- Relevance score calculation
- Uses sample resume data from two.py

### 2. CLI Demo Tool
```bash
cd BackEnd/scripts
python job_matching_cli.py --api-key YOUR_API_KEY --query "Software Engineer" --location "USA"
```

Features:
- Interactive command-line interface
- Customizable search parameters
- Detailed scoring breakdown
- Results ranking and statistics

### 3. Complete System Test
```bash
cd BackEnd/scripts
python complete_test.py --api-key YOUR_API_KEY --user-email test@example.com
```

This tests the full workflow:
- Creates test user with profile and resume
- Triggers job matching process
- Displays results from database
- Optional cleanup of test data

## Frontend Integration

### Trigger Matching
```javascript
const triggerJobMatching = async () => {
  try {
    const response = await fetch('/jobs/match', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${userToken}`,
        'Content-Type': 'application/json'
      }
    });
    
    const result = await response.json();
    console.log(`Processed ${result.jobs_processed} jobs`);
  } catch (error) {
    console.error('Job matching failed:', error);
  }
};
```

### Get Matches
```javascript
const getJobMatches = async (limit = 10) => {
  try {
    const response = await fetch(`/jobs/matches?limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${userToken}`
      }
    });
    
    const matches = await response.json();
    return matches;
  } catch (error) {
    console.error('Failed to get matches:', error);
    return [];
  }
};
```

## Relevance Score Algorithm

The system uses a weighted algorithm:

**Skills Match (70%)**:
- Compares user's technical skills with job requirements
- Higher weight because skills are crucial for job fit

**Keyword Match (30%)**:
- Compares resume keywords (projects, courses, experience) with job description
- Provides contextual matching beyond just skills

**Formula**:
```
Relevance Score = (0.7 × Skills Match %) + (0.3 × Keyword Match %)
```

**Score Interpretation**:
- 🟢 70%+: Excellent match
- 🟡 50-69%: Good match  
- 🔴 <50%: Needs improvement

## Configuration

### Limits
- **Jobs per match**: 3 (configurable via MAX_JOBS_PER_MATCH)
- **API rate limits**: Depends on JSearch subscription
- **Minimum score**: 0.0 (configurable via MIN_RELEVANCE_SCORE)

### Required User Data
- **Resume parsed data**: Skills, experience, projects, education
- **Job preferences**: Query (job title), location, employment type

## Troubleshooting

### Common Issues

**1. "Job matching service not available"**
- Check JSEARCH_API_KEY in .env file
- Verify API key is valid on RapidAPI

**2. "No parsed resume data found"**
- User needs to upload resume first
- Resume parsing must complete successfully

**3. "Job preferences not set"**
- User must set job title and location
- Check user profile completeness

**4. "No jobs found"**
- Try broader search terms
- Check if location is too specific
- Verify API subscription limits

### Debug Mode
```bash
# Enable detailed logging
export DEBUG=True
```

### Check User Data
```sql
-- Check if user has resume data
SELECT user_id, resume_parsed IS NOT NULL as has_resume 
FROM user_profile WHERE user_id = 1;

-- Check job preferences
SELECT query, location, work_experience, employment_types 
FROM user_profile WHERE user_id = 1;

-- Check job matches
SELECT jm.relevance_score, j.title, j.company 
FROM job_matches jm 
JOIN jobs j ON jm.job_id = j.id 
WHERE jm.user_id = 1 
ORDER BY jm.relevance_score DESC;
```

## Next Steps

1. **Set up API key** in environment
2. **Test with scripts** to verify functionality
3. **Integrate with frontend** for user experience
4. **Monitor performance** and adjust limits as needed
5. **Gather user feedback** to improve matching algorithm

## Support

- Review logs for detailed error information
- Test with simple_api_test.py to isolate issues  
- Check JOB_MATCHING_README.md for comprehensive documentation
- Verify user data completeness before matching
