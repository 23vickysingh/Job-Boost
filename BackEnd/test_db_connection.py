#!/usr/bin/env python3
"""
Simple test script to verify database connection and UserProfile model works correctly.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append('/app')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import engine, get_db
from models import UserProfile, User
import traceback

def test_database_connection():
    """Test basic database connectivity and model queries."""
    
    print("Testing database connection...")
    
    try:
        # Test basic connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Database connected: {version}")
        
        # Test table structure
        with engine.connect() as conn:
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='user_profile' ORDER BY column_name;"))
            columns = [row[0] for row in result.fetchall()]
            print(f"✅ user_profile columns: {columns}")
            
            if 'last_job_search' in columns:
                print("✅ last_job_search column exists")
            else:
                print("❌ last_job_search column is missing!")
                return False
        
        # Test SQLAlchemy model query
        session = sessionmaker(bind=engine)()
        try:
            # Simple count query
            count = session.query(UserProfile).count()
            print(f"✅ UserProfile query works, found {count} profiles")
            
            # Test a more complex query like the one failing
            profile = session.query(UserProfile).filter(UserProfile.user_id == 1).first()
            print(f"✅ UserProfile complex query works")
            
        except Exception as e:
            print(f"❌ SQLAlchemy query failed: {e}")
            traceback.print_exc()
            return False
        finally:
            session.close()
            
        print("✅ All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
