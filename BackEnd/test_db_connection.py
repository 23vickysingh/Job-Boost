#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

def test_database_connection():
    """Test basic database connectivity"""
    print("🔍 Testing Database Connection...")
    
    try:
        print("📦 Importing modules...")
        from sqlalchemy import create_engine, text
        from database import SessionLocal, POSTGRES_DATABASE_URL
        
        print(f"✅ Modules imported")
        print(f"📊 Database URL: {POSTGRES_DATABASE_URL}")
        
        # Test direct engine connection
        print("🔧 Testing engine connection...")
        engine = create_engine(POSTGRES_DATABASE_URL)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            print(f"✅ Direct engine connection successful: {result.fetchone()}")
        
        # Test SessionLocal
        print("🔧 Testing SessionLocal...")
        db = SessionLocal()
        result = db.execute(text("SELECT version()"))
        version = result.fetchone()
        print(f"✅ SessionLocal connection successful")
        print(f"   PostgreSQL version: {version[0] if version else 'Unknown'}")
        
        # Test table access
        print("🔧 Testing table access...")
        result = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' LIMIT 5"))
        tables = result.fetchall()
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        db.close()
        print(f"✅ Database connection test completed successfully!")
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_connection()
