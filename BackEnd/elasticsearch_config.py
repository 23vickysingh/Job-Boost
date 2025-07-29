"""
Elasticsearch index mappings and initialization.
"""

from database import es_sync

# User Profiles Index Mapping
USER_PROFILES_MAPPING = {
    "mappings": {
        "properties": {
            "user_id": {"type": "integer"},
            "timestamp": {"type": "date"},
            "experiences": {"type": "text", "analyzer": "standard"},
            "skills": {"type": "text", "analyzer": "standard"},
            "projects": {"type": "text", "analyzer": "standard"},
            "education": {"type": "text", "analyzer": "standard"},
            "courses": {"type": "text", "analyzer": "standard"},
            "achievements": {"type": "text", "analyzer": "standard"},
            "extra_curricular": {"type": "text", "analyzer": "standard"},
            "resume_filename": {"type": "keyword"},
        }
    }
}

# Resumes Index Mapping (for search)
RESUMES_MAPPING = {
    "mappings": {
        "properties": {
            "user_id": {"type": "integer"},
            "timestamp": {"type": "date"},
            "searchable_content": {
                "properties": {
                    "skills": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    },
                    "experience": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "education": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "projects": {
                        "type": "text",
                        "analyzer": "standard"
                    }
                }
            },
            "parsed_json": {"type": "text"}
        }
    }
}

def initialize_elasticsearch_indices():
    """Initialize Elasticsearch indices with proper mappings."""
    try:
        # Create user profiles index
        es_sync.create_index_if_not_exists("user_profiles", USER_PROFILES_MAPPING)
        
        # Create resumes index for search
        es_sync.create_index_if_not_exists("resumes", RESUMES_MAPPING)
        
        print("Elasticsearch indices initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing Elasticsearch indices: {e}")
        return False
