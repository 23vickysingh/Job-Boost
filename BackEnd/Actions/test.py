import requests
from bs4 import BeautifulSoup

def scrape_glassdoor_jobs(position, experience, city):
    url = f"https://www.glassdoor.com/Job/bengaluru-india-software-engineer-jobs-SRCH_KO0,14_IC1138212_KE15,24.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # return soup

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
    
    return job_listings

print(scrape_glassdoor_jobs("software engineer", 2, "Banglore"))
