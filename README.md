# Job Boost

A modern job application platform with AI-powered resume parsing and user profile management.

## Features

- User Authentication (Registration, Login, Password Reset)
- Profile Management with Job Preferences
- AI-Powered Resume Upload and Parsing
- Redis-based OTP System
- Clean Dashboard Interface

## Tech Stack

### Backend
- FastAPI (Python web framework)
- PostgreSQL (Database)
- Redis (Caching and OTP storage)
- Google Gemini AI (Resume parsing)
- Docker (Containerization)

### Frontend
- React + TypeScript
- Vite (Build tool)
- Tailwind CSS (Styling)
- React Router (Navigation)
- Context API (State management)

## Getting Started

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your environment variables
3. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```
4. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Project Structure

```
Job-Boost/
├── BackEnd/                 # FastAPI backend
│   ├── auth/               # Authentication logic
│   ├── routers/           # API route handlers
│   ├── services/          # Business logic services
│   ├── utils/             # Utility functions
│   ├── main.py            # FastAPI application
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   └── requirements.txt   # Python dependencies
├── FrontEnd/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── contexts/      # React contexts
│   │   └── lib/           # API utilities
│   └── package.json       # Node.js dependencies
├── docker-compose.yml     # Docker services configuration
└── README.md             # This file
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database
POSTGRES_DB=jobboost_db
POSTGRES_USER=jobboost_user
POSTGRES_PASSWORD=your_password

# Redis
REDIS_URL=redis://redis:6379/0

# API Keys
GEMINI_API_KEY=your_gemini_api_key
BREVO_API_KEY=your_brevo_api_key

# JWT
SECRET_KEY=your_secret_key
```

## API Endpoints

- `POST /user/register` - User registration
- `POST /user/login` - User login
- `POST /user/request-password-reset` - Request password reset
- `POST /user/reset-password` - Reset password
- `GET /profile/me` - Get user profile
- `PUT /profile/preferences` - Update job preferences
- `POST /profile/upload-resume` - Upload and parse resume

## License

This project is licensed under the MIT License.
