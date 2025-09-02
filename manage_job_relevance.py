#!/usr/bin/env python3
"""
Job Relevance Database Management Script

This script helps manage job relevance calculations in the database.
Use this to calculate relevance scores for existing job matches.
"""

import sys
import os
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the BackEnd directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'BackEnd'))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Import necessary modules
from database import get_db_url, Base
from services.job_relevance_service import calculate_job_relevance, calculate_all_user_job_relevances, recalculate_all_relevances
import models

async def main():
    print("🔍 Job Relevance Database Management")
    print("=" * 50)
    
    # Create database connection
    try:
        DATABASE_URL = get_db_url()
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        print("✅ Database connection established")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return
    
    while True:
        print("\nChoose an option:")
        print("1. Calculate relevance for a specific job match")
        print("2. Calculate relevance for all matches of a user")
        print("3. Recalculate all missing relevance scores")
        print("4. View job matches without relevance scores")
        print("5. View statistics")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        try:
            if choice == "1":
                await handle_single_match_relevance(db)
            elif choice == "2":
                await handle_user_relevances(db)
            elif choice == "3":
                await handle_batch_recalculation(db)
            elif choice == "4":
                view_missing_relevances(db)
            elif choice == "5":
                view_statistics(db)
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
        
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    db.close()

async def handle_single_match_relevance(db):
    """Calculate relevance for a specific job match."""
    try:
        match_id = int(input("Enter job match ID: ").strip())
        
        print(f"Calculating relevance for job match {match_id}...")
        relevance_score = await calculate_job_relevance(match_id, db)
        
        if relevance_score is not None:
            print(f"✅ Relevance calculated: {relevance_score:.2f} ({int(relevance_score * 100)}%)")
        else:
            print("❌ Failed to calculate relevance. Check that the job match exists and has required data.")
            
    except ValueError:
        print("❌ Invalid job match ID. Please enter a number.")
    except Exception as e:
        print(f"❌ Error calculating relevance: {e}")

async def handle_user_relevances(db):
    """Calculate relevance for all matches of a specific user."""
    try:
        user_id = int(input("Enter user ID: ").strip())
        
        print(f"Calculating relevance for all job matches of user {user_id}...")
        results = await calculate_all_user_job_relevances(user_id, db)
        
        if results:
            print(f"✅ Calculated relevance for {len(results)} job matches:")
            for match_id, score in results.items():
                print(f"  - Match {match_id}: {score:.2f} ({int(score * 100)}%)")
        else:
            print("❌ No job matches found or no relevance scores calculated.")
            
    except ValueError:
        print("❌ Invalid user ID. Please enter a number.")
    except Exception as e:
        print(f"❌ Error calculating user relevances: {e}")

async def handle_batch_recalculation(db):
    """Recalculate all missing relevance scores."""
    try:
        limit = input("Enter maximum number of matches to process (default 50): ").strip()
        limit = int(limit) if limit else 50
        
        print(f"Recalculating up to {limit} missing relevance scores...")
        print("⚠️  This may take a while depending on the number of matches.")
        
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Operation cancelled.")
            return
        
        stats = await recalculate_all_relevances(db, limit=limit)
        
        print("\n📊 Batch Recalculation Results:")
        print(f"  - Processed: {stats['processed']}")
        print(f"  - Updated: {stats['updated']}")
        print(f"  - Errors: {stats['errors']}")
        
    except ValueError:
        print("❌ Invalid limit. Please enter a number.")
    except Exception as e:
        print(f"❌ Error in batch recalculation: {e}")

def view_missing_relevances(db):
    """View job matches without relevance scores."""
    try:
        matches = db.query(models.JobMatch).filter(
            models.JobMatch.relevance_score.is_(None)
        ).limit(20).all()
        
        if not matches:
            print("✅ All job matches have relevance scores!")
            return
        
        print(f"\n📋 Job Matches Missing Relevance Scores (showing up to 20):")
        print("-" * 80)
        print(f"{'ID':<6} {'User ID':<8} {'Job Title':<25} {'Company':<20} {'Created'}")
        print("-" * 80)
        
        for match in matches:
            job_title = (match.job_title or "Unknown")[:24]
            company = (match.company_name or "Unknown")[:19]
            created = match.created_at.strftime("%Y-%m-%d") if match.created_at else "Unknown"
            
            print(f"{match.id:<6} {match.user_id:<8} {job_title:<25} {company:<20} {created}")
        
        total_missing = db.query(models.JobMatch).filter(
            models.JobMatch.relevance_score.is_(None)
        ).count()
        
        print(f"\nTotal matches missing relevance: {total_missing}")
        
    except Exception as e:
        print(f"❌ Error viewing missing relevances: {e}")

def view_statistics(db):
    """View relevance score statistics."""
    try:
        # Total matches
        total_matches = db.query(models.JobMatch).count()
        
        # Matches with relevance scores
        with_relevance = db.query(models.JobMatch).filter(
            models.JobMatch.relevance_score.is_not(None)
        ).count()
        
        # Matches without relevance scores
        without_relevance = total_matches - with_relevance
        
        # Average relevance score
        if with_relevance > 0:
            avg_relevance = db.query(
                models.JobMatch.relevance_score
            ).filter(
                models.JobMatch.relevance_score.is_not(None)
            ).all()
            
            scores = [score[0] for score in avg_relevance if score[0] is not None]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            # Score distribution
            excellent = sum(1 for s in scores if s >= 0.8)
            good = sum(1 for s in scores if 0.6 <= s < 0.8)
            fair = sum(1 for s in scores if 0.4 <= s < 0.6)
            poor = sum(1 for s in scores if s < 0.4)
        else:
            avg_score = 0
            excellent = good = fair = poor = 0
        
        print("\n📊 Job Relevance Statistics:")
        print("-" * 40)
        print(f"Total Job Matches: {total_matches}")
        print(f"With Relevance Scores: {with_relevance}")
        print(f"Without Relevance Scores: {without_relevance}")
        print(f"Coverage: {(with_relevance/total_matches*100):.1f}%" if total_matches > 0 else "Coverage: 0%")
        
        if with_relevance > 0:
            print(f"\nAverage Relevance Score: {avg_score:.2f} ({int(avg_score * 100)}%)")
            print("\nScore Distribution:")
            print(f"  Excellent (80-100%): {excellent}")
            print(f"  Good (60-79%): {good}")
            print(f"  Fair (40-59%): {fair}")
            print(f"  Poor (0-39%): {poor}")
        
    except Exception as e:
        print(f"❌ Error viewing statistics: {e}")

if __name__ == "__main__":
    asyncio.run(main())
