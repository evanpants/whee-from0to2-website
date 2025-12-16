# Google Sheets Setup Guide

## Step-by-Step Google Sheets Configuration

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" then "New Project"
3. Name your project (e.g., "LinkedIn Job Scraper")
4. Click "Create"

### Step 2: Enable Google Sheets API

1. In your new project, go to **APIs & Services** > **Library**
2. Search for "Google Sheets API"
3. Click on it and press **"Enable"**

### Step 3: Create Service Account Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **"+ CREATE CREDENTIALS"** > **"Service account"**
3. Fill in the details:
   - **Service account name**: `linkedin-scraper-service`
   - **Service account ID**: Will auto-generate (keep it)
   - **Description**: `Service account for LinkedIn job scraper`
4. Click **"Create and Continue"**
5. Skip the next steps (Grant access, Grant users access) - just click **"Done"**

### Step 4: Create Service Account Key

1. In the Credentials page, find your new service account
2. Click on the service account email
3. Go to the **"Keys"** tab
4. Click **"Add Key"** > **"Create new key"**
5. Choose **JSON** format
6. Click **"Create"**
7. **IMPORTANT**: This will download a JSON file - save it as `credentials.json` in your project folder

### Step 5: Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a **New** blank spreadsheet
3. Name it something like "Hardware Manager Jobs"
4. **Copy the Sheet ID** from the URL:
   - URL looks like: `https://docs.google.com/spreadsheets/d/1ABC123DEF456GHI789JKL/edit`
   - The Sheet ID is: `1ABC123DEF456GHI789JKL` (the part between `/d/` and `/edit`)

### Step 6: Share Sheet with Service Account

1. In your Google Sheet, click **Share** (top right)
2. Add the service account email (it looks like: `linkedin-scraper-service@your-project-id.iam.gserviceaccount.com`)
3. Give it **Editor** permissions
4. Click **Send** (you don't need to notify anyone)

### Step 7: Configure Environment

1. Copy your Sheet ID from Step 5
2. In Terminal, run:
   ```bash
   cp env_template.txt .env
   ```
3. Edit the `.env` file and replace `your_google_sheet_id_here` with your actual Sheet ID

## Testing the Setup

Once configured, test with:
```bash
python job_scraper_agent.py --run-now
```

This will run once immediately without waiting for the 8 AM schedule.


