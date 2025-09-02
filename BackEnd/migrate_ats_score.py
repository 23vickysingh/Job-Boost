"""
Database migration script to add ATS scoring columns to user_profile table.
Run this script to update the database schema.
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: DATABASE_URL environment variable not found")
    sys.exit(1)

def run_migration():
    """Add ATS scoring columns to user_profile table."""
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            # Check if columns already exist
            result = connection.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user_profile' 
                AND column_name IN ('ats_score', 'ats_score_calculated_at')
            """))
            
            existing_columns = [row[0] for row in result]
            
            # Add ats_score column if it doesn't exist
            if 'ats_score' not in existing_columns:
                print("Adding ats_score column...")
                connection.execute(text("""
                    ALTER TABLE user_profile 
                    ADD COLUMN ats_score INTEGER NULL
                """))
                print("✓ ats_score column added")
            else:
                print("ats_score column already exists")
            
            # Add ats_score_calculated_at column if it doesn't exist
            if 'ats_score_calculated_at' not in existing_columns:
                print("Adding ats_score_calculated_at column...")
                connection.execute(text("""
                    ALTER TABLE user_profile 
                    ADD COLUMN ats_score_calculated_at TIMESTAMP NULL
                """))
                print("✓ ats_score_calculated_at column added")
            else:
                print("ats_score_calculated_at column already exists")
            
            # Commit the changes
            connection.commit()
            print("Migration completed successfully!")
            
    except Exception as e:
        print(f"Migration failed: {str(e)}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("Running ATS score migration...")
    run_migration()
