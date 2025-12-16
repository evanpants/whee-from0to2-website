# Google Apps Script Setup Guide

This guide will walk you through setting up Google Apps Script to handle form submissions from your website and automatically save them to your Google Sheet.

## Prerequisites

- Access to the Google Sheet: https://docs.google.com/spreadsheets/d/1rlA9JrJyElCr9NEs31Qsa9QA-4GeSQVX5CQJhbDggoc/edit#gid=2065220436
- A Google account with access to the sheet

## Step-by-Step Setup

### Step 1: Open Apps Script

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1rlA9JrJyElCr9NEs31Qsa9QA-4GeSQVX5CQJhbDggoc/edit#gid=2065220436
2. Click on **"Extensions"** in the menu bar
3. Select **"Apps Script"**
4. A new tab will open with the Apps Script editor

### Step 2: Paste the Code

1. In the Apps Script editor, you'll see a default function
2. **Delete all existing code** in the editor
3. Open the file `google-apps-script-code.gs` from your project
4. **Copy the entire contents** of that file
5. **Paste it** into the Apps Script editor

### Step 3: Configure the Script

1. In the code, find this line:
   ```javascript
   const SHEET_NAME = 'YOUR_SHEET_NAME';
   ```
2. Replace `'YOUR_SHEET_NAME'` with the actual name of the tab in your Google Sheet
   - To find the tab name: Look at the bottom of your Google Sheet for the tab name
   - For example, if the tab is called "Inquiries", change it to: `const SHEET_NAME = 'Inquiries';`
   - If you're not sure, you can leave it as is - the script will try to find the sheet by GID (2065220436)

3. Verify the email address is correct:
   ```javascript
   const EMAIL_TO = 'ride@from0to2.com';
   ```
   - This should already be set correctly, but double-check

### Step 4: Save the Script

1. Click the **"Save"** icon (floppy disk) or press `Cmd+S` (Mac) / `Ctrl+S` (Windows)
2. Give your project a name (e.g., "from0to2 Form Handler")
3. Click **"OK"**

### Step 5: Deploy as Web App

1. Click the **"Deploy"** button (top right)
2. Select **"New deployment"**
3. Click the gear icon (⚙️) next to "Select type" and choose **"Web app"**
4. Fill in the deployment settings:
   - **Description**: "from0to2 form handler v1" (or any description)
   - **Execute as**: Select **"Me"** (your email)
   - **Who has access**: Select **"Anyone"** (important - this allows your website to submit forms)
5. Click **"Deploy"**

### Step 6: Authorize the Script

1. Google will ask you to authorize the script
2. Click **"Authorize access"**
3. Select your Google account
4. You'll see a warning: "Google hasn't verified this app"
   - Click **"Advanced"**
   - Click **"Go to [your project name] (unsafe)"**
5. Click **"Allow"** to grant permissions

### Step 7: Copy the Web App URL

1. After deployment, you'll see a **"Web app"** section
2. Copy the **"Web app URL"** - it will look like:
   ```
   https://script.google.com/macros/s/AKfycby.../exec
   ```
3. **IMPORTANT**: Save this URL somewhere safe - you'll need it in the next step

### Step 8: Update HTML Files

1. Open these files in your project:
   - `tern-gsd.html`
   - `tern-hsd.html`
   - `tern-quick-haul.html`

2. In each file, find this line:
   ```javascript
   const scriptUrl = 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE';
   ```

3. Replace `'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE'` with the Web App URL you copied
   - For example:
   ```javascript
   const scriptUrl = 'https://script.google.com/macros/s/AKfycby.../exec';
   ```

4. Save all three files

### Step 9: Commit and Push Changes to GitHub

**Platform:** Terminal (Command Line) on your Mac  
**Location:** Your project folder: `/Users/evan/Documents/Cursor - Project 1`

#### Detailed Steps:

1. **Open Terminal on your Mac:**
   - Press `Cmd + Space` to open Spotlight
   - Type "Terminal" and press Enter
   - OR go to Applications > Utilities > Terminal

2. **Navigate to your project folder:**
   - Type this command and press Enter:
     ```bash
     cd "/Users/evan/Documents/Cursor - Project 1"
     ```
   - You should see the prompt change to show you're in that directory

3. **Check what files have changed:**
   - Type this command to see what files were modified:
     ```bash
     git status
     ```
   - You should see the three HTML files listed (tern-gsd.html, tern-hsd.html, tern-quick-haul.html)

4. **Add all changed files:**
   - Type this command and press Enter:
     ```bash
     git add .
     ```
   - This stages all your changes for commit

5. **Commit the changes:**
   - Type this command and press Enter:
     ```bash
     git commit -m "Add Google Apps Script integration for forms"
     ```
   - This saves your changes with a message describing what you did

6. **Push to GitHub:**
   - Type this command and press Enter:
     ```bash
     git push
     ```
   - If prompted for credentials:
     - **Username:** Your GitHub username
     - **Password:** Use a Personal Access Token (NOT your GitHub password)
       - If you don't have one, see: https://github.com/settings/tokens
       - Create a token with "repo" permissions
       - Use that token as your password

7. **Wait for confirmation:**
   - You should see a message like "Writing objects: 100%"
   - This means your changes are now on GitHub

### Step 10: Test the Form

1. **Wait 1-2 minutes** for GitHub Pages to update your live website

2. **Visit one of your bike pages:**
   - Go to: `https://from0to2.com/tern-gsd.html`
   - OR: `https://from0to2.com/tern-hsd.html`
   - OR: `https://from0to2.com/tern-quick-haul.html`

3. **Fill out and submit the form:**
   - Enter your email address
   - Optionally add your name and a message
   - Click "Submit Inquiry" or "Notify Me When Available"

4. **Check the results:**
   - **Google Sheet:** Open your Google Sheet and check if a new row was added with your form data
   - **Email:** Check ride@from0to2.com for an email notification about the submission

## Troubleshooting

### Form submissions not working?

1. **Check the Web App URL**: Make sure it's correctly pasted in all three HTML files
2. **Check deployment settings**: Ensure "Who has access" is set to "Anyone"
3. **Check browser console**: Open browser developer tools (F12) and look for errors
4. **Check Apps Script execution log**: In Apps Script editor, go to "Executions" to see if requests are being received

### Data not appearing in sheet?

1. **Check sheet name**: Make sure `SHEET_NAME` matches your actual tab name
2. **Check permissions**: Ensure the script has permission to edit the sheet
3. **Check sheet ID**: Verify the sheet ID in the code matches your sheet

### Email not being sent?

1. **Check email address**: Verify `EMAIL_TO` is set to `ride@from0to2.com`
2. **Check Apps Script quotas**: Google has daily email limits (100 emails/day for free accounts)
3. **Check spam folder**: Emails might be going to spam

## Data Captured

Each form submission will include:
- **Email** (required)
- **Name** (optional)
- **Message** (optional)
- **Bike Model** (TERN GSD, TERN HSD, or TERN Quick Haul)
- **Status** (Available or Out of Stock)
- **Timestamp** (when form was submitted)
- **Referrer** (where user came from)
- **User Agent** (browser/device info)
- **IP Address** (automatically captured)
- **Date** and **Time** (formatted)

## Security Notes

- The Web App URL is public, but only accepts POST requests
- Form validation happens on the client side
- Consider adding rate limiting if you receive spam submissions
- The script automatically handles errors gracefully

## Need Help?

If you encounter issues:
1. Check the Apps Script execution log for errors
2. Verify all URLs and settings are correct
3. Test with a simple form submission first
4. Check that the sheet permissions allow the script to write data

