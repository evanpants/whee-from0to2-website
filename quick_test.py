#!/usr/bin/env python3
"""
Quick test to verify basic configuration without installing all dependencies.
"""
import os
import json

def check_config():
    """Check if basic configuration files are present and valid."""
    print("🔍 Checking configuration files...")
    
    # Check .env file
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    print("✅ .env file found")
    
    # Check credentials.json
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json file not found")
        return False
    
    print("✅ credentials.json file found")
    
    # Read .env file
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            if 'your_google_sheet_id_here' not in env_content:
                print("✅ Google Sheet ID appears to be configured")
            else:
                print("❌ Google Sheet ID still has placeholder value")
                return False
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    # Check credentials.json format
    try:
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
            if 'client_email' in creds and 'private_key' in creds:
                print("✅ credentials.json has valid format")
                print(f"   Service account email: {creds['client_email']}")
            else:
                print("❌ credentials.json appears to be malformed")
                return False
    except Exception as e:
        print(f"❌ Error reading credentials.json: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("LinkedIn Job Scraper - Quick Configuration Test")
    print("=" * 50)
    
    if check_config():
        print("\n🎉 Basic configuration looks good!")
        print("\nNext steps:")
        print("1. Install dependencies: pip3 install -r requirements.txt")
        print("2. Test full setup: python3 test_setup.py")
        print("3. Run test scrape: python3 job_scraper_agent.py --run-now")
    else:
        print("\n⚠️  Configuration issues found. Please fix them before proceeding.")




