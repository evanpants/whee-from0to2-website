"""
Real job data sources that provide actual job postings with real URLs.
These require proper setup for legitimate access.
"""
import requests
import logging
import json
from typing import List, Dict, Optional
from datetime import datetime
import time

logger = logging.getLogger(__name__)

class RealJobSources:
    """Access real job data from legitimate sources."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def search_github_jobs(self, keywords: str, location: str = "New York, NY", limit: int = 30) -> List[Dict]:
        """
        GitHub Jobs API - provides real job listings.
        Note: GitHub Jobs API was deprecated but some alternatives exist.
        """
        try:
            # GitHub Jobs API was deprecated, but we can try the redirect
            url = "https://jobs.github.com/positions.json"
            
            params = {
                'description': keywords,
                'location': location,
                'full_time': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_github_jobs_results(data)
            else:
                logger.warning(f"GitHub Jobs API responded with {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with GitHub Jobs: {e}")
            return []
    
    def search_remoteok(self, keywords: str, limit: int = 30) -> List[Dict]:
        """
        RemoteOK API - provides real remote job listings.
        Free API, no authentication required.
        """
        try:
            url = "https://remoteok.io/api"
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                # The first line is usually a comment, skip it
                data = response.text.strip()
                if data.startswith('//'):
                    # Remove the comment line
                    data = '\n'.join(data.split('\n')[1:])
                
                try:
                    jobs_data = json.loads(data)
                    return self._parse_remoteok_results(jobs_data, keywords, limit)
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing RemoteOK JSON: {e}")
                    return []
            else:
                logger.error(f"RemoteOK API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with RemoteOK: {e}")
            return []
    
    def search_jobspresso(self, keywords: str, limit: int = 30) -> List[Dict]:
        """
        JobsPresso API - real remote job listings.
        """
        try:
            url = "https://jobspresso.co/api/jobs"
            
            params = {
                'search': keywords,
                'remote': '1',
                'limit': min(limit, 50)
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_jobspresso_results(data)
            else:
                logger.error(f"JobsPresso API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with JobsPresso: {e}")
            return []
    
    def search_with_serpapi_real(self, api_key: str, keywords: str, location: str, limit: int = 30) -> List[Dict]:
        """
        Use SerpAPI to get real Google Jobs results (includes actual LinkedIn jobs).
        Requires a real API key from https://serpapi.com/
        """
        try:
            url = "https://serpapi.com/search"
            
            params = {
                'api_key': api_key,
                'engine': 'google_jobs',
                'q': f'{keywords} {location}',
                'location': location,
                'chips': 'min_salary:USD180000',
                'num': min(limit, 10)
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_serpapi_real_results(data)
            else:
                logger.error(f"SerpAPI error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error with SerpAPI: {e}")
            return []
    
    def _parse_github_jobs_results(self, data: List[dict]) -> List[Dict]:
        """Parse GitHub Jobs API results."""
        jobs = []
        
        for job_data in data:
            job = {
                'title': job_data.get('title', ''),
                'company': job_data.get('company', ''),
                'location': job_data.get('location', ''),
                'salary': 'Not specified',  # GitHub Jobs doesn't usually include salary
                'description': job_data.get('description', '')[:500],
                'url': job_data.get('url', ''),
                'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_time': datetime.now().strftime('%H:%M:%S'),
                'source': 'GitHub Jobs'
            }
            
            if self._is_hardware_manager_job(job):
                jobs.append(job)
        
        return jobs
    
    def _parse_remoteok_results(self, data: List[dict], keywords: str, limit: int) -> List[Dict]:
        """Parse RemoteOK API results."""
        jobs = []
        
        for job_data in data[:limit * 2]:  # Get more to filter
            if not isinstance(job_data, dict) or not job_data.get('position'):
                continue
            
            # Check if it matches our criteria
            position = job_data.get('position', '').lower()
            description = job_data.get('description', '').lower()
            
            if 'hardware' in position and 'manager' in position:
                job = {
                    'title': job_data.get('position', ''),
                    'company': job_data.get('company', ''),
                    'location': 'Remote',  # RemoteOK is for remote jobs
                    'salary': job_data.get('salary', 'Not specified'),
                    'description': job_data.get('description', '')[:500],
                    'url': job_data.get('url', ''),
                    'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                    'scraped_time': datetime.now().strftime('%H:%M:%S'),
                    'source': 'RemoteOK'
                }
                jobs.append(job)
        
        return jobs[:limit]
    
    def _parse_jobspresso_results(self, data: dict) -> List[Dict]:
        """Parse JobsPresso API results."""
        jobs = []
        
        for job_data in data.get('jobs', []):
            job = {
                'title': job_data.get('title', ''),
                'company': job_data.get('company', ''),
                'location': 'Remote',  # JobsPresso focuses on remote
                'salary': job_data.get('salary', 'Not specified'),
                'description': job_data.get('description', '')[:500],
                'url': job_data.get('url', ''),
                'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_time': datetime.now().strftime('%H:%M:%S'),
                'source': 'JobsPresso'
            }
            
            if self._is_hardware_manager_job(job):
                jobs.append(job)
        
        return jobs
    
    def _parse_serpapi_real_results(self, data: dict) -> List[Dict]:
        """Parse SerpAPI Google Jobs results with real data."""
        jobs = []
        
        for job_data in data.get('jobs_results', []):
            job = {
                'title': job_data.get('title', ''),
                'company': job_data.get('company_name', ''),
                'location': job_data.get('location', ''),
                'salary': job_data.get('salary', {}).get('salary_text', 'Not specified') if job_data.get('salary') else 'Not specified',
                'description': job_data.get('description', '')[:500],
                'url': job_data.get('apply_options', [{}])[0].get('link', '') if job_data.get('apply_options') else '',
                'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_time': datetime.now().strftime('%H:%M:%S'),
                'source': 'SerpAPI (Google Jobs)'
            }
            
            if self._is_hardware_manager_job(job) and self._is_ny_location(job):
                jobs.append(job)
        
        return jobs
    
    def _is_hardware_manager_job(self, job: Dict) -> bool:
        """Check if job is hardware manager related."""
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        
        hardware_keywords = ['hardware', 'engineering manager', 'product manager', 'technical manager']
        manager_keywords = ['manager', 'director', 'lead', 'head']
        
        has_hardware = any(keyword in title or keyword in description for keyword in hardware_keywords)
        has_manager = any(keyword in title or keyword in description for keyword in manager_keywords)
        
        return has_hardware and has_manager
    
    def _is_ny_location(self, job: Dict) -> bool:
        """Check if job is in New York area."""
        location = job.get('location', '').lower()
        ny_keywords = ['new york', 'ny', 'nyc', 'queens', 'brooklyn', 'manhattan', 'bronx', 'staten island']
        return any(keyword in location for keyword in ny_keywords)

def test_real_sources():
    """Test the real job sources."""
    scraper = RealJobSources()
    
    print("Testing RemoteOK API...")
    remoteok_jobs = scraper.search_remoteok("hardware manager", 5)
    print(f"Found {len(remoteok_jobs)} jobs from RemoteOK")
    
    for job in remoteok_jobs[:2]:
        print(f"- {job['title']} at {job['company']}")
        print(f"  URL: {job['url']}")
        print(f"  Source: {job['source']}")
        print()

if __name__ == "__main__":
    test_real_sources()




