#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_database_with_localhost():
    """Test database connection using localhost instead of Docker service name"""
    print("🔍 Testing Database Connection with localhost...")
    
    try:
        from sqlalchemy import create_engine, text
        
        # Use localhost instead of 'postgres' service name
        db_url = "postgresql://user:password@localhost:5432/job_boost_db"
        print(f"📊 Database URL: {db_url}")
        
        print("🔧 Testing engine connection...")
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            print(f"✅ Connection successful: {result.fetchone()}")
        
        # Test table queries
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' LIMIT 5"))
            tables = result.fetchall()
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
                
            # Check for users
            try:
                result = connection.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.fetchone()[0]
                print(f"📊 Users in database: {user_count}")
            except Exception as e:
                print(f"⚠️ Could not query users table: {e}")
        
        print(f"✅ Database test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_database_with_localhost()
