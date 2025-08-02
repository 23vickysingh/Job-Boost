# Job-Boost Application - Profile Update Guide

## Quick Start

### 1. Start the Backend Server

```bash
cd BackEnd
uvicorn main:app --reload --port 8000
```

The backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 2. Start the Frontend Development Server

```bash
cd FrontEnd
npm install  # if dependencies not installed
npm run dev
```

The frontend will be available at: http://localhost:5173

### 3. Test the Profile Section

1. **Register/Login**: Create an account or login with existing credentials
2. **Navigate to Dashboard**: You should see the dashboard with profile section
3. **Profile Data**: The profile section now displays:
   - User name and email from the `users` table
   - Job preferences from the `user_profile` table
   - Resume information from parsed resume data

## Profile Section Features

### ✅ User Information (from `users` table)
- **Email**: Displayed from `users.user_id` field
- **Name**: Extracted from resume data and stored as `user_name`

### ✅ Job Preferences (from `user_profile` table)
- **Job Title/Query**: What type of job you're looking for
- **Location**: Preferred work location
- **Work Mode**: Remote/Hybrid/On-site preference
- **Experience Level**: Years of experience
- **Employment Types**: Full-time, Part-time, Contract, etc.
- **Company Types**: Startup, Enterprise, Government, etc.
- **Additional Requirements**: Special requirements or notes

### ✅ Resume Information (from `resume_parsed` JSON)
- **Skills**: Technical and soft skills as badges
- **Experience**: Work history with timeline
- **Education**: Degrees and institutions
- **Projects**: Personal/academic projects with technologies
- **Achievements**: Awards and accomplishments
- **Certifications**: Professional certifications
- **Courses**: Additional courses taken

## Troubleshooting

### Profile Not Loading (404 Error)

If you see a 404 error or profile section not updating:

1. **Check Backend Status**:
   ```bash
   python test_backend_simple.py
   ```

2. **Verify Backend is Running**:
   - Go to http://localhost:8000/docs
   - You should see the FastAPI documentation

3. **Check Browser Console**:
   - Open browser developer tools (F12)
   - Look for API errors in the Console tab
   - Network tab will show API request details

4. **Authentication Issues**:
   - Make sure you're logged in
   - Token might be expired - try logging out and back in

### Profile Data Missing

If profile section loads but shows no data:

1. **Upload Resume**: Go to resume upload page and upload a resume
2. **Set Job Preferences**: Complete your job preferences
3. **Check Database**: Verify data exists in `user_profile` table

### Backend Connection Issues

1. **Port Conflicts**: Make sure port 8000 is available
2. **Dependencies**: Install Python dependencies:
   ```bash
   cd BackEnd
   pip install -r requirements.txt
   ```

3. **Database Issues**: Check if database tables exist and are accessible

## API Endpoints

### Profile Endpoints
- `GET /profile/` - Get user profile with user information
- `POST /profile/job-preferences` - Save job preferences
- `POST /profile/upload-resume` - Upload and parse resume
- `PUT /profile/` - Update profile information

### Enhanced Profile Response
The profile endpoint now returns:
```json
{
  "id": 1,
  "user_id": 1,
  "user_email": "user@example.com",
  "user_name": "John Doe",
  "query": "Software Developer",
  "location": "New York",
  "mode_of_job": "remote",
  "work_experience": "3-5 years",
  "employment_types": ["full-time"],
  "company_types": ["startup", "tech"],
  "job_requirements": "Python, React experience",
  "resume_parsed": {
    "personal_info": {...},
    "experience": [...],
    "education": [...],
    "skills": [...],
    // ... other resume data
  },
  "last_updated": "2025-08-03T10:00:00"
}
```

## Files Modified

### Backend
- `routers/profile.py` - Enhanced profile endpoint with user information
- `schemas.py` - Updated UserProfileOut schema

### Frontend
- `pages/Dashboard.tsx` - Added error handling and debugging
- `components/dashboard/UserProfile.tsx` - Enhanced profile display
- `components/dashboard/DashboardStats.tsx` - Dynamic profile strength
- `lib/api.ts` - Added API debugging

## Development Notes

- The profile section automatically handles missing data with fallbacks
- Profile strength is calculated dynamically based on completeness
- All user_profile table attributes are displayed in the UI
- Clean, modern interface with responsive design
- Error handling for network and authentication issues
