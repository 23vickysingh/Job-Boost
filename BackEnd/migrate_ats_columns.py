#!/usr/bin/env python3
"""
Migration script to add ats_score and ats_score_calculated_at columns to user_profile table.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import get_database_url

def run_migration():
    """Run the migration to add ATS score columns."""
    
    # Get database URL
    database_url = get_database_url()
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = SessionLocal()
    
    try:
        print("Starting migration to add ATS score columns to user_profile table...")
        
        # Add ats_score column if it doesn't exist
        try:
            session.execute(text("""
                ALTER TABLE user_profile 
                ADD COLUMN ats_score FLOAT;
            """))
            print("✓ Added ats_score column")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("⚠ ats_score column already exists, skipping...")
            else:
                print(f"Error adding ats_score column: {e}")
                raise
        
        # Add ats_score_calculated_at column if it doesn't exist
        try:
            session.execute(text("""
                ALTER TABLE user_profile 
                ADD COLUMN ats_score_calculated_at TIMESTAMP;
            """))
            print("✓ Added ats_score_calculated_at column")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("⚠ ats_score_calculated_at column already exists, skipping...")
            else:
                print(f"Error adding ats_score_calculated_at column: {e}")
                raise
        
        # Commit all changes
        session.commit()
        print("✅ Migration completed successfully!")
        
        # Verify the columns were added
        result = session.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'user_profile' 
            AND column_name IN ('ats_score', 'ats_score_calculated_at')
            ORDER BY column_name;
        """))
        
        columns = result.fetchall()
        print("\n📋 Verified columns in user_profile table:")
        for column in columns:
            print(f"  - {column[0]}: {column[1]}")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    run_migration()
