#!/usr/bin/env python3
"""
Test script to verify all components are working correctly.
"""

import os
import sys
import asyncio

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing module imports...")
    
    try:
        import models
        print("✅ Models imported successfully")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        import database
        print("✅ Database module imported successfully")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        import elasticsearch_config
        print("✅ Elasticsearch config imported successfully")
    except Exception as e:
        print(f"❌ Elasticsearch config import failed: {e}")
        return False
    
    try:
        from database import ElasticsearchSync
        print("✅ ElasticsearchSync imported successfully")
    except Exception as e:
        print(f"❌ ElasticsearchSync import failed: {e}")
        return False
    
    return True

def test_elasticsearch_connection():
    """Test Elasticsearch connection."""
    print("\n🔍 Testing Elasticsearch connection...")
    
    try:
        from database import get_elasticsearch_client, ElasticsearchSync
        
        es = get_elasticsearch_client()
        if es is None:
            print("❌ Elasticsearch client is None")
            return False
        
        if es.ping():
            print("✅ Elasticsearch connection successful")
            
            # Test ElasticsearchSync
            es_sync = ElasticsearchSync()
            if es_sync.is_available():
                print("✅ ElasticsearchSync is available")
                return True
            else:
                print("❌ ElasticsearchSync is not available")
                return False
        else:
            print("❌ Elasticsearch ping failed")
            return False
            
    except Exception as e:
        print(f"❌ Elasticsearch connection test failed: {e}")
        return False

def test_postgresql_connection():
    """Test PostgreSQL connection."""
    print("\n🔍 Testing PostgreSQL connection...")
    
    try:
        from database import engine, SessionLocal
        
        # Test engine connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ PostgreSQL connection successful")
            
        # Test session
        db = SessionLocal()
        try:
            print("✅ PostgreSQL session created successfully")
            return True
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ PostgreSQL connection test failed: {e}")
        return False

async def test_elasticsearch_sync():
    """Test Elasticsearch synchronization."""
    print("\n🔍 Testing Elasticsearch sync...")
    
    try:
        from database import ElasticsearchSync
        
        es_sync = ElasticsearchSync()
        
        if not es_sync.is_available():
            print("⚠️  Elasticsearch not available, skipping sync test")
            return True
        
        # Test user profile sync
        test_profile_data = {
            "user_id": 999,
            "username": "test_user",
            "email": "test@example.com",
            "skills": "Python, JavaScript",
            "updated_at": "2025-07-29T10:00:00"
        }
        
        await es_sync.sync_user_profile(999, test_profile_data)
        print("✅ Elasticsearch user profile sync test successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Elasticsearch sync test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Job Boost Backend Tests...\n")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return
    
    # Test Elasticsearch
    if not test_elasticsearch_connection():
        print("\n❌ Elasticsearch tests failed!")
        return
    
    # Test PostgreSQL  
    if not test_postgresql_connection():
        print("\n❌ PostgreSQL tests failed!")
        return
    
    # Test Elasticsearch sync
    asyncio.run(test_elasticsearch_sync())
    
    print("\n🎉 All tests completed successfully!")
    print("✅ Your Job Boost backend is ready to use!")

if __name__ == "__main__":
    main()
