"""
Google Sheets integration for storing scraped job data.
"""
import logging
from typing import List, Dict
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

from config import Config

logger = logging.getLogger(__name__)

class GoogleSheetsManager:
    """Manager for Google Sheets operations."""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SHEET_NAME = 'Hardware Manager Jobs'
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self.setup_google_sheets()
    
    def setup_google_sheets(self):
        """Setup Google Sheets API connection."""
        try:
            if not os.path.exists(Config.GOOGLE_CREDENTIALS_FILE):
                raise FileNotFoundError(f"Credentials file not found: {Config.GOOGLE_CREDENTIALS_FILE}")
            
            # Use service account credentials
            creds = service_account.Credentials.from_service_account_file(
                Config.GOOGLE_CREDENTIALS_FILE, scopes=self.SCOPES)
            
            self.credentials = creds
            self.service = build('sheets', 'v4', credentials=creds)
            logger.info("Google Sheets connection established")
            
        except Exception as e:
            logger.error(f"Error setting up Google Sheets: {e}")
            raise
    
    def get_existing_jobs(self) -> List[Dict]:
        """Get existing job data from the sheet to check for duplicates."""
        try:
            if not Config.GOOGLE_SHEET_ID:
                raise ValueError("Google Sheet ID not configured")
            
            range_name = f'{self.SHEET_NAME}!A:J'  # Assuming columns A through J
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=Config.GOOGLE_SHEET_ID,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.info("No existing data found in sheet")
                return []
            
            # Convert to list of dictionaries (skip header row)
            headers = values[0] if values else []
            existing_jobs = []
            
            for row in values[1:]:  # Skip header row
                if len(row) >= len(headers):
                    job_dict = dict(zip(headers, row[:len(headers)]))
                    existing_jobs.append(job_dict)
            
            logger.info(f"Retrieved {len(existing_jobs)} existing job records")
            return existing_jobs
            
        except Exception as e:
            logger.error(f"Error retrieving existing jobs: {e}")
            return []
    
    def is_duplicate(self, new_job: Dict, existing_jobs: List[Dict]) -> bool:
        """Check if a job is a duplicate based on title, company, and URL."""
        try:
            new_title = new_job.get('title', '').strip().lower()
            new_company = new_job.get('company', '').strip().lower()
            new_url = new_job.get('url', '').strip()
            
            for existing_job in existing_jobs:
                existing_title = existing_job.get('title', '').strip().lower()
                existing_company = existing_job.get('company', '').strip().lower()
                existing_url = existing_job.get('url', '').strip()
                
                # Check for exact URL match first
                if new_url and existing_url and new_url == existing_url:
                    return True
                
                # Check for title and company match
                if (new_title == existing_title and 
                    new_company == existing_company and
                    new_title and new_company):
                    return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Error checking for duplicates: {e}")
            return False
    
    def add_jobs_to_sheet(self, jobs: List[Dict]) -> int:
        """
        Add new jobs to the Google Sheet.
        
        Args:
            jobs: List of job dictionaries to add
            
        Returns:
            Number of jobs successfully added
        """
        try:
            if not jobs:
                logger.info("No jobs to add")
                return 0
            
            # Get existing jobs to check for duplicates
            existing_jobs = self.get_existing_jobs()
            
            # Filter out duplicates
            new_jobs = []
            for job in jobs:
                if not self.is_duplicate(job, existing_jobs):
                    new_jobs.append(job)
            
            if not new_jobs:
                logger.info("All jobs are duplicates, nothing to add")
                return 0
            
            logger.info(f"Adding {len(new_jobs)} new jobs (filtered from {len(jobs)} total)")
            
            # Prepare the data for insertion
            if not existing_jobs:
                # First time - add headers
                headers = ['Title', 'Company', 'Location', 'Salary', 'Description', 'URL', 'Scraped Date', 'Scraped Time']
                values_to_add = [headers]
            else:
                # Check if headers exist
                range_name = f'{self.SHEET_NAME}!A1:J1'
                result = self.service.spreadsheets().values().get(
                    spreadsheetId=Config.GOOGLE_SHEET_ID,
                    range=range_name
                ).execute()
                
                headers = result.get('values', [[]])[0]
                if not headers:
                    headers = ['Title', 'Company', 'Location', 'Salary', 'Description', 'URL', 'Scraped Date', 'Scraped Time']
                    values_to_add = [headers]
                else:
                    values_to_add = []
            
            # Add new job data
            for job in new_jobs:
                row = [
                    job.get('title', ''),
                    job.get('company', ''),
                    job.get('location', ''),
                    job.get('salary', ''),
                    job.get('description', '')[:500],  # Limit description length
                    job.get('url', ''),
                    job.get('scraped_date', ''),
                    job.get('scraped_time', '')
                ]
                values_to_add.append(row)
            
            # Determine where to insert (after existing data or at the beginning)
            if existing_jobs:
                # Find the next empty row
                range_name = f'{self.SHEET_NAME}!A:J'
                result = self.service.spreadsheets().values().get(
                    spreadsheetId=Config.GOOGLE_SHEET_ID,
                    range=range_name
                ).execute()
                
                values = result.get('values', [])
                next_row = len(values) + 1
                
                # Only add new job rows (skip headers)
                new_job_rows = values_to_add[1:] if len(values_to_add) > 1 and values_to_add[0] == headers else values_to_add
                
                if new_job_rows:
                    range_to_update = f'{self.SHEET_NAME}!A{next_row}:H{next_row + len(new_job_rows) - 1}'
                    
                    body = {
                        'values': new_job_rows
                    }
                    
                    result = self.service.spreadsheets().values().update(
                        spreadsheetId=Config.GOOGLE_SHEET_ID,
                        range=range_to_update,
                        valueInputOption='RAW',
                        body=body
                    ).execute()
            else:
                # First time setup
                range_to_update = f'{self.SHEET_NAME}!A1:H{len(values_to_add)}'
                
                body = {
                    'values': values_to_add
                }
                
                result = self.service.spreadsheets().values().update(
                    spreadsheetId=Config.GOOGLE_SHEET_ID,
                    range=range_to_update,
                    valueInputOption='RAW',
                    body=body
                ).execute()
            
            logger.info(f"Successfully added {len(new_jobs)} jobs to Google Sheet")
            return len(new_jobs)
            
        except Exception as e:
            logger.error(f"Error adding jobs to sheet: {e}")
            return 0
    
    def create_sheet_if_not_exists(self):
        """Create the sheet if it doesn't exist."""
        try:
            # Get spreadsheet metadata
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=Config.GOOGLE_SHEET_ID
            ).execute()
            
            sheet_names = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
            
            if self.SHEET_NAME not in sheet_names:
                # Create new sheet
                request_body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': self.SHEET_NAME
                            }
                        }
                    }]
                }
                
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=Config.GOOGLE_SHEET_ID,
                    body=request_body
                ).execute()
                
                logger.info(f"Created new sheet: {self.SHEET_NAME}")
            else:
                logger.info(f"Sheet {self.SHEET_NAME} already exists")
                
        except Exception as e:
            logger.error(f"Error creating sheet: {e}")
            raise
