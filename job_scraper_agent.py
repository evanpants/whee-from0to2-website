"""
Main agent script for LinkedIn job scraping and Google Sheets integration.
Runs daily at 8 AM ET to scrape hardware manager jobs in NY.
"""
import logging
import schedule
import time
from datetime import datetime, timezone
import sys

from linkedin_scraper import LinkedInJobScraper
from google_sheets import GoogleSheetsManager
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class JobScraperAgent:
    """Main agent class for job scraping operations."""
    
    def __init__(self):
        self.linkedin_scraper = None
        self.sheets_manager = None
    
    def initialize(self):
        """Initialize the scraper and sheets manager."""
        try:
            logger.info("Initializing job scraper agent...")
            
            # Validate configuration
            Config.validate_config()
            
            # Initialize components
            self.sheets_manager = GoogleSheetsManager()
            self.sheets_manager.create_sheet_if_not_exists()
            
            logger.info("Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise
    
    def run_scraping_job(self):
        """Main job scraping task that runs daily."""
        start_time = datetime.now(timezone.utc)
        logger.info(f"Starting daily job scraping at {start_time}")
        
        try:
            # Initialize scraper for this run
            self.linkedin_scraper = LinkedInJobScraper()
            
            # Scrape jobs
            logger.info("Scraping LinkedIn for hardware manager jobs...")
            jobs = self.linkedin_scraper.scrape_jobs()
            
            if not jobs:
                logger.warning("No jobs found during scraping")
                return
            
            logger.info(f"Found {len(jobs)} jobs during scraping")
            
            # Sort jobs by relevance (you can implement custom sorting logic here)
            sorted_jobs = self.sort_jobs_by_relevance(jobs)
            
            # Take top 30 jobs
            top_jobs = sorted_jobs[:Config.MAX_RESULTS]
            logger.info(f"Selected top {len(top_jobs)} jobs for processing")
            
            # Add to Google Sheets
            logger.info("Adding jobs to Google Sheet...")
            added_count = self.sheets_manager.add_jobs_to_sheet(top_jobs)
            
            logger.info(f"Successfully added {added_count} new jobs to Google Sheet")
            
        except Exception as e:
            logger.error(f"Error during job scraping: {e}")
        finally:
            # Clean up
            if self.linkedin_scraper:
                self.linkedin_scraper.close()
                self.linkedin_scraper = None
        
        end_time = datetime.now(timezone.utc)
        duration = end_time - start_time
        logger.info(f"Job scraping completed in {duration}")
    
    def sort_jobs_by_relevance(self, jobs):
        """
        Sort jobs by relevance based on title keywords and salary.
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            Sorted list of jobs
        """
        def relevance_score(job):
            score = 0
            title = job.get('title', '').lower()
            description = job.get('description', '').lower()
            salary = job.get('salary', '')
            
            # Title relevance scoring
            if 'hardware' in title:
                score += 10
            if 'manager' in title:
                score += 8
            if 'director' in title:
                score += 6
            if 'lead' in title:
                score += 4
            
            # Description relevance
            if 'hardware' in description:
                score += 5
            
            # Salary scoring (try to extract numeric value)
            if salary and salary != 'not specified':
                import re
                salary_match = re.search(r'\$?(\d+(?:,\d{3})*)', salary)
                if salary_match:
                    try:
                        salary_num = int(salary_match.group(1).replace(',', ''))
                        if 'k' in salary.lower() or 'thousand' in salary.lower():
                            salary_num *= 1000
                        if salary_num >= Config.MIN_SALARY:
                            score += 3
                        if salary_num >= Config.MIN_SALARY * 1.2:  # 20% above minimum
                            score += 2
                    except:
                        pass
            
            return score
        
        return sorted(jobs, key=relevance_score, reverse=True)
    
    def schedule_jobs(self):
        """Schedule the daily job scraping task."""
        try:
            logger.info(f"Scheduling daily job scraping for {Config.SCHEDULE_TIME} ET")
            
            # Schedule the job for 8 AM ET daily
            schedule.every().day.at(Config.SCHEDULE_TIME).do(self.run_scraping_job)
            
            logger.info("Job scheduling completed. Agent is ready to run.")
            
        except Exception as e:
            logger.error(f"Error scheduling jobs: {e}")
            raise
    
    def run_immediately(self):
        """Run the scraping job immediately (for testing purposes)."""
        logger.info("Running scraping job immediately...")
        self.run_scraping_job()
    
    def start_scheduler(self):
        """Start the scheduler and keep the agent running."""
        logger.info("Starting job scraper agent scheduler...")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Received interrupt signal. Shutting down...")
                break
            except Exception as e:
                logger.error(f"Unexpected error in scheduler: {e}")
                time.sleep(60)  # Wait a minute before retrying

def main():
    """Main function to run the agent."""
    agent = JobScraperAgent()
    
    try:
        # Initialize the agent
        agent.initialize()
        
        # Check if we should run immediately or start scheduler
        if len(sys.argv) > 1 and sys.argv[1] == '--run-now':
            logger.info("Running job scraping immediately...")
            agent.run_immediately()
        else:
            logger.info("Starting scheduled agent...")
            agent.schedule_jobs()
            agent.start_scheduler()
            
    except KeyboardInterrupt:
        logger.info("Agent stopped by user")
    except Exception as e:
        logger.error(f"Fatal error in agent: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        if agent.linkedin_scraper:
            agent.linkedin_scraper.close()

if __name__ == "__main__":
    main()


