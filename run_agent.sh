#!/bin/bash

# LinkedIn Job Scraper Agent Launcher
# This script helps launch the agent with proper error handling

echo "LinkedIn Job Scraper Agent"
echo "========================="

# Check if we're in the right directory
if [ ! -f "job_scraper_agent.py" ]; then
    echo "Error: job_scraper_agent.py not found. Please run this script from the project directory."
    exit 1
fi

# Check if virtual environment should be activated
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if dependencies are installed
if ! python -c "import selenium, schedule, google" 2>/dev/null; then
    echo "Dependencies not found. Installing..."
    pip install -r requirements.txt
fi

# Run the agent
echo "Starting job scraper agent..."
if [ "$1" = "--run-now" ]; then
    echo "Running immediate scrape..."
    python job_scraper_agent.py --run-now
else
    echo "Starting scheduled agent (Ctrl+C to stop)..."
    python job_scraper_agent.py
fi


