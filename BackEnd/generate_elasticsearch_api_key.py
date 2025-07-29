#!/usr/bin/env python3
"""
Script to generate Elasticsearch API key for authentication.

This script will:
1. Connect to Elasticsearch using basic auth (elastic:changeme)
2. Create an API key for the application
3. Display the API key that you can add to your .env file

Usage:
    python generate_elasticsearch_api_key.py
"""

from elasticsearch import Elasticsearch
import base64
import json

def generate_api_key():
    """Generate an API key for Elasticsearch authentication."""
    
    # Connect to Elasticsearch using basic auth
    es = Elasticsearch(
        ["http://localhost:9200"],
        basic_auth=("elastic", "changeme"),
        verify_certs=False
    )
    
    try:
        # Check if Elasticsearch is available
        if not es.ping():
            print("❌ Could not connect to Elasticsearch. Make sure it's running.")
            return
        
        print("✅ Connected to Elasticsearch successfully!")
        
        # Create an API key
        api_key_response = es.security.create_api_key(
            body={
                "name": "job-boost-backend",
                "role_descriptors": {
                    "job_boost_role": {
                        "cluster": ["monitor", "manage"],
                        "indices": [
                            {
                                "names": ["user_profiles", "resumes", "*"],
                                "privileges": ["all"]
                            }
                        ]
                    }
                }
            }
        )
        
        # Extract API key details
        api_key_id = api_key_response["id"]
        api_key_secret = api_key_response["api_key"]
        
        # Create the base64 encoded API key
        api_key_credentials = f"{api_key_id}:{api_key_secret}"
        encoded_api_key = base64.b64encode(api_key_credentials.encode()).decode()
        
        print("\n🔑 API Key generated successfully!")
        print("=" * 50)
        print(f"API Key ID: {api_key_id}")
        print(f"API Key Secret: {api_key_secret}")
        print(f"Encoded API Key: {encoded_api_key}")
        print("=" * 50)
        print("\n📝 Add this to your .env file:")
        print(f"ELASTICSEARCH_API_KEY={encoded_api_key}")
        print("\n⚠️  IMPORTANT: Save this API key securely. You won't be able to retrieve the secret again!")
        
    except Exception as e:
        print(f"❌ Error generating API key: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Elasticsearch is running: docker-compose up elasticsearch")
        print("2. Wait for Elasticsearch to be fully ready (check the logs)")
        print("3. Ensure xpack.security.enabled=true in docker-compose.yml")

if __name__ == "__main__":
    print("🚀 Generating Elasticsearch API Key...")
    generate_api_key()
