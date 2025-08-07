#!/usr/bin/env python3
"""
Database migration script to add resume_text column to user_profile table.
This script adds the new resume_text column to store raw extracted text
separately from the processed resume_parsed data.
"""

import sys
import os
import logging
from sqlalchemy import create_engine, text, Column, Text, inspect
from sqlalchemy.exc import SQLAlchemyError

# Add the BackEnd directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import POSTGRES_DATABASE_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Run the database migration to add resume_text column."""
    try:
        # Create engine using the same logic as database.py
        if POSTGRES_DATABASE_URL:
            engine = create_engine(POSTGRES_DATABASE_URL)
        else:
            logger.info("⚠️ Warning: POSTGRES_DATABASE_URL not set, using fallback")
            engine = create_engine("postgresql://user:password@localhost:5432/job_boost_db")
        
        # Check if the column already exists
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('user_profile')]
        
        if 'resume_text' in columns:
            logger.info("✅ Column 'resume_text' already exists in user_profile table")
            return True
        
        logger.info("📝 Adding resume_text column to user_profile table...")
        
        # Add the resume_text column
        with engine.connect() as connection:
            # Begin transaction
            with connection.begin():
                # Add the new column
                alter_sql = """
                ALTER TABLE user_profile 
                ADD COLUMN resume_text TEXT;
                """
                connection.execute(text(alter_sql))
                logger.info("✅ Column 'resume_text' added successfully")
                
                # Optional: Migrate existing data if needed
                # Check if there are any profiles with resume_parsed but no resume_text
                check_sql = """
                SELECT COUNT(*) as count 
                FROM user_profile 
                WHERE resume_parsed IS NOT NULL AND resume_text IS NULL;
                """
                result = connection.execute(text(check_sql)).fetchone()
                
                if result and result.count > 0:
                    logger.info(f"📋 Found {result.count} profiles with parsed data but no resume text")
                    logger.info("💡 Consider running data migration to extract text from existing parsed data")
                
        logger.info("🎉 Migration completed successfully!")
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"❌ Database error during migration: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during migration: {e}")
        return False

def verify_migration():
    """Verify that the migration was successful."""
    try:
        # Create engine using the same logic as database.py
        if POSTGRES_DATABASE_URL:
            engine = create_engine(POSTGRES_DATABASE_URL)
        else:
            logger.info("⚠️ Warning: POSTGRES_DATABASE_URL not set, using fallback")
            engine = create_engine("postgresql://user:password@localhost:5432/job_boost_db")
        inspector = inspect(engine)
        columns = inspector.get_columns('user_profile')
        
        # Check if resume_text column exists
        resume_text_exists = any(col['name'] == 'resume_text' for col in columns)
        
        if resume_text_exists:
            logger.info("✅ Migration verification passed: resume_text column exists")
            
            # Show column details
            for col in columns:
                if col['name'] == 'resume_text':
                    logger.info(f"📋 Column details: {col}")
            
            return True
        else:
            logger.error("❌ Migration verification failed: resume_text column not found")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during migration verification: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting database migration for resume_text column...")
    
    # Run migration
    success = run_migration()
    
    if success:
        # Verify migration
        if verify_migration():
            logger.info("🎉 Database migration completed and verified successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Migration verification failed")
            sys.exit(1)
    else:
        logger.error("❌ Migration failed")
        sys.exit(1)
