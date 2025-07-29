#!/usr/bin/env python3
"""
Simple test to verify database connectivity and initialize tables.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test environment variables."""
    print("🔍 Checking environment variables...")
    
    postgres_url = os.getenv('POSTGRES_DATABASE_URL')
    es_host = os.getenv('ELASTICSEARCH_HOST')
    es_api_key = os.getenv('ELASTICSEARCH_API_KEY')
    
    print(f"POSTGRES_DATABASE_URL: {postgres_url}")
    print(f"ELASTICSEARCH_HOST: {es_host}")
    print(f"ELASTICSEARCH_API_KEY: {'***set***' if es_api_key else 'NOT SET'}")
    
    return postgres_url is not None

def test_postgresql():
    """Test PostgreSQL connection."""
    print("\n🔍 Testing PostgreSQL connection...")
    
    try:
        from sqlalchemy import create_engine, text
        
        postgres_url = os.getenv('POSTGRES_DATABASE_URL')
        if not postgres_url:
            print("❌ POSTGRES_DATABASE_URL not set")
            return False
        
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ PostgreSQL connected successfully!")
            print(f"   Version: {version}")
            return True
            
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_elasticsearch():
    """Test Elasticsearch connection."""
    print("\n🔍 Testing Elasticsearch connection...")
    
    try:
        from elasticsearch import Elasticsearch
        
        es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost:9200')
        es_api_key = os.getenv('ELASTICSEARCH_API_KEY')
        
        if es_api_key:
            es = Elasticsearch(
                [f"http://{es_host}"],
                api_key=es_api_key
            )
        else:
            es = Elasticsearch([f"http://{es_host}"])
        
        if es.ping():
            info = es.info()
            print(f"✅ Elasticsearch connected successfully!")
            print(f"   Version: {info['version']['number']}")
            print(f"   Cluster: {info['cluster_name']}")
            return True
        else:
            print("❌ Elasticsearch ping failed")
            return False
            
    except Exception as e:
        print(f"❌ Elasticsearch connection failed: {e}")
        return False

def create_tables():
    """Create database tables."""
    print("\n🔍 Creating database tables...")
    
    try:
        from database import engine, Base
        import models  # Import models to register them
        
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting connectivity tests...\n")
    
    # Test environment
    if not test_environment():
        print("\n❌ Environment test failed!")
        return
    
    # Test PostgreSQL
    postgres_ok = test_postgresql()
    
    # Test Elasticsearch
    elasticsearch_ok = test_elasticsearch()
    
    # Create tables if PostgreSQL is working
    if postgres_ok:
        create_tables()
    
    print(f"\n📊 Test Results:")
    print(f"   PostgreSQL: {'✅ OK' if postgres_ok else '❌ FAILED'}")
    print(f"   Elasticsearch: {'✅ OK' if elasticsearch_ok else '❌ FAILED'}")
    
    if postgres_ok and elasticsearch_ok:
        print("\n🎉 All systems operational!")
    else:
        print("\n⚠️  Some systems need attention")

if __name__ == "__main__":
    main()
