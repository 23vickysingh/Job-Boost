import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import random
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Set up CSV file with additional columns
with open('linkedin_jobs.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Company', 'Location', 'Date', 'Experience Level', 
                    'Job Type', 'Job Link', 'Description'])

# Configure headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def get_job_description(job_link):
    """Fetch job description from individual job page"""
    try:
        response = requests.get(job_link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            description_div = soup.find('div', class_='description__text')
            if description_div:
                return description_div.get_text(separator='\n', strip=True)
        return "Description not available"
    except Exception as e:
        print(f"Error fetching description for {job_link}: {e}")
        return "Description not available"

def scrape_linkedin_jobs(keyword, location, experience=None, job_type=None, city_level=False):
    """
    Scrape LinkedIn jobs with advanced filters
    
    Parameters:
    - keyword: Job title/search term
    - location: Country/region/city
    - experience: 'internship', 'entry', 'associate', 'mid-senior', 'director', 'executive'
    - job_type: 'full-time', 'part-time', 'contract', 'temporary', 'volunteer', 'internship'
    - city_level: Boolean for precise city-level location matching
    """
    base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
    start = 0
    results = []
    
    while True:
        params = {
            'keywords': keyword,
            'location': location,
            'start': start,
            'f_TPR': 'r86400',  # Last 24 hours
        }
        
        # Add experience filter if specified
        if experience:
            experience_map = {
                'internship': '1',
                'entry': '2',
                'associate': '3',
                'mid-senior': '4',
                'director': '5',
                'executive': '6'
            }
            params['f_E'] = experience_map.get(experience.lower(), '')
        
        # Add job type filter if specified
        if job_type:
            job_type_map = {
                'full-time': 'F',
                'part-time': 'P',
                'contract': 'C',
                'temporary': 'T',
                'volunteer': 'V',
                'internship': 'I'
            }
            params['f_JT'] = job_type_map.get(job_type.lower(), '')
        
        # Enable city-level location matching
        if city_level:
            params['f_PP'] = '102571732'  # Magic number for city-level precision
        
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f'Failed to retrieve page {start//25 + 1} (Status: {response.status_code})')
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('div', class_='base-card')
        
        if not jobs:
            print("No more jobs found")
            break
            
        for job in jobs:
            try:
                title = job.find('h3', class_='base-search-card__title').text.strip()
                company = job.find('h4', class_='base-search-card__subtitle').text.strip()
                location = job.find('span', class_='job-search-card__location').text.strip()
                
                # Handle date (multiple possible classes)
                date_elem = (job.find('time', class_='job-search-card__listdate') or 
                            job.find('time', class_='job-search-card__listdate--new'))
                date = date_elem['datetime'] if date_elem else 'N/A'
                
                # Get job link
                job_link = job.find('a', class_='base-card__full-link')['href']
                
                # Clean job link (remove tracking parameters)
                parsed = urlparse(job_link)
                clean_link = urlunparse(parsed._replace(query=''))
                
                # Get experience level and job type from the job card
                metadata = job.find('div', class_='metadata')
                experience_level = 'Not specified'
                employment_type = 'Not specified'
                
                if metadata:
                    items = metadata.find_all('li')
                    if len(items) >= 1:
                        employment_type = items[0].get_text(strip=True)
                    if len(items) >= 2:
                        experience_level = items[1].get_text(strip=True)
                
                # Fetch job description
                description = get_job_description(clean_link)
                
                results.append([
                    title, 
                    company, 
                    location, 
                    date, 
                    experience_level, 
                    employment_type, 
                    clean_link, 
                    description
                ])
                
                # Random delay between 1-3 seconds to avoid rate limiting
                sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Skipping a job due to error: {str(e)}")
                continue
            
        print(f'Scraped page {start//25 + 1} with {len(jobs)} jobs')
        start += 25
        
        # Random delay between pages
        sleep(random.uniform(2, 5))
        
    # Write to CSV
    with open('linkedin_jobs.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(results)
        
    print(f'Scraping complete. Saved {len(results)} jobs to linkedin_jobs.csv')

# Example usage with all parameters
scrape_linkedin_jobs(
    keyword='Python Developer',
    location='Banglore, India',  # More precise location
    experience='mid-senior',              # Experience level filter
    job_type='full-time'               # Job type filter
)