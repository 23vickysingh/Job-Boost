#!/usr/bin/env python3
"""
Database migration script to:
1. Add external_id column to jobs table
2. Add unique constraint to job_matches table
3. Populate external_id from existing job_id values
"""

import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect, create_engine
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
    from models import Job, JobMatch
except ImportError as e:
    print(f"❌ Error importing models: {e}")
    print("💡 Make sure you're running this script from the BackEnd directory")
    sys.exit(1)

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table."""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def check_constraint_exists(table_name, constraint_name):
    """Check if a constraint exists in a table."""
    inspector = inspect(engine)
    try:
        constraints = inspector.get_unique_constraints(table_name)
        return any(constraint['name'] == constraint_name for constraint in constraints)
    except:
        return False

def add_external_id_column():
    """Add external_id column to jobs table if it doesn't exist."""
    db: Session = SessionLocal()
    
    try:
        if check_column_exists('jobs', 'external_id'):
            print("✅ external_id column already exists in jobs table")
            return True
            
        print("🔧 Adding external_id column to jobs table...")
        
        # Add the column
        db.execute(text("ALTER TABLE jobs ADD COLUMN external_id VARCHAR(255)"))
        
        # Create index
        db.execute(text("CREATE INDEX idx_jobs_external_id ON jobs(external_id)"))
        
        # Populate external_id with existing job_id values
        print("📝 Populating external_id with existing job_id values...")
        db.execute(text("UPDATE jobs SET external_id = job_id WHERE external_id IS NULL"))
        
        db.commit()
        print("✅ Successfully added external_id column and populated data")
        return True
        
    except Exception as e:
        print(f"❌ Error adding external_id column: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def add_unique_constraint():
    """Add unique constraint to job_matches table if it doesn't exist."""
    db: Session = SessionLocal()
    
    try:
        if check_constraint_exists('job_matches', 'unique_user_job_match'):
            print("✅ Unique constraint already exists on job_matches table")
            return True
            
        print("🔧 Adding unique constraint to job_matches table...")
        
        # First, we need to ensure there are no duplicates
        print("🔍 Checking for existing duplicates...")
        duplicates_check = db.execute(text("""
            SELECT user_id, job_id, COUNT(*) as count
            FROM job_matches 
            GROUP BY user_id, job_id 
            HAVING COUNT(*) > 1
        """)).fetchall()
        
        if duplicates_check:
            print(f"⚠️  Found {len(duplicates_check)} sets of duplicates!")
            print("❌ Cannot add unique constraint with existing duplicates.")
            print("🔧 Please run the duplicate removal script first:")
            print("   python remove_duplicates.py")
            return False
        
        # Add the unique constraint
        db.execute(text("""
            ALTER TABLE job_matches 
            ADD CONSTRAINT unique_user_job_match 
            UNIQUE (user_id, job_id)
        """))
        
        db.commit()
        print("✅ Successfully added unique constraint to job_matches table")
        return True
        
    except Exception as e:
        print(f"❌ Error adding unique constraint: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def verify_migration():
    """Verify that the migration was successful."""
    print("\n🔍 Verifying migration...")
    
    # Check external_id column
    external_id_exists = check_column_exists('jobs', 'external_id')
    print(f"   external_id column: {'✅ EXISTS' if external_id_exists else '❌ MISSING'}")
    
    # Check unique constraint
    constraint_exists = check_constraint_exists('job_matches', 'unique_user_job_match')
    print(f"   unique constraint: {'✅ EXISTS' if constraint_exists else '❌ MISSING'}")
    
    # Check data
    db: Session = SessionLocal()
    try:
        jobs_with_external_id = db.execute(text("SELECT COUNT(*) FROM jobs WHERE external_id IS NOT NULL")).scalar()
        total_jobs = db.execute(text("SELECT COUNT(*) FROM jobs")).scalar()
        print(f"   jobs with external_id: {jobs_with_external_id}/{total_jobs}")
        
        if external_id_exists and constraint_exists and jobs_with_external_id == total_jobs:
            print("\n🎉 Migration completed successfully!")
            return True
        else:
            print("\n❌ Migration incomplete!")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False
    finally:
        db.close()

def main():
    print("🚀 Database Migration Script")
    print("=" * 50)
    print("This script will:")
    print("1. Add external_id column to jobs table")
    print("2. Add unique constraint to job_matches table")
    print("3. Populate external_id with existing job_id values")
    print()
    
    # Step 1: Add external_id column
    if not add_external_id_column():
        print("❌ Failed to add external_id column. Aborting migration.")
        return False
    
    print()
    
    # Step 2: Add unique constraint
    if not add_unique_constraint():
        print("❌ Failed to add unique constraint. Migration partially completed.")
        print("💡 You may need to run the duplicate removal script first.")
        return False
    
    print()
    
    # Step 3: Verify migration
    success = verify_migration()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Run the duplicate removal script if needed: python remove_duplicates.py")
        print("2. Test the job search functionality")
        print("3. Monitor for any duplicate creation issues")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)