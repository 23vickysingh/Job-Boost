#!/usr/bin/env python3
"""
Migration script to add job_title and company_name columns to job_matches table
and populate them with data from the related jobs table.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import get_database_url

def run_migration():
    """Run the migration to add job_title and company_name columns."""
    
    # Get database URL
    database_url = get_database_url()
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = SessionLocal()
    
    try:
        print("Starting migration to add job_title and company_name columns...")
        
        # Add job_title column if it doesn't exist
        try:
            session.execute(text("""
                ALTER TABLE job_matches 
                ADD COLUMN job_title VARCHAR(500);
            """))
            print("✓ Added job_title column")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("⚠ job_title column already exists, skipping...")
            else:
                print(f"Error adding job_title column: {e}")
                raise
        
        # Add company_name column if it doesn't exist
        try:
            session.execute(text("""
                ALTER TABLE job_matches 
                ADD COLUMN company_name VARCHAR(500);
            """))
            print("✓ Added company_name column")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("⚠ company_name column already exists, skipping...")
            else:
                print(f"Error adding company_name column: {e}")
                raise
        
        # Update existing records with job details from jobs table
        session.execute(text("""
            UPDATE job_matches 
            SET 
                job_title = jobs.job_title,
                company_name = jobs.employer_name
            FROM jobs 
            WHERE job_matches.job_id = jobs.id 
            AND (job_matches.job_title IS NULL OR job_matches.company_name IS NULL);
        """))
        
        updated_rows = session.execute(text("SELECT ROW_COUNT();")).fetchone()
        print(f"✓ Updated {updated_rows[0] if updated_rows else 'unknown'} existing job match records with job details")
        
        # Commit all changes
        session.commit()
        print("✅ Migration completed successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    run_migration()
