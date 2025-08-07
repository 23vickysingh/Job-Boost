#!/usr/bin/env python3
"""
Database migration script to add detailed job information fields to jobs table.
This script adds new columns for storing detailed job information fetched from JSearch API.
"""

import sys
import os
import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

# Add the BackEnd directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import POSTGRES_DATABASE_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Run the database migration to add detailed job information fields."""
    try:
        # Create engine using the same logic as database.py
        if POSTGRES_DATABASE_URL:
            engine = create_engine(POSTGRES_DATABASE_URL)
        else:
            logger.info("⚠️ Warning: POSTGRES_DATABASE_URL not set, using fallback")
            engine = create_engine("postgresql://user:password@localhost:5432/job_boost_db")
        
        # Check which columns already exist
        inspector = inspect(engine)
        existing_columns = [col['name'] for col in inspector.get_columns('jobs')]
        
        # Define new columns to add
        new_columns = [
            ("detailed_description", "TEXT"),
            ("job_apply_options", "JSON"),
            ("job_publisher", "VARCHAR(255)"),
            ("estimated_salaries", "JSON"),
            ("job_posting_date", "TIMESTAMP"),
            ("job_apply_deadline", "TIMESTAMP"),
            ("detailed_requirements", "JSON"),
            ("detailed_responsibilities", "JSON"),
            ("company_info", "JSON"),
            ("is_detailed_fetched", "BOOLEAN DEFAULT FALSE")
        ]
        
        logger.info("📝 Adding detailed job information columns to jobs table...")
        
        with engine.connect() as connection:
            with connection.begin():
                columns_added = 0
                
                for column_name, column_type in new_columns:
                    if column_name not in existing_columns:
                        alter_sql = f"""
                        ALTER TABLE jobs 
                        ADD COLUMN {column_name} {column_type};
                        """
                        connection.execute(text(alter_sql))
                        logger.info(f"✅ Added column: {column_name}")
                        columns_added += 1
                    else:
                        logger.info(f"⏭️ Column '{column_name}' already exists")
                
                logger.info(f"🎉 Migration completed! Added {columns_added} new columns")
                
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
        columns = inspector.get_columns('jobs')
        
        # Check for new columns
        new_column_names = [
            'detailed_description', 'job_apply_options', 'job_publisher',
            'estimated_salaries', 'job_posting_date', 'job_apply_deadline',
            'detailed_requirements', 'detailed_responsibilities', 'company_info',
            'is_detailed_fetched'
        ]
        
        missing_columns = []
        for col_name in new_column_names:
            if not any(col['name'] == col_name for col in columns):
                missing_columns.append(col_name)
        
        if not missing_columns:
            logger.info("✅ Migration verification passed: all detailed job columns exist")
            logger.info("📋 Job table now includes:")
            for col in columns:
                if col['name'] in new_column_names:
                    logger.info(f"  - {col['name']}: {col['type']}")
            return True
        else:
            logger.error(f"❌ Migration verification failed: missing columns: {missing_columns}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during migration verification: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting database migration for detailed job information columns...")
    
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
