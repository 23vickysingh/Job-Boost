#!/usr/bin/env python3
"""
Migration script to add 'status' column to job_matches table
"""

from sqlalchemy import text
from database import engine

def add_status_column():
    """Add status column to job_matches table if it doesn't exist"""
    
    # Check if column already exists
    check_column_query = """
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'job_matches' 
    AND column_name = 'status'
    """
    
    with engine.connect() as conn:
        result = conn.execute(text(check_column_query))
        existing_columns = result.fetchall()
        
        if not existing_columns:
            print("Adding 'status' column to job_matches table...")
            
            # Add the status column with default value
            add_column_query = """
            ALTER TABLE job_matches 
            ADD COLUMN status VARCHAR(50) DEFAULT 'pending' NOT NULL
            """
            
            conn.execute(text(add_column_query))
            conn.commit()
            print("✅ Successfully added 'status' column to job_matches table")
        else:
            print("ℹ️  'status' column already exists in job_matches table")

if __name__ == "__main__":
    print("🔄 Running job_matches table migration...")
    try:
        add_status_column()
        print("✅ Migration completed successfully!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
