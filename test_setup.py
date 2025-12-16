#!/usr/bin/env python3
"""
Test script to verify Google Sheets setup before running the main scraper.
"""
import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are properly set."""
    print("🔍 Testing environment configuration...")
    
    load_dotenv()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found. Please copy env_template.txt to .env and configure it.")
        return False
    
    # Check Google Sheet ID
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    if not sheet_id or sheet_id == 'your_google_sheet_id_here':
        print("❌ GOOGLE_SHEET_ID not configured in .env file")
        print("   Please edit .env and set your Google Sheet ID")
        return False
    
    print(f"✅ Google Sheet ID configured: {sheet_id[:10]}...")
    
    # Check credentials file
    creds_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    if not os.path.exists(creds_file):
        print(f"❌ Credentials file not found: {creds_file}")
        print("   Please download your Google service account credentials as 'credentials.json'")
        return False
    
    print(f"✅ Credentials file found: {creds_file}")
    return True

def test_google_sheets_connection():
    """Test Google Sheets API connection."""
    print("\n🔍 Testing Google Sheets connection...")
    
    try:
        from google_sheets import GoogleSheetsManager
        
        # Initialize the sheets manager
        sheets_manager = GoogleSheetsManager()
        
        # Try to get existing jobs (this tests the connection)
        existing_jobs = sheets_manager.get_existing_jobs()
        
        print(f"✅ Successfully connected to Google Sheets!")
        print(f"   Found {len(existing_jobs)} existing job records")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheets: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you downloaded the credentials.json file")
        print("2. Check that the Google Sheet ID is correct")
        print("3. Verify the sheet is shared with your service account")
        return False

def test_scraper_components():
    """Test that scraper components can be imported."""
    print("\n🔍 Testing scraper components...")
    
    try:
        from linkedin_scraper import LinkedInJobScraper
        from config import Config
        
        # Validate configuration
        Config.validate_config()
        
        print("✅ All scraper components loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading scraper components: {e}")
        return False

def main():
    """Run all setup tests."""
    print("LinkedIn Job Scraper - Setup Test")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    # Test environment configuration
    if test_environment():
        tests_passed += 1
    
    # Test Google Sheets connection
    if test_google_sheets_connection():
        tests_passed += 1
    
    # Test scraper components
    if test_scraper_components():
        tests_passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! You're ready to run the scraper.")
        print("\nTo test the scraper immediately:")
        print("  python job_scraper_agent.py --run-now")
    else:
        print("⚠️  Some tests failed. Please fix the issues above before running the scraper.")
        return False
    
    return True

if __name__ == "__main__":
    main()




