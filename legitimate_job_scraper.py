"""
Legitimate job data sources that aggregate LinkedIn and other job board data.
These APIs are designed for legitimate use and don't violate terms of service.
"""
import requests
import logging
import os
from typing import List, Dict, Optional
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class LegitimateJobScraper:
    """Use legitimate job APIs that aggregate data from multiple sources including LinkedIn."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        # Initialize real job sources
        try:
            from real_job_sources import RealJobSources
            self.real_sources = RealJobSources()
        except ImportError:
            self.real_sources = None
            logger.warning("Real job sources module not available")
    
    def search_with_adzuna(self, keywords: str, location: str = "new-york-ny", limit: int = 30) -> List[Dict]:
        """
        Use Adzuna API - aggregates jobs from multiple sources including LinkedIn.
        Free tier available: https://adzuna.com/landing
        
        Note: You need to sign up for a free API key at adzuna.com
        """
        try:
            # Get API credentials from environment variables
            api_key = os.getenv('ADZUNA_APP_KEY') or "YOUR_ADZUNA_API_KEY"
            app_id = os.getenv('ADZUNA_APP_ID') or "YOUR_ADZUNA_APP_ID"
            
            if api_key == "YOUR_ADZUNA_API_KEY" or app_id == "YOUR_ADZUNA_APP_ID":
                logger.warning("Adzuna API credentials not configured. Please set ADZUNA_APP_KEY and ADZUNA_APP_ID in .env file")
                return []
            
            url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
            
            params = {
                'app_id': app_id,
                'app_key': api_key,
                'what': keywords,
                'where': location,
                'results_per_page': min(limit, 50),
                'salary_min': '180000',  # Our minimum salary requirement
                'content-type': 'application/json'
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_adzuna_results(data)
            else:
                logger.error(f"Adzuna API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with Adzuna API: {e}")
            return []
    
    def search_with_jobapi(self, keywords: str, location: str = "New York, NY", limit: int = 30) -> List[Dict]:
        """
        Use JobAPI - another legitimate job aggregator.
        Free tier available with limitations.
        
        Sign up at: https://www.reed.co.uk/developers/jobseeker
        """
        try:
            # You'll need to get a free API key
            api_key = "YOUR_JOBAPI_KEY"  # Get from job aggregator services
            
            url = "https://www.reed.co.uk/api/1.0/search"
            
            headers = {
                'Authorization': f'Basic {api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'keywords': keywords,
                'locationName': location,
                'resultsToTake': min(limit, 100),
                'minimumSalary': '180000'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_jobapi_results(data)
            else:
                logger.error(f"JobAPI error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with JobAPI: {e}")
            return []
    
    def search_with_welcometothejungle(self, keywords: str, location: str = "new-york", limit: int = 30) -> List[Dict]:
        """
        Use Welcome to the Jungle - aggregates jobs from top tech companies.
        This requires proper API access or web scraping their public job listings.
        """
        try:
            logger.info("Welcome to the Jungle: Attempting to access real job data...")
            
            # Try different possible API endpoints
            possible_endpoints = [
                "https://api.welcometothejungle.com/api/v2/jobs",
                "https://www.welcometothejungle.com/api/v2/jobs",
                "https://welcometothejungle.com/api/v2/jobs"
            ]
            
            params = {
                'what': keywords,
                'where': location,
                'per_page': min(limit, 100),
                'lang': 'en'
            }
            
            for endpoint in possible_endpoints:
                try:
                    response = requests.get(endpoint, params=params, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        logger.info(f"Successfully accessed Welcome to the Jungle API at {endpoint}")
                        return self._parse_wttj_results(data)
                except:
                    continue
            
            logger.warning("Welcome to the Jungle API not accessible - may need authentication or different endpoint")
            return []
                
        except Exception as e:
            logger.error(f"Error with Welcome to the Jungle: {e}")
            return []
    
    def search_with_indeed_api(self, keywords: str, location: str = "New York, NY", limit: int = 30) -> List[Dict]:
        """
        Use Indeed's official job search API.
        Requires API key registration at: https://ads.indeed.com/jobroll/xmlfeed
        """
        try:
            # You'll need to register for Indeed's Partner API
            publisher_id = "YOUR_INDEED_PUBLISHER_ID"
            
            url = "https://api.indeed.com/ads/apisearch"
            
            params = {
                'publisher': publisher_id,
                'q': keywords,
                'l': location,
                'radius': '25',
                'st': 'employer',
                'jk': '',
                'sort': 'date',
                'fromage': '',
                'limit': min(limit, 25),  # Indeed API limit
                'format': 'json',
                'latlong': '1',
                'co': 'us'
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_indeed_results(data)
            else:
                logger.error(f"Indeed API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with Indeed API: {e}")
            return []
    
    def search_with_serpapi(self, keywords: str, location: str = "New York, NY", limit: int = 30) -> List[Dict]:
        """
        Use SerpAPI to search Google Jobs results (which include LinkedIn jobs).
        This is legitimate and widely used.
        
        Get free credits at: https://serpapi.com/
        """
        try:
            api_key = os.getenv('SERPAPI_KEY') or "YOUR_SERPAPI_KEY"  # Get from .env or https://serpapi.com/
            
            if api_key == "YOUR_SERPAPI_KEY":
                logger.warning("SerpAPI key not configured. Please set SERPAPI_KEY in .env file")
                return []
            
            url = "https://serpapi.com/search"
            
            params = {
                'api_key': api_key,
                'engine': 'google_jobs',
                'q': f'{keywords} {location}',
                'location': location,
                'chips': 'min_salary:USD180000',
                'num': min(limit, 10)  # SerpAPI free tier limits
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_serpapi_results(data)
            else:
                logger.error(f"SerpAPI error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with SerpAPI: {e}")
            return []
    
    def _parse_adzuna_results(self, data: dict) -> List[Dict]:
        """Parse Adzuna API results."""
        jobs = []
        
        for job_data in data.get('results', []):
            job = {
                'title': job_data.get('title', ''),
                'company': job_data.get('company', {}).get('display_name', ''),
                'location': job_data.get('location', {}).get('display_name', ''),
                'salary': f"${job_data.get('salary_min', '')} - ${job_data.get('salary_max', '')}" if job_data.get('salary_min') else "Not specified",
                'description': job_data.get('description', '')[:500],  # Truncate
                'url': job_data.get('redirect_url', ''),
                'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_time': datetime.now().strftime('%H:%M:%S')
            }
            
            # Filter for hardware manager positions
            if self._is_hardware_manager_job(job):
                jobs.append(job)
        
        return jobs
    
    def _parse_jobapi_results(self, data: dict) -> List[Dict]:
        """Parse JobAPI results."""
        jobs = []
        
        for job_data in data.get('results', []):
            job = {
                'title': job_data.get('jobTitle', ''),
                'company': job_data.get('employerName', ''),
                'location': job_data.get('locationName', ''),
                'salary': f"{job_data.get('minimumSalary', '')} - {job_data.get('maximumSalary', '')}" if job_data.get('minimumSalary') else "Not specified",
                'description': job_data.get('jobDescription', '')[:500],
                'url': job_data.get('jobUrl', ''),
                'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_time': datetime.now().strftime('%H:%M:%S')
            }
            
            if self._is_hardware_manager_job(job):
                jobs.append(job)
        
        return jobs
    
    def _parse_wttj_results(self, data: dict) -> List[Dict]:
        """Parse Welcome to the Jungle API results."""
        jobs = []
        
        for job_data in data.get('jobs', []):
            company_info = job_data.get('organization', {})
            location_info = job_data.get('place', {})
            
            job = {
                'title': job_data.get('name', ''),
                'company': company_info.get('name', ''),
                'location': location_info.get('city', '') + ', ' + location_info.get('country', ''),
                'salary': self._parse_wttj_salary(job_data.get('salary', {})),
                'description': job_data.get('description', '')[:500],
                'url': job_data.get('websites_urls', {}).get('job_details', ''),
                'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_time': datetime.now().strftime('%H:%M:%S')
            }
            
            if self._is_hardware_manager_job(job):
                jobs.append(job)
        
        return jobs
    
    def _parse_indeed_results(self, data: dict) -> List[Dict]:
        """Parse Indeed API results."""
        jobs = []
        
        for job_data in data.get('results', []):
            job = {
                'title': job_data.get('jobtitle', ''),
                'company': job_data.get('company', ''),
                'location': job_data.get('formattedLocation', ''),
                'salary': job_data.get('salary', 'Not specified'),
                'description': job_data.get('snippet', '')[:500],
                'url': job_data.get('url', ''),
                'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_time': datetime.now().strftime('%H:%M:%S')
            }
            
            if self._is_hardware_manager_job(job):
                jobs.append(job)
        
        return jobs
    
    def _parse_wttj_salary(self, salary_data: dict) -> str:
        """Extract salary information from Welcome to the Jungle data."""
        if not salary_data:
            return "Not specified"
        
        min_salary = salary_data.get('min')
        max_salary = salary_data.get('max')
        currency = salary_data.get('currency', '$')
        
        if min_salary and max_salary:
            return f"{currency}{min_salary:,} - {currency}{max_salary:,}"
        elif min_salary:
            return f"{currency}{min_salary:,}+"
        else:
            return "Not specified"
    
    def _parse_serpapi_results(self, data: dict) -> List[Dict]:
        """Parse SerpAPI Google Jobs results."""
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
                'scraped_time': datetime.now().strftime('%H:%M:%S')
            }
            
            if self._is_hardware_manager_job(job):
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

    def search_with_real_sources(self, keywords: str, location: str, limit: int = 30) -> List[Dict]:
        """
        Use real job sources that provide actual job URLs.
        """
        all_jobs = []
        
        if self.real_sources:
            try:
                # Try RemoteOK for real remote hardware jobs
                logger.info("Trying RemoteOK for real job data...")
                remoteok_jobs = self.real_sources.search_remoteok(keywords, limit // 2)
                if remoteok_jobs:
                    logger.info(f"Found {len(remoteok_jobs)} real jobs from RemoteOK")
                    all_jobs.extend(remoteok_jobs)
            except Exception as e:
                logger.warning(f"RemoteOK error: {e}")
        
        return all_jobs
    
    def scrape_all_sources(self, keywords: str = "hardware manager", location: str = "New York, NY", limit: int = 30) -> List[Dict]:
        """
        Try multiple legitimate sources and combine results, prioritizing real data sources.
        """
        all_jobs = []
        
        # First try real sources that provide actual URLs
        logger.info("Attempting to get real job data...")
        real_jobs = self.search_with_real_sources(keywords, location, limit)
        if real_jobs:
            all_jobs.extend(real_jobs)
            logger.info(f"Added {len(real_jobs)} real jobs")
        
        # Try different APIs - all legitimate and suitable for personal use
        sources = [
            ("Welcome to the Jungle", self.search_with_welcometothejungle),  # High-quality tech jobs
            ("SerpAPI", self.search_with_serpapi),  # Google Jobs aggregation
            ("Adzuna", self.search_with_adzuna),    # Multi-source job aggregation
            ("Indeed", self.search_with_indeed_api), # Indeed's official API
            ("JobAPI", self.search_with_jobapi)     # Another job aggregator
        ]
        
        for source_name, search_func in sources:
            try:
                logger.info(f"Trying {source_name}...")
                jobs = search_func(keywords, location, limit // len(sources))
                logger.info(f"Found {len(jobs)} jobs from {source_name}")
                all_jobs.extend(jobs)
                time.sleep(1)  # Be respectful with API calls
            except Exception as e:
                logger.warning(f"Error with {source_name}: {e}")
                continue
        
        # Remove duplicates based on title and company
        unique_jobs = []
        seen = set()
        
        for job in all_jobs:
            job_id = (job.get('title', ''), job.get('company', ''))
            if job_id not in seen and len(unique_jobs) < limit:
                seen.add(job_id)
                unique_jobs.append(job)
        
        return unique_jobs[:limit]
