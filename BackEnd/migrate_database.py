#!/usr/bin/env python3
"""
Database migration script to add missing columns to existing tables.
Run this script to update the database schema when new columns are added to models.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

# Add the parent directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine

def migrate_database():
    """Add missing columns to existing tables."""
    
    print("Starting database migration...")
    
    # Check if last_job_search column exists, if not add it
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='user_profile' AND column_name='last_job_search';
            """))
            
            if not result.fetchone():
                print("Adding last_job_search column to user_profile table...")
                conn.execute(text("""
                    ALTER TABLE user_profile 
                    ADD COLUMN last_job_search TIMESTAMP;
                """))
                conn.commit()
                print("✅ Added last_job_search column successfully")
            else:
                print("✅ last_job_search column already exists")
                
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False
    
    print("✅ Database migration completed successfully!")
    return True

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
