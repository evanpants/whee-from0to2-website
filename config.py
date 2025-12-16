"""
Configuration management for LinkedIn job scraper.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the LinkedIn job scraper."""
    
    # LinkedIn search parameters
    JOB_TITLE = "hardware manager"
    LOCATION = "New York, NY"
    MIN_SALARY = 180000
    MAX_RESULTS = 30
    
    # Google Sheets configuration
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    
    # Selenium configuration
    HEADLESS = True  # Set to True for production, False for testing
    BROWSER_TIMEOUT = 30
    
    # LinkedIn URLs
    BASE_URL = "https://www.linkedin.com/jobs"
    SEARCH_URL = f"{BASE_URL}/search"
    
    # Timing configuration
    SCHEDULE_TIME = "08:00"  # 8 AM ET
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 5
    
    @classmethod
    def get_search_params(cls):
        """Get LinkedIn search parameters."""
        return {
            'keywords': cls.JOB_TITLE,
            'location': cls.LOCATION,
            'f_SB2': '8'  # Salary filter for $100k+
        }
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present."""
        required_vars = ['GOOGLE_SHEET_ID']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required configuration: {', '.join(missing_vars)}")
        
        return True
