# Job Boost

A modern job application platform with AI-powered resume parsing and intelligent job-candidate matching.

## 🚀 Features

- **User Authentication** (Registration, Login, Password Reset)
- **Profile Management** with Job Preferences  
- **AI-Powered Resume Upload and Parsing** using Google Gemini API
- **Job-Resume Relevance Matching** with semantic similarity analysis
- **Redis-based OTP System** for secure authentication
- **Celery Background Tasks** for job searching and processing
- **Clean Dashboard Interface** with modern UI/UX

## 🛠 Tech Stack

### Backend
- **FastAPI** (Python web framework)
- **PostgreSQL** (Primary database)
- **Redis** (Caching, Celery broker, OTP storage)
- **Google Gemini AI** (Resume parsing & job relevance)
- **Celery** (Background task processing)
- **Docker** (Containerization)
- **SQLAlchemy** (ORM)

### Frontend
- **React + TypeScript**
- **Vite** (Build tool)
- **Tailwind CSS** (Styling)
- **Shadcn/ui** (UI components)
- **React Router** (Navigation)
- **Context API** (State management)

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Job-Boost
   ```

2. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   - `GOOGLE_API_KEY`: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - `BREVO_API_KEY`: Get from [Brevo](https://brevo.com)
   - `JSEARCH_API_KEY`: Get from [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)

3. **Start the Application**
   ```bash
   docker-compose up -d
   ```

4. **Access the Application**
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

### Manual Setup (Development)

1. **Backend Setup**
   ```bash
   cd BackEnd
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up -d postgres redis
   
   # Database will be automatically created on first run
   ```

3. **Start Backend**
   ```bash
   uvicorn main:app --reload
   ```

4. **Frontend Setup**
   ```bash
   cd FrontEnd
   npm install  # or bun install
   npm run dev  # or bun dev
   ```

## 📁 Project Structure

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
