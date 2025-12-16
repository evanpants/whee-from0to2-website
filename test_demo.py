#!/usr/bin/env python3
"""
Demo script to test Google Sheets integration and add some sample data.
"""
import logging
import sys
from datetime import datetime
from google_sheets import GoogleSheetsManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_sample_jobs():
    """Create some sample hardware manager jobs to test the system."""
    sample_jobs = [
        {
            'title': 'Senior Hardware Engineering Manager',
            'company': 'TechCorp Inc.',
            'location': 'New York, NY',
            'salary': '$180,000 - $220,000',
            'description': 'Lead hardware engineering teams in developing next-generation products. Manage cross-functional teams and drive technical strategy.',
            'url': 'https://linkedin.com/jobs/view/sample1',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'scraped_time': datetime.now().strftime('%H:%M:%S')
        },
        {
            'title': 'Principal Hardware Manager',
            'company': 'InnovateTech Solutions',
            'location': 'Manhattan, NY',
            'salary': '$200,000 - $250,000',
            'description': 'Oversee hardware development for consumer electronics. Experience with embedded systems and IoT required.',
            'url': 'https://linkedin.com/jobs/view/sample2',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'scraped_time': datetime.now().strftime('%H:%M:%S')
        },
        {
            'title': 'Hardware Product Manager',
            'company': 'StartupX',
            'location': 'Brooklyn, NY',
            'salary': '$185,000 - $210,000',
            'description': 'Product management role for hardware products. Work with engineering and design teams to bring products to market.',
            'url': 'https://linkedin.com/jobs/view/sample3',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'scraped_time': datetime.now().strftime('%H:%M:%S')
        },
        {
            'title': 'Director of Hardware Engineering',
            'company': 'GlobalTech Corp',
            'location': 'Queens, NY',
            'salary': '$220,000 - $280,000',
            'description': 'Lead and grow hardware engineering organization. Strategic planning and team management for hardware products.',
            'url': 'https://linkedin.com/jobs/view/sample4',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'scraped_time': datetime.now().strftime('%H:%M:%S')
        },
        {
            'title': 'Senior Hardware Manager - AI/ML',
            'company': 'AI Innovations Ltd.',
            'location': 'New York, NY',
            'salary': '$190,000 - $240,000',
            'description': 'Manage hardware teams developing AI/ML accelerator chips. Strong background in semiconductor and neural network hardware.',
            'url': 'https://linkedin.com/jobs/view/sample5',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'scraped_time': datetime.now().strftime('%H:%M:%S')
        }
    ]
    return sample_jobs

def main():
    """Test the Google Sheets integration with sample data."""
    logger.info("Testing Google Sheets integration with sample data...")
    
    try:
        # Initialize the sheets manager
        sheets_manager = GoogleSheetsManager()
        logger.info("✅ Google Sheets connection established")
        
        # Create sample job data
        sample_jobs = create_sample_jobs()
        logger.info(f"✅ Created {len(sample_jobs)} sample jobs")
        
        # Add jobs to the sheet
        added_count = sheets_manager.add_jobs_to_sheet(sample_jobs)
        logger.info(f"✅ Successfully added {added_count} jobs to Google Sheet")
        
        # Get existing jobs to verify
        existing_jobs = sheets_manager.get_existing_jobs()
        logger.info(f"✅ Total jobs in sheet: {len(existing_jobs)}")
        
        print("\n" + "="*60)
        print("🎉 DEMO SUCCESSFUL!")
        print("="*60)
        print(f"✅ Google Sheets integration: WORKING")
        print(f"✅ Added {added_count} new jobs to your sheet")
        print(f"✅ Total jobs now in sheet: {len(existing_jobs)}")
        print(f"✅ Your Google Sheet: https://docs.google.com/spreadsheets/d/1jhrssBU6Te3qwjWTpL59QiIDRXGg1laRRXYyruv8mg4")
        print("\nThe system is ready for daily LinkedIn scraping!")
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()




