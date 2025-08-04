# Job Matching System Documentation

## Overview

This job matching system integrates with the JSearch API to fetch relevant jobs based on user preferences and calculates relevance scores by comparing job descriptions with user resume data. The system is designed to:

1. Fetch jobs from JSearch API based on user job preferences
2. Get detailed job descriptions for each job
3. Calculate relevance scores using resume-to-job matching algorithms
4. Store results in the database for future reference

## Features

- **Intelligent Job Matching**: Uses advanced algorithms to match user skills and experience with job requirements
- **JSearch API Integration**: Fetches real-time job data from a comprehensive job search API
- **Relevance Scoring**: Calculates scores based on skills match (70%) and keyword similarity (30%)
- **Database Storage**: Stores jobs and match results for quick retrieval
- **Comprehensive Job Data**: Captures detailed job information including salary, benefits, requirements, etc.

## Setup and Configuration

### 1. API Key Setup

Get your JSearch API key from [RapidAPI](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) and add it to your environment:

```bash
# In your .env file
JSEARCH_API_KEY=your_jsearch_api_key_here
```

### 2. Database Schema

The system uses the following database tables:

#### Jobs Table
Stores comprehensive job information from JSearch API:
- Basic info (title, company, location, description, apply_link)
- Employment details (type, salary range, benefits)
- Location data (city, state, country, coordinates)
- Requirements (experience, skills, education)
- Company info (logo, website, rating)

#### Job Matches Table
Stores user-job relevance scores:
- user_id (foreign key to users table)
- job_id (foreign key to jobs table)
- relevance_score (calculated match percentage)

### 3. Required User Data

For job matching to work, users must have:
1. **Resume uploaded and parsed** - Contains skills, experience, projects, education
2. **Job preferences set** - Includes job title, location, experience level, employment types

## Usage

### API Endpoints

#### Trigger Job Matching
```http
POST /jobs/match
```

Triggers the complete job matching workflow:
1. Validates user has resume and preferences
2. Searches for jobs based on preferences
3. Fetches detailed job descriptions
4. Calculates relevance scores
5. Saves results to database

#### Get User's Job Matches
```http
GET /jobs/matches?limit=10&min_score=50.0
```

Returns sorted job matches for the authenticated user.

#### Get All Jobs
```http
GET /jobs?title_search=engineer&location_search=USA
```

Returns jobs from database with optional filtering.

### Command Line Tools

#### Simple API Test
Test JSearch API connectivity without database:
```bash
cd BackEnd/scripts
python simple_api_test.py YOUR_API_KEY
```

#### Job Matching CLI
Demonstrate matching algorithm with sample resume:
```bash
cd BackEnd/scripts
python job_matching_cli.py --api-key YOUR_API_KEY --query "Software Engineer" --location "USA"
```

#### Complete Test
Full workflow test with database:
```bash
cd BackEnd/scripts
python complete_test.py --api-key YOUR_API_KEY --user-email test@example.com
```

## Algorithm Details

### Relevance Score Calculation

The system uses a weighted scoring algorithm:

1. **Skills Matching (70% weight)**:
   - Extracts skills from user resume
   - Identifies required skills from job description
   - Calculates percentage match

2. **Keyword Matching (30% weight)**:
   - Extracts keywords from resume (projects, courses, experience)
   - Identifies keywords from job description
   - Calculates semantic similarity

3. **Final Score**:
   ```
   Relevance Score = (0.7 × Skills Score) + (0.3 × Keyword Score)
   ```

### Data Sources

**From Resume**:
- Technical skills list
- Project names and descriptions
- Course names
- Work experience descriptions
- Technologies used

**From Job Description**:
- Job qualifications
- Required skills
- Job responsibilities
- Job title and description text

## Configuration

### Environment Variables

```bash
# Required
JSEARCH_API_KEY=your_api_key_here

# Optional (with defaults)
MAX_JOBS_PER_MATCH=3
MIN_RELEVANCE_SCORE=0.0
```

### Job Search Parameters

The system automatically uses user preferences:
- **Query**: From user's job title preference
- **Location**: From user's location preference
- **Employment Type**: From user's employment type preferences
- **Experience Level**: Considered in scoring algorithm

## Error Handling

The system includes comprehensive error handling:

- **API Failures**: Graceful handling of JSearch API errors
- **Missing Data**: Validates required user data before processing
- **Database Errors**: Proper transaction management and rollback
- **Rate Limiting**: Respects API rate limits with appropriate delays

## Logging and Monitoring

All operations are logged with detailed information:
- API requests and responses
- Scoring calculations
- Database operations
- Error conditions

Example log output:
```
🔍 Searching for jobs: Software Engineer in USA
✅ Found 25 jobs from search
📄 Fetching details for job_id: abc123
📊 Relevance Score Calculation:
   Skills Match: 15/25 = 60.00%
   Keywords Match: 45/120 = 37.50%
   Final Score: 53.25%
💾 Saved job match: User 1 <-> Job abc123 (Score: 53.25%)
```

## Performance Considerations

- **API Rate Limits**: JSearch API has usage limits based on subscription
- **Job Limit**: Processing limited to 3 jobs per match for performance
- **Caching**: Jobs are stored in database to avoid re-fetching
- **Async Processing**: Job matching can be run as background task

## Integration with Frontend

The frontend can trigger job matching and display results:

```javascript
// Trigger job matching
const response = await fetch('/jobs/match', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` }
});

// Get matches
const matches = await fetch('/jobs/matches?limit=5', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

## Troubleshooting

### Common Issues

1. **No jobs found**: Check user preferences and API key
2. **Low relevance scores**: User may need to update resume or skills
3. **API errors**: Verify API key and check rate limits
4. **Missing parsed data**: Ensure resume was successfully uploaded and parsed

### Debug Mode

Enable debug logging for detailed information:
```bash
export DEBUG=True
```

## Future Enhancements

- **Machine Learning**: Implement ML-based scoring algorithms
- **User Feedback**: Learn from user job application behavior
- **Company Preferences**: Match based on company culture and values
- **Salary Optimization**: Consider salary expectations in matching
- **Location Intelligence**: Smart location matching (remote, nearby cities)

## Support

For issues or questions:
1. Check the logs for detailed error information
2. Verify API key and environment configuration
3. Test with simple_api_test.py to isolate issues
4. Review user data completeness (resume + preferences)
