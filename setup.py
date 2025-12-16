#!/usr/bin/env python3
"""
Setup script for LinkedIn Job Scraper Agent.
"""
import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def check_credentials():
    """Check if credentials file exists."""
    if not os.path.exists("credentials.json"):
        print("Warning: credentials.json not found.")
        print("Please download your Google service account credentials and save as 'credentials.json'")
        return False
    print("Credentials file found!")
    return True

def check_env_file():
    """Check if .env file exists and is configured."""
    if not os.path.exists(".env"):
        print("Creating .env file from template...")
        try:
            with open("env_template.txt", "r") as template:
                content = template.read()
            with open(".env", "w") as env_file:
                env_file.write(content)
            print("Created .env file. Please edit it with your Google Sheet ID.")
            return False
    else:
        # Check if GOOGLE_SHEET_ID is set
        with open(".env", "r") as f:
            content = f.read()
            if "your_google_sheet_id_here" in content:
                print("Please edit .env file and set your Google Sheet ID.")
                return False
    
    print("Environment file configured!")
    return True

def main():
    """Main setup function."""
    print("Setting up LinkedIn Job Scraper Agent...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check credentials
    creds_ok = check_credentials()
    
    # Check environment file
    env_ok = check_env_file()
    
    print("\n" + "=" * 50)
    if creds_ok and env_ok:
        print("✅ Setup completed successfully!")
        print("\nYou can now run the agent with:")
        print("  python job_scraper_agent.py --run-now    # Test run")
        print("  python job_scraper_agent.py              # Start scheduler")
    else:
        print("⚠️  Setup completed with warnings.")
        print("\nPlease complete the following:")
        if not creds_ok:
            print("  - Add your Google credentials.json file")
        if not env_ok:
            print("  - Configure your .env file with Google Sheet ID")
        print("\nThen you can run the agent.")
    
    return True

if __name__ == "__main__":
    main()


