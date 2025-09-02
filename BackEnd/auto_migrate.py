"""
Auto-migration function to add ATS score columns if they don't exist.
This will be called when the application starts.
"""

from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

def migrate_ats_columns(db_session):
    """Add ATS score columns to user_profile table if they don't exist."""
    try:
        # Check if columns exist
        result = db_session.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'user_profile' 
            AND column_name IN ('ats_score', 'ats_score_calculated_at')
        """))
        
        existing_columns = [row[0] for row in result]
        
        # Add ats_score column if it doesn't exist
        if 'ats_score' not in existing_columns:
            logger.info("Adding ats_score column to user_profile table...")
            db_session.execute(text("""
                ALTER TABLE user_profile 
                ADD COLUMN ats_score INTEGER NULL
            """))
            logger.info("✓ ats_score column added successfully")
        else:
            logger.info("ats_score column already exists")
        
        # Add ats_score_calculated_at column if it doesn't exist
        if 'ats_score_calculated_at' not in existing_columns:
            logger.info("Adding ats_score_calculated_at column to user_profile table...")
            db_session.execute(text("""
                ALTER TABLE user_profile 
                ADD COLUMN ats_score_calculated_at TIMESTAMP NULL
            """))
            logger.info("✓ ats_score_calculated_at column added successfully")
        else:
            logger.info("ats_score_calculated_at column already exists")
        
        # Commit the changes
        db_session.commit()
        logger.info("ATS score migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        db_session.rollback()
        raise e
