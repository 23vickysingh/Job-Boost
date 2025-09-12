#!/usr/bin/env python3
"""
Script to remove duplicate job matches from the database.
Keeps only the earliest entry for each (user_id, job_id) combination.
"""

import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import text, func, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create database connection directly
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # If running locally (not in Docker), replace 'postgres' hostname with 'localhost'
    if 'postgres:5432' in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace('postgres:5432', 'localhost:5432')
        print(f"🔧 Adjusted DATABASE_URL for local execution: {DATABASE_URL}")
else:
    # Fallback to default database URL if not set
    DATABASE_URL = "postgresql://user:password@localhost:5432/job_boost_db"
    print(f"⚠️  DATABASE_URL not found in environment, using fallback: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, echo=False)
    # Test connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print(f"✅ Successfully connected to database")
except Exception as e:
    print(f"❌ Failed to connect to database: {e}")
    print(f"💡 Make sure PostgreSQL is running on localhost:5432")
    print(f"💡 Or run this script inside Docker: docker-compose exec app python migrate_database.py")
    sys.exit(1)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models after setting up database connection
try:
    from models import JobMatch, Job, User
except ImportError as e:
    print(f"❌ Error importing models: {e}")
    print("💡 Make sure you're running this script from the BackEnd directory")
    sys.exit(1)

def remove_duplicate_job_matches():
    """Remove duplicate job matches, keeping only the earliest one per user-job combination."""
    db: Session = SessionLocal()
    
    try:
        print("🔍 Analyzing duplicate job matches...")
        
        # Find duplicates using group by
        duplicates_query = text("""
            SELECT user_id, job_id, COUNT(*) as count, MIN(id) as keep_id, MAX(id) as latest_id
            FROM job_matches 
            GROUP BY user_id, job_id 
            HAVING COUNT(*) > 1
            ORDER BY COUNT(*) DESC
        """)
        
        duplicates = db.execute(duplicates_query).fetchall()
        
        if not duplicates:
            print("✅ No duplicate job matches found!")
            return
        
        print(f"📊 Found {len(duplicates)} sets of duplicate job matches")
        
        total_to_delete = 0
        for row in duplicates:
            user_id, job_id, count, keep_id, latest_id = row
            total_to_delete += (count - 1)
            print(f"  User {user_id}, Job {job_id}: {count} entries (keeping ID {keep_id})")
        
        print(f"🗑️  Total entries to delete: {total_to_delete}")
        
        # Confirm deletion
        confirm = input("Do you want to proceed with deletion? (yes/no): ").lower().strip()
        if confirm not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            return
        
        # Delete duplicates, keeping only the entry with minimum ID (earliest)
        delete_query = text("""
            DELETE jm1 FROM job_matches jm1
            INNER JOIN (
                SELECT user_id, job_id, MIN(id) as min_id
                FROM job_matches
                GROUP BY user_id, job_id
                HAVING COUNT(*) > 1
            ) jm2 ON jm1.user_id = jm2.user_id 
                   AND jm1.job_id = jm2.job_id 
                   AND jm1.id > jm2.min_id
        """)
        
        result = db.execute(delete_query)
        deleted_count = result.rowcount
        db.commit()
        
        print(f"✅ Successfully removed {deleted_count} duplicate job matches!")
        
        # Verify cleanup
        remaining_duplicates = db.execute(duplicates_query).fetchall()
        if remaining_duplicates:
            print(f"⚠️  Warning: {len(remaining_duplicates)} duplicate sets still exist")
        else:
            print("✅ All duplicates have been successfully removed!")
            
    except Exception as e:
        print(f"❌ Error removing duplicates: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def show_statistics():
    """Show database statistics before and after cleanup."""
    db: Session = SessionLocal()
    
    try:
        # Total job matches
        total_matches = db.query(JobMatch).count()
        
        # Unique user-job combinations
        unique_combinations = db.query(
            func.count(func.distinct(JobMatch.user_id + JobMatch.job_id * 10000))
        ).scalar()
        
        # Users with matches
        users_with_matches = db.query(
            func.count(func.distinct(JobMatch.user_id))
        ).scalar()
        
        # Jobs with matches
        jobs_with_matches = db.query(
            func.count(func.distinct(JobMatch.job_id))
        ).scalar()
        
        print(f"""
📊 Database Statistics:
   • Total job matches: {total_matches}
   • Unique user-job combinations: {unique_combinations}
   • Users with matches: {users_with_matches}
   • Jobs with matches: {jobs_with_matches}
   • Potential duplicates: {total_matches - unique_combinations if total_matches > unique_combinations else 0}
        """)
        
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🧹 Job Match Duplicate Removal Tool")
    print("=" * 50)
    
    print("\n📊 Current Statistics:")
    show_statistics()
    
    print("\n🔧 Starting duplicate removal process...")
    remove_duplicate_job_matches()
    
    print("\n📊 Final Statistics:")
    show_statistics()
    
    print("\n✅ Process completed!")