#!/usr/bin/env python3
"""
Data migration script to separate existing resume text from parsed data.
This script handles existing profiles where resume_parsed contains both
raw text and structured data, separating them into appropriate fields.
"""

import sys
import os
import json
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the BackEnd directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import POSTGRES_DATABASE_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_existing_data():
    """Migrate existing resume data to separate text and parsed fields."""
    try:
        engine = create_engine(POSTGRES_DATABASE_URL)
        
        with engine.connect() as connection:
            with connection.begin():
                # Get all profiles with resume_parsed data but no resume_text
                select_sql = """
                SELECT id, resume_parsed 
                FROM user_profile 
                WHERE resume_parsed IS NOT NULL AND resume_text IS NULL;
                """
                
                result = connection.execute(text(select_sql))
                profiles = result.fetchall()
                
                if not profiles:
                    logger.info("📝 No profiles found that need data migration")
                    return True
                
                logger.info(f"🔄 Found {len(profiles)} profiles to migrate")
                
                migrated_count = 0
                for profile in profiles:
                    try:
                        profile_id = profile.id
                        resume_data = profile.resume_parsed
                        
                        if isinstance(resume_data, str):
                            resume_data = json.loads(resume_data)
                        
                        # Extract text and parsed data
                        resume_text = None
                        parsed_data = None
                        
                        # Check if this is old format with 'text' and 'parsed_data'
                        if isinstance(resume_data, dict) and 'text' in resume_data:
                            resume_text = resume_data.get('text')
                            parsed_data = resume_data.get('parsed_data', resume_data.get('gemini_response'))
                        
                        # Check if this is old format with 'resume_text' and 'gemini_response'
                        elif isinstance(resume_data, dict) and 'resume_text' in resume_data:
                            resume_text = resume_data.get('resume_text')
                            parsed_data = resume_data.get('gemini_response')
                        
                        # If it's already structured data (new format), keep as is
                        elif isinstance(resume_data, dict) and any(key in resume_data for key in ['personal_information', 'experience', 'education']):
                            parsed_data = resume_data
                            resume_text = None  # No text to extract
                        
                        # Update the profile
                        if resume_text or parsed_data:
                            update_sql = """
                            UPDATE user_profile 
                            SET resume_text = :resume_text,
                                resume_parsed = :resume_parsed
                            WHERE id = :profile_id;
                            """
                            
                            connection.execute(text(update_sql), {
                                'resume_text': resume_text,
                                'resume_parsed': json.dumps(parsed_data) if parsed_data else None,
                                'profile_id': profile_id
                            })
                            
                            migrated_count += 1
                            logger.info(f"✅ Migrated profile {profile_id}")
                        else:
                            logger.warning(f"⚠️ Could not extract data from profile {profile_id}")
                    
                    except Exception as e:
                        logger.error(f"❌ Error migrating profile {profile_id}: {e}")
                        continue
                
                logger.info(f"🎉 Successfully migrated {migrated_count} profiles")
                return True
                
    except SQLAlchemyError as e:
        logger.error(f"❌ Database error during data migration: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during data migration: {e}")
        return False

def verify_data_migration():
    """Verify the data migration results."""
    try:
        engine = create_engine(POSTGRES_DATABASE_URL)
        
        with engine.connect() as connection:
            # Count profiles with different states
            stats_sql = """
            SELECT 
                COUNT(*) as total_profiles,
                COUNT(CASE WHEN resume_text IS NOT NULL THEN 1 END) as with_text,
                COUNT(CASE WHEN resume_parsed IS NOT NULL THEN 1 END) as with_parsed,
                COUNT(CASE WHEN resume_text IS NOT NULL AND resume_parsed IS NOT NULL THEN 1 END) as with_both
            FROM user_profile;
            """
            
            result = connection.execute(text(stats_sql)).fetchone()
            
            logger.info("📊 Data migration verification:")
            logger.info(f"   Total profiles: {result.total_profiles}")
            logger.info(f"   With resume text: {result.with_text}")
            logger.info(f"   With parsed data: {result.with_parsed}")
            logger.info(f"   With both: {result.with_both}")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Error during data migration verification: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting data migration for resume text separation...")
    
    # Run data migration
    success = migrate_existing_data()
    
    if success:
        # Verify migration
        if verify_data_migration():
            logger.info("🎉 Data migration completed and verified successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Data migration verification failed")
            sys.exit(1)
    else:
        logger.error("❌ Data migration failed")
        sys.exit(1)
