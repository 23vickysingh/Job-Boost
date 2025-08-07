#!/usr/bin/env python3
"""
Database cleanup script to remove job-related tables.
"""

import os
import sys
from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL

def cleanup_job_tables():
    """Remove job-related tables from database."""
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        
        with engine.connect() as connection:
            # Start transaction
            trans = connection.begin()
            
            try:
                print("🗑️ Dropping job-related tables...")
                
                # Drop tables in correct order (considering foreign keys)
                tables_to_drop = [
                    "job_matches",
                    "jobs"
                ]
                
                for table in tables_to_drop:
                    try:
                        result = connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))
                        print(f"✅ Dropped table: {table}")
                    except Exception as e:
                        print(f"⚠️ Table {table} might not exist: {e}")
                
                # Remove last_job_search column from user_profile if it exists
                try:
                    connection.execute(text("ALTER TABLE user_profile DROP COLUMN IF EXISTS last_job_search;"))
                    print("✅ Removed last_job_search column from user_profile")
                except Exception as e:
                    print(f"⚠️ Column last_job_search might not exist: {e}")
                
                # Commit the transaction
                trans.commit()
                print("✅ Database cleanup completed successfully!")
                
            except Exception as e:
                trans.rollback()
                print(f"❌ Error during cleanup, transaction rolled back: {e}")
                
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")

if __name__ == "__main__":
    cleanup_job_tables()
