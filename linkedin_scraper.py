"""
LinkedIn job scraper for hardware manager positions.
"""
import time
import re
import os
import logging
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from config import Config

logger = logging.getLogger(__name__)

class LinkedInJobScraper:
    """Scraper for LinkedIn job postings."""
    
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with appropriate options."""
        chrome_options = Options()
        if Config.HEADLESS:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            # Set Chrome binary path for macOS
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            
            # Try to install and setup ChromeDriver with proper path resolution
            try:
                driver_path = ChromeDriverManager().install()
                # Ensure we get the actual executable, not a directory
                if os.path.isdir(driver_path):
                    # Look for the chromedriver executable in the directory
                    possible_paths = [
                        os.path.join(driver_path, "chromedriver"),
                        os.path.join(driver_path, "chromedriver-mac-x64", "chromedriver"),
                        os.path.join(driver_path, "chromedriver.exe")
                    ]
                    for path in possible_paths:
                        if os.path.isfile(path) and os.access(path, os.X_OK):
                            driver_path = path
                            break
                    else:
                        raise Exception(f"Could not find executable chromedriver in {driver_path}")
                
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                logger.info(f"Chrome driver initialized successfully with path: {driver_path}")
                
            except Exception as driver_error:
                logger.warning(f"WebDriver Manager failed: {driver_error}")
                # Fallback: let Selenium find the driver automatically
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                logger.info("Chrome driver initialized successfully with auto-detection")
                
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            logger.info("You may need to install Chrome browser or check your ChromeDriver setup")
            raise
    
    def scrape_jobs(self) -> List[Dict]:
        """
        Scrape LinkedIn jobs based on configured criteria.
        
        Returns:
            List of job dictionaries with relevant information.
        """
        try:
            logger.info("Starting LinkedIn job scraping...")
            
            # Navigate to LinkedIn jobs search
            search_url = self._build_search_url()
            logger.info(f"Navigating to: {search_url}")
            
            self.driver.get(search_url)
            
            # Add random delay to avoid detection
            time.sleep(3)
            
            try:
                # Wait for page to load with multiple possible selectors
                selectors_to_try = [
                    (By.CLASS_NAME, "jobs-search-results-list"),
                    (By.CLASS_NAME, "scaffold-layout__main"),
                    (By.CSS_SELECTOR, "[data-test-id='search-results']"),
                    (By.TAG_NAME, "main")
                ]
                
                page_loaded = False
                for selector_type, selector_value in selectors_to_try:
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((selector_type, selector_value))
                        )
                        page_loaded = True
                        logger.info(f"Page loaded, found element with {selector_type}: {selector_value}")
                        break
                    except:
                        continue
                
                if not page_loaded:
                    logger.warning("Could not detect page load, proceeding anyway...")
                
                time.sleep(2)  # Additional wait for dynamic content
                
            except Exception as wait_error:
                logger.warning(f"Error waiting for page load: {wait_error}")
                time.sleep(5)  # Fallback wait
            
            jobs = []
            processed_jobs = set()  # To avoid duplicates within the same run
            
            # Try multiple selectors for job cards
            job_cards_selectors = [
                ".scaffold-layout__list-container .jobs-search-results__list-item",
                ".jobs-search-results__list-item",
                "[data-job-id]",
                ".job-card-container"
            ]
            
            job_cards = []
            for selector in job_cards_selectors:
                try:
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if job_cards:
                        logger.info(f"Found {len(job_cards)} job cards using selector: {selector}")
                        break
                except:
                    continue
            
            if not job_cards:
                logger.warning("No job cards found, LinkedIn may have changed their structure or detected automation")
                return []
            
            # Process job cards with better error handling
            for i, job_card in enumerate(job_cards[:Config.MAX_RESULTS * 2]):  # Get more to filter
                try:
                    # Scroll to element to ensure it's visible
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
                    time.sleep(0.5)  # Small delay between cards
                    
                    job_data = self._extract_job_data(job_card)
                    if job_data and self._is_valid_job(job_data):
                        # Use job URL as unique identifier
                        job_id = job_data.get('url', f"job_{i}")
                        if job_id not in processed_jobs:
                            processed_jobs.add(job_id)
                            jobs.append(job_data)
                            
                            if len(jobs) >= Config.MAX_RESULTS:
                                break
                                
                except Exception as e:
                    logger.warning(f"Error processing job card {i}: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs)} valid jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Error during job scraping: {e}")
            # Return empty list instead of crashing
            return []
    
    def _build_search_url(self) -> str:
        """Build LinkedIn search URL with parameters."""
        params = Config.get_search_params()
        base_url = f"{Config.SEARCH_URL}?keywords={params['keywords']}&location={params['location']}"
        return base_url.replace(' ', '%20')
    
    def _extract_job_data(self, job_card) -> Optional[Dict]:
        """Extract job data from a job card element."""
        try:
            # Extract job title
            title_element = job_card.find_element(By.CSS_SELECTOR, ".job-card-list__title a, .jobs-unified-top-card__job-title a")
            job_title = title_element.text.strip() if title_element else "N/A"
            
            # Extract company name
            company_element = job_card.find_element(By.CSS_SELECTOR, ".job-card-container__company-name, .jobs-unified-top-card__company-name")
            company = company_element.text.strip() if company_element else "N/A"
            
            # Extract location
            location_element = job_card.find_element(By.CSS_SELECTOR, ".job-card-container__metadata-wrapper .job-card-container__primary-description, .jobs-unified-top-card__bullet")
            location = location_element.text.strip() if location_element else "N/A"
            
            # Extract job URL
            job_url = ""
            try:
                link_element = job_card.find_element(By.CSS_SELECTOR, ".job-card-list__title a, .jobs-unified-top-card__job-title a")
                job_url = link_element.get_attribute("href")
            except:
                pass
            
            # Try to extract salary information
            salary = self._extract_salary(job_card)
            
            # Get job description (requires clicking into the job)
            description = self._get_job_description(job_card)
            
            return {
                'title': job_title,
                'company': company,
                'location': location,
                'salary': salary,
                'description': description,
                'url': job_url,
                'scraped_date': time.strftime('%Y-%m-%d'),
                'scraped_time': time.strftime('%H:%M:%S')
            }
            
        except Exception as e:
            logger.warning(f"Error extracting job data: {e}")
            return None
    
    def _extract_salary(self, job_card) -> str:
        """Extract salary information from job card."""
        try:
            # Look for salary indicators in various possible locations
            salary_selectors = [
                ".job-card-container__metadata .job-card-container__primary-description",
                ".salary",
                "[data-test='attribute-text']"
            ]
            
            for selector in salary_selectors:
                try:
                    elements = job_card.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text
                        if any(keyword in text.lower() for keyword in ['$', 'salary', 'compensation', 'pay']):
                            # Extract numeric salary information
                            salary_match = re.search(r'\$[\d,]+(?:-\$[\d,]+)?(?:\s*(?:k|thousand|000))?', text, re.IGNORECASE)
                            if salary_match:
                                return salary_match.group()
                except:
                    continue
            
            return "Not specified"
        except:
            return "Not specified"
    
    def _get_job_description(self, job_card) -> str:
        """Get job description by clicking into the job."""
        try:
            # Click on the job card to get more details
            clickable_element = job_card.find_element(By.CSS_SELECTOR, ".job-card-list__title a, .jobs-unified-top-card__job-title")
            self.driver.execute_script("arguments[0].click();", clickable_element)
            
            # Wait for job details to load
            time.sleep(2)
            
            # Extract job description
            try:
                desc_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-description-content__text, .jobs-box__html-content"))
                )
                description = desc_element.text[:500] if desc_element else ""  # Limit description length
                return description
            except:
                return ""
        except Exception as e:
            logger.warning(f"Could not extract job description: {e}")
            return ""
    
    def _is_valid_job(self, job_data: Dict) -> bool:
        """Check if job meets the criteria."""
        try:
            # Check if it's hardware manager related
            title_lower = job_data.get('title', '').lower()
            description_lower = job_data.get('description', '').lower()
            
            hardware_keywords = ['hardware', 'engineering manager', 'product manager', 'technical manager']
            manager_keywords = ['manager', 'director', 'lead', 'head']
            
            has_hardware = any(keyword in title_lower or keyword in description_lower for keyword in hardware_keywords)
            has_manager = any(keyword in title_lower or keyword in description_lower for keyword in manager_keywords)
            
            # Check salary if available
            salary = job_data.get('salary', '').lower()
            salary_valid = True
            
            if salary != "not specified" and salary:
                # Extract numeric salary value
                salary_match = re.search(r'\$?(\d+(?:,\d{3})*)', salary)
                if salary_match:
                    try:
                        salary_num = int(salary_match.group(1).replace(',', ''))
                        # Convert k to thousands if present
                        if 'k' in salary or 'thousand' in salary:
                            salary_num *= 1000
                        salary_valid = salary_num >= Config.MIN_SALARY
                    except:
                        salary_valid = True  # If we can't parse, assume it's valid
            
            # Check location (should be NY-based)
            location = job_data.get('location', '').lower()
            ny_keywords = ['new york', 'ny', 'nyc', 'queens', 'brooklyn', 'manhattan', 'bronx', 'staten island']
            is_ny = any(keyword in location for keyword in ny_keywords)
            
            return has_hardware and has_manager and is_ny and salary_valid
            
        except Exception as e:
            logger.warning(f"Error validating job: {e}")
            return False
    
    def close(self):
        """Close the browser driver."""
        if self.driver:
            self.driver.quit()
