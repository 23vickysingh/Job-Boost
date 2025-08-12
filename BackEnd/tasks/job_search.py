import time
import models
from sqlalchemy.orm import Session
from database import get_db, SessionLocal

from tasks.celery_app import app
from services.jsearch_service import fetch_jobs_from_api, JSearchAPIError
from utils.resume_parser import parse_resume_with_gemini # Assuming Gemini logic is here

# --- Master Scheduler Task ---

@app.task(bind=True, name='tasks.job_search.schedule_daily_job_searches')
def schedule_daily_job_searches(self):
    """
    Scheduled task to run daily.
    
    This task queries for all users who have a complete profile (resume and preferences)
    and queues an individual job search task for each of them.
    """
    print("Executing daily job search schedule...")
    db: Session = SessionLocal()
    try:
        # Find all users who have both a resume and job preferences (query) set
        eligible_users = db.query(models.User).join(models.UserProfile).filter(
            models.UserProfile.resume_location.isnot(None),
            models.UserProfile.query.isnot(None)
        ).all()

        if not eligible_users:
            print("No eligible users found for the daily job search.")
            return

        print(f"Found {len(eligible_users)} eligible users. Queueing individual tasks...")
        
        # For each eligible user, create a separate background task
        for user in eligible_users:
            print(f"Queueing job search for user ID: {user.id}")
            # .delay() sends the task to the Celery queue to be processed by a worker
            find_and_match_jobs_for_user.delay(user.id)
            
        return f"Successfully queued job searches for {len(eligible_users)} users."
    
    except Exception as e:
        print(f"ERROR: Failed during daily job search scheduling: {e}")
        # self.retry(exc=e, countdown=60) # Optional: retry the task after 60 seconds
    finally:
        db.close()
        print("Database connection closed.")
    return "Daily Job Searches scheduled."


# --- Individual Worker Task ---

@app.task(bind=True, name='tasks.job_search.find_and_match_jobs_for_user')
def find_and_match_jobs_for_user(self, user_id: int):
    """
    Worker task to find and match jobs for a single user.
    
    This task performs the heavy lifting: fetching jobs, checking for duplicates,
    saving new jobs, and running relevance comparison with Gemini AI.
    """
    print(f"Starting job search and match process for user ID: {user_id}")
    db: Session = SessionLocal()
    try:
        # Step 1: Fetch user and their profile from the database
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user or not user.profile:
            print(f"User with ID {user_id} or their profile not found. Skipping.")
            return

        # Step 2: Fetch job listings from JSearch API using the user's profile
        try:
            jobs_from_api = fetch_jobs_from_api(user.profile)
        except JSearchAPIError as e:
            print(f"Failed to fetch jobs for user {user_id} from JSearch API: {e}")
            # self.retry(exc=e, countdown=300) # Optional: retry after 5 minutes on API failure
            return

        if not jobs_from_api:
            print(f"No new jobs found from API for user {user_id}. Process finished.")
            return

        print(f"Found {len(jobs_from_api)} potential jobs for user {user_id}. Processing...")

        # Step 3: Loop through each job, check for duplicates, and process new ones
        new_jobs_processed = 0
        for job_data in jobs_from_api:
            api_job_id = job_data.get("job_id")
            if not api_job_id:
                continue # Skip if the job has no ID

            # Check if this job already exists in our database
            existing_job = db.query(models.Job).filter(models.Job.job_id == api_job_id).first()
            
            if existing_job:
                # Job already exists, we can skip it for now.
                # In the future, you could check if this user has already been matched with it.
                continue

            # This is a new job, so we save it to our 'jobs' table
            new_job = models.Job(
                job_id=api_job_id,
                employer_name=job_data.get("employer_name"),
                job_title=job_data.get("job_title"),
                job_description=job_data.get("job_description"),
                job_apply_link=job_data.get("job_apply_link"),
                job_city=job_data.get("job_city"),
                job_country=job_data.get("job_country"),
                job_employment_type=job_data.get("job_employment_type"),
                job_is_remote=job_data.get("job_is_remote", False),
                job_posted_at_datetime_utc=job_data.get("job_posted_at_datetime_utc"),
                job_required_skills=job_data.get("job_required_skills"),
                job_min_salary=job_data.get("job_min_salary"),
                job_max_salary=job_data.get("job_max_salary"),
                job_salary_currency=job_data.get("job_salary_currency"),
                job_salary_period=job_data.get("job_salary_period"),
                job_api_response=job_data # Store the full API response
            )
            db.add(new_job)
            db.commit()
            db.refresh(new_job)
            
            # Step 4: Compare resume with the new job description using Gemini AI
            # This is a placeholder for your actual Gemini API call
            relevance_score = 0.0
            if user.profile.resume_text and new_job.job_description:
                # In a real scenario, you'd call your Gemini service here
                # relevance_score = await your_gemini_service.get_relevance_score(
                #     user.profile.resume_text, new_job.job_description
                # )
                # For now, we'll simulate a score
                relevance_score = round(random.uniform(0.65, 0.95), 4)

            # Step 5: Save the match and score to the 'job_matches' table
            job_match = models.JobMatch(
                user_id=user.id,
                job_id=new_job.id,
                relevance_score=relevance_score
            )
            db.add(job_match)
            db.commit()
            
            new_jobs_processed += 1
            print(f"Processed and matched new job '{new_job.job_title}' for user {user_id} with score {relevance_score}")
            
            # Respect API rate limits
            time.sleep(1) 

        return f"Completed job search for user {user_id}. Processed {new_jobs_processed} new jobs."

    except Exception as e:
        print(f"FATAL ERROR for user {user_id}: {e}")
        db.rollback() # Rollback any partial database changes
        # self.retry(exc=e, countdown=600) # Optional: retry the whole task after 10 minutes
    finally:
        db.close()