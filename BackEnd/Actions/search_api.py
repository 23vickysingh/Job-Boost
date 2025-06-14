import requests
from bs4 import BeautifulSoup
import pandas as pd

##################                   linkedin scrapper

def scrape_linkedin_jobs(keyword, experience, location):
    base_url = "https://in.linkedin.com/jobs/search/"
    params = {
        "keywords": keyword,
        "f_E": experience,  # 2=Entry, 3=Associate, 4=Mid-Senior
        "location": location,
        "f_TPR": "r86400"  # Last 24 hours
    }
    
    response = requests.get(base_url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    jobs = []
    for job_card in soup.select('.base-card'):
        title = job_card.select_one('h3').get_text(strip=True)
        company = job_card.select_one('.base-search-card__subtitle').get_text(strip=True)
        location = job_card.select_one('.job-search-card__location').get_text(strip=True)
        posted = job_card.select_one('time').get('datetime')
        link = job_card.find('a', class_='base-card__full-link')['href']
        
        jobs.append({
            'platform': 'LinkedIn',
            'title': title,
            'company': company,
            'location': location,
            'posted': posted,
            'link': link
        })
    
    return pd.DataFrame(jobs)

# print(scrape_linkedin_jobs("software engineer", 2, "Banglore"))




############################                  glassdoor scrapper

def scrape_glassdoor_jobs(position, experience, city):
    url = f"https://www.glassdoor.com/Job/{city}-{position}-jobs-SRCH_KO0,14_IC1138212_KE15,24.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_listings = []
    for job in soup.select('[data-test="jobListing"]'):
        title = job.select_one('[data-test="job-title"]').text.strip()
        company = job.select_one('[data-test="employer-name"]').text.strip()
        location = job.select_one('[data-test="location"]').text.strip()
        salary = job.select_one('[data-test="detailSalary"]').text.strip() if job.select_one('[data-test="detailSalary"]') else 'N/A'
        
        job_listings.append({
            'platform': 'Glassdoor',
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'experience': experience
        })
    
    return pd.DataFrame(job_listings)









######################                      dynamic parameter handling

# Experience level mapping
EXPERIENCE_MAP = {
    'entry': 2,
    'mid': 3,
    'senior': 4
}

# Location normalization
def normalize_location(location):
    return location.lower().replace(' ', '-')








######################                            driver code

if __name__ == "__main__":
    search_params = {
        'keyword': 'Software Engineer',
        'experience': EXPERIENCE_MAP['entry'],
        'location': normalize_location('Banglore')
    }

    linkedin_df = scrape_linkedin_jobs(**search_params)
    glassdoor_df = scrape_glassdoor_jobs(
        position=search_params['keyword'],
        experience=search_params['experience'],
        city=search_params['location']
    )
    
    combined_jobs = pd.concat([linkedin_df, glassdoor_df])
    combined_jobs.to_csv('job_listings.csv', index=False)
