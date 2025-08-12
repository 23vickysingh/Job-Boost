import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

import models

# Load environment variables from the .env file
load_dotenv()

# Retrieve the JSearch API key and define the API endpoint
JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY")
JSEARCH_API_URL = "https://jsearch.p.rapidapi.com/search"

class JSearchAPIError(Exception):
    """Custom exception for JSearch API errors."""
    pass

def fetch_jobs_from_api(user_profile: models.UserProfile) -> List[Dict[str, Any]]:
    """
    Fetches job listings from the JSearch API based on user profile preferences.

    Args:
        user_profile: The SQLAlchemy UserProfile object containing job preferences.

    Returns:
        A list of job dictionaries from the API response.

    Raises:
        JSearchAPIError: If the API key is missing or the request fails.
    """
    if not JSEARCH_API_KEY:
        print("ERROR: JSEARCH_API_KEY not found in environment variables.")
        raise JSearchAPIError("JSearch API key is not configured.")

    # Construct the query parameters from the user's profile
    # The 'query' parameter is a combination of the job title and location for best results.
    query = f"{user_profile.query} in {user_profile.location}"
    
    params = {
        "query": query,
        "num_pages": "1" # Fetch one page of results (up to 10 jobs) per run
    }
    
    # Add employment types if they exist, formatted as a comma-separated string
    if user_profile.employment_types:
        params["employment_types"] = ",".join(user_profile.employment_types).upper()

    # Set the required headers for the RapidAPI endpoint
    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        print(f"Fetching jobs for query: {query}")
        response = requests.get(JSEARCH_API_URL, headers=headers, params=params)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        data = response.json()

        # The actual job listings are in the 'data' key of the response
        if 'data' in data and data['data']:
            return data['data']
        else:
            print(f"No jobs found for query: {query}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to connect to JSearch API. {e}")
        raise JSearchAPIError(f"An error occurred while contacting the JSearch API: {e}")
    except KeyError:
        print(f"ERROR: Unexpected API response format. 'data' key not found.")
        raise JSearchAPIError("Received an unexpected response format from JSearch API.")