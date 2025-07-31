from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
# from elasticsearch import Elasticsearch  # DISABLED - Elasticsearch not in use
import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL Database Configuration
POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")

# Elasticsearch Configuration - DISABLED FOR NOW
# ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost:9200")
# ELASTICSEARCH_API_KEY = os.getenv("ELASTICSEARCH_API_KEY", "")

# Create SQLAlchemy engine for PostgreSQL
if POSTGRES_DATABASE_URL:
    engine = create_engine(POSTGRES_DATABASE_URL, echo=False)
else:
    print("⚠️ Warning: POSTGRES_DATABASE_URL not set, using fallback")
    engine = create_engine("postgresql://user:password@localhost:5432/job_boost_db", echo=False)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models - using modern SQLAlchemy 2.0+ approach
class Base(DeclarativeBase):
    pass

# Elasticsearch client setup - DISABLED FOR NOW
# def get_elasticsearch_client():
#     """Create and return Elasticsearch client with API key authentication."""
#     try:
#         if ELASTICSEARCH_API_KEY:
#             # Use API key authentication (recommended for production)
#             es = Elasticsearch(
#                 [f"http://{ELASTICSEARCH_HOST}"],
#                 api_key=ELASTICSEARCH_API_KEY,
#                 verify_certs=False
#             )
#         else:
#             # For local development without authentication
#             es = Elasticsearch([f"http://{ELASTICSEARCH_HOST}"])
#         
#         # Test the connection
#         if not es.ping():
#             print("⚠️  Warning: Could not connect to Elasticsearch")
#             return None
#             
#         return es
#     except Exception as e:
#         print(f"⚠️  Warning: Elasticsearch connection failed: {e}")
#         return None

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ELASTICSEARCH FUNCTIONALITY DISABLED FOR NOW
# class ElasticsearchSync:
#     """Handle synchronization between PostgreSQL and Elasticsearch."""
#     
#     def __init__(self):
#         self.es = get_elasticsearch_client()
#     
#     def is_available(self) -> bool:
#         """Check if Elasticsearch is available."""
#         return self.es is not None
#     
#     def create_index_if_not_exists(self, index_name: str, mapping: Dict[str, Any]):
#         """Create Elasticsearch index if it doesn't exist."""
#         if not self.is_available():
#             print(f"⚠️  Elasticsearch not available, skipping index creation for {index_name}")
#             return
#             
#         try:
#             if not self.es.indices.exists(index=index_name):
#                 self.es.indices.create(index=index_name, body=mapping)
#                 print(f"✅ Created Elasticsearch index: {index_name}")
#         except Exception as e:
#             print(f"❌ Error creating index {index_name}: {e}")
#     
#     async def sync_user_profile(self, user_id: int, profile_data: Dict[str, Any]):
#         """Sync user profile data to Elasticsearch."""
#         if not self.is_available():
#             print("⚠️  Elasticsearch not available, skipping profile sync")
#             return
#             
#         try:
#             doc_body = {
#                 "user_id": user_id,
#                 "timestamp": profile_data.get("updated_at"),
#                 **profile_data
#             }
#             self.es.index(
#                 index="user_profiles",
#                 id=user_id,
#                 body=doc_body
#             )
#             print(f"Synced user profile {user_id} to Elasticsearch")
#         except Exception as e:
#             print(f"Error syncing user profile {user_id}: {e}")
#     
#     async def sync_resume_data(self, user_id: int, resume_data: Dict[str, Any]):
#         """Sync parsed resume data to Elasticsearch for search."""
#         if not self.is_available():
#             print("⚠️  Elasticsearch not available, skipping resume sync")
#             return
#             
#         try:
#             doc_body = {
#                 "user_id": user_id,
#                 "timestamp": resume_data.get("updated_at"),
#                 "searchable_content": {
#                     "skills": resume_data.get("skills", ""),
#                     "experience": resume_data.get("experiences", ""),
#                     "education": resume_data.get("education", ""),
#                     "projects": resume_data.get("projects", "")
#                 },
#                 "parsed_json": resume_data.get("resume_data", "")
#             }
#             self.es.index(
#                 index="resumes",
#                 id=user_id,
#                 body=doc_body
#             )
#             print(f"✅ Synced resume data for user {user_id} to Elasticsearch")
#         except Exception as e:
#             print(f"❌ Error syncing resume data for user {user_id}: {e}")
#     
#     async def search_profiles(self, query: str, filters: Optional[Dict] = None) -> Dict:
#         """Search user profiles and resumes."""
#         if not self.is_available():
#             print("⚠️  Elasticsearch not available, returning empty search results")
#             return {"hits": {"hits": []}}
#             
#         try:
#             search_body = {
#                 "query": {
#                     "multi_match": {
#                         "query": query,
#                         "fields": [
#                             "searchable_content.skills^3",
#                             "searchable_content.experience^2",
#                             "searchable_content.education",
#                             "searchable_content.projects"
#                         ]
#                     }
#                 }
#             }
#             
#             if filters:
#                 search_body["query"] = {
#                     "bool": {
#                         "must": [search_body["query"]],
#                         "filter": filters
#                     }
#                 }
#             
#             result = self.es.search(index="resumes", body=search_body)
#             return result
#         except Exception as e:
#             print(f"❌ Error searching profiles: {e}")
#             return {"hits": {"hits": []}}

# Global Elasticsearch sync instance - DISABLED FOR NOW
# es_sync = ElasticsearchSync()
