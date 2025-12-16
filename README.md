# LinkedIn Job Scraper Agent

An automated agent that scrapes LinkedIn for hardware manager job postings in New York with salaries of at least $180,000. The agent runs daily at 8 AM ET and updates a Google Sheet with new job postings, ensuring no duplicates are added.

## Features

- **Automated Daily Scraping**: Runs at 8 AM ET every day
- **Smart Filtering**: Searches for hardware manager positions in NY with $180k+ salaries
- **Duplicate Prevention**: Never adds duplicate job postings
- **Google Sheets Integration**: Automatically updates a Google Sheet with new jobs
- **Top 30 Results**: Adds the 30 best matches each day
- **Robust Error Handling**: Continues running even if individual jobs fail
- **Detailed Logging**: Comprehensive logging for monitoring and debugging

## Prerequisites

1. **Python 3.8+**
2. **Google Cloud Project** with Sheets API enabled
3. **Google Sheet** created and shared with the service account
4. **Chrome browser** (for Selenium)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API" and enable it
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Download the JSON key file and rename it to `credentials.json`
   - Place it in the project root directory

5. Create a Google Sheet and get the Sheet ID:
   - Create a new Google Sheet
   - Copy the Sheet ID from the URL (the long string between `/d/` and `/edit`)
   - Share the sheet with the service account email (found in credentials.json)

### 3. Configuration

1. Copy the environment template:
   ```bash
   cp env_template.txt .env
   ```

2. Edit `.env` file with your configuration:
   ```
   GOOGLE_SHEET_ID=your_actual_sheet_id_here
   GOOGLE_CREDENTIALS_FILE=credentials.json
   ```

### 4. First Run Test

Test the setup by running the scraper immediately:

```bash
python job_scraper_agent.py --run-now
```

This will:
- Scrape LinkedIn for hardware manager jobs in NY
- Filter for salaries >= $180,000
- Add top 30 results to your Google Sheet
- Create the sheet headers if it's the first run

## Usage

### Run Once (for testing)
```bash
python job_scraper_agent.py --run-now
```

### Run Scheduled (production)
```bash
python job_scraper_agent.py
```

The agent will:
- Run the scraping job daily at 8 AM ET
- Continue running in the background
- Log all activities to `job_scraper.log`

### Stop the Agent
Press `Ctrl+C` to stop the scheduled agent.

## Configuration Options

Edit `config.py` to modify:

- **Job criteria**: Title, location, minimum salary
- **Schedule time**: Default is 8 AM ET
- **Max results**: Number of jobs to add per day (default: 30)
- **Scraping options**: Browser settings, timeouts, etc.

## Output

The Google Sheet will contain columns:
- **Title**: Job title
- **Company**: Company name
- **Location**: Job location
- **Salary**: Salary information (if available)
- **Description**: Job description snippet
- **URL**: Link to the LinkedIn job posting
- **Scraped Date**: Date when the job was scraped
- **Scraped Time**: Time when the job was scraped

## Troubleshooting

### Common Issues

1. **"Credentials file not found"**
   - Ensure `credentials.json` is in the project root
   - Check the file name matches your configuration

2. **"Google Sheet ID not configured"**
   - Set the `GOOGLE_SHEET_ID` in your `.env` file
   - Ensure the sheet is shared with your service account

3. **"Permission denied"**
   - Check that the service account has edit access to the Google Sheet
   - Verify the Sheet ID is correct

4. **No jobs found**
   - LinkedIn may have changed their page structure
   - Check the logs for specific error messages
   - Consider adjusting the search criteria in `config.py`

### Logs

Check `job_scraper.log` for detailed information about:
- Scraping progress
- Errors and warnings
- Number of jobs found and added
- Duplicate detection results

## Legal and Ethical Considerations

- This scraper is for educational and personal use
- Respect LinkedIn's Terms of Service
- Use reasonable delays between requests
- Consider the website's robots.txt policy
- Be mindful of rate limiting to avoid being blocked

## Technical Details

### Architecture

- **LinkedIn Scraper**: Uses Selenium WebDriver to navigate LinkedIn job search
- **Google Sheets**: Uses Google Sheets API for data storage
- **Scheduler**: Uses the `schedule` library for daily execution
- **Duplicate Detection**: Compares title, company, and URL to prevent duplicates

### Error Handling

- Graceful handling of network timeouts
- Retry mechanisms for failed requests
- Continues processing even if individual jobs fail
- Comprehensive logging for debugging

## Support

For issues or questions, check the logs first and refer to the troubleshooting section above.


