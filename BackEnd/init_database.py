"""
Database initialization script for Job-Boost application.
This script creates PostgreSQL tables and Elasticsearch indices.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base, get_elasticsearch_client
from elasticsearch_config import initialize_elasticsearch_indices
import models

def create_database_tables():
    """Create all PostgreSQL tables."""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ PostgreSQL tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating PostgreSQL tables: {e}")

def create_elasticsearch_indices():
    """Create all Elasticsearch indices."""
    try:
        initialize_elasticsearch_indices()
        print("✅ Elasticsearch indices created successfully!")
    except Exception as e:
        print(f"❌ Error creating Elasticsearch indices: {e}")

def main():
    print("🚀 Initializing Job-Boost database...")
    
    # Create PostgreSQL tables
    print("\n📊 Creating PostgreSQL tables...")
    create_database_tables()
    
    # Create Elasticsearch indices
    print("\n🔍 Creating Elasticsearch indices...")
    create_elasticsearch_indices()
    
    print("\n✨ Database initialization complete!")

if __name__ == "__main__":
    main()
