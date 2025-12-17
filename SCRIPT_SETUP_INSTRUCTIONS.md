# Complete Google Apps Script Setup Instructions

## Step-by-Step Setup

### Step 1: Open Your Google Sheet
1. Go to: https://docs.google.com/spreadsheets/d/1rlA9JrJyElCr9NEs31Qsa9QA-4GeSQVX5CQJhbDggoc/edit#gid=2065220436
2. Click **Extensions** → **Apps Script**

### Step 2: Replace All Code
1. In the Apps Script editor, **SELECT ALL** (Ctrl+A or Cmd+A)
2. **DELETE** everything
3. Open the file `COMPLETE_GOOGLE_APPS_SCRIPT.gs` from your project folder
4. **COPY ALL** the code (Ctrl+A, Ctrl+C or Cmd+A, Cmd+C)
5. **PASTE** it into the Apps Script editor (Ctrl+V or Cmd+V)

### Step 3: Update Configuration (if needed)
1. Look at the top of the script for these lines:
   ```javascript
   const SHEET_NAME = 'website_inquiries'; // Change this if your tab has a different name
   ```
2. If your sheet tab name is different, change `'website_inquiries'` to your actual tab name
3. The email address `ride@from0to2.com` should already be correct

### Step 4: Save the Script
1. Click **File** → **Save** (or Ctrl+S / Cmd+S)
2. Give it a name like "Form Handler" if prompted

### Step 5: Test Sheet Access
1. In the function dropdown (top of editor), select `testSheetAccess`
2. Click **Run** (▶️)
3. Check the **Execution log** (View → Logs or Ctrl+Enter / Cmd+Enter)
4. You should see "Sheet accessed successfully"

### Step 6: Test Email and Trigger Authorization

**If the authorization prompt doesn't appear, try these methods in order:**

#### Method A: Run testEmail Function
1. In the function dropdown, select `testEmail`
2. Click **Run** (▶️)
3. Check the **Execution log** (View → Logs or press Ctrl+Enter / Cmd+Enter)
4. Look for any error messages

**If you see "Authorization required" in the log:**
- Click on the error message
- This should open the authorization flow
- Click **Review Permissions** → Choose account → **Advanced** → **Go to [Project Name] (unsafe)** → **Allow**

**If you see an error but no authorization prompt:**
- Try Method B below

#### Method B: Deploy First (This Often Triggers Authorization)
1. **Skip to Step 7** and deploy the web app first
2. During deployment, Google may ask for authorization
3. After deploying, come back and try `testEmail` again

#### Method C: Check Existing Authorizations
1. In Apps Script, look for a **🔒 Lock icon** in the toolbar
2. Or go to **View** → **Show execution transcript**
3. If you see "Authorization required", click it

#### Method D: Manual Authorization via OAuth
1. In Apps Script, go to **Overview** (left sidebar, `</>` icon)
2. Click **Project Settings** (gear icon)
3. Scroll to **OAuth consent screen**
4. If it says "Not configured", this might be the issue
5. Try deploying the web app (Step 7) - this will configure OAuth

#### Method E: Force Re-authorization
1. Go to: https://myaccount.google.com/permissions
2. Find your Google Apps Script project in "Third-party apps with account access"
3. If it's there, click **Remove**
4. Go back to Apps Script and try running `testEmail` again

**Once authorization appears:**
1. Click **Review Permissions**
2. Choose your Google account
3. You may see a warning - click **Advanced** → **Go to [Your Project Name] (unsafe)**
4. Click **Allow**
5. Check the execution log - you should see "Test email sent successfully!"
6. Check your inbox at `ride@from0to2.com` for the test email

### Step 7: Deploy as Web App (This May Trigger Authorization)
1. Click **Deploy** → **New deployment**
2. Click the gear icon ⚙️ next to "Select type"
3. Choose **Web app**
4. Set:
   - **Description**: "Form submission handler"
   - **Execute as**: **Me**
   - **Who has access**: **Anyone**
5. Click **Deploy**
6. **If authorization prompt appears during deployment:**
   - Click **Review Permissions**
   - Choose your Google account
   - Click **Advanced** → **Go to [Project Name] (unsafe)** → **Allow**
7. **Copy the Web App URL** - it will look like:
   `https://script.google.com/macros/s/AKfycbz.../exec`
8. **IMPORTANT**: Make sure this URL matches the one in your HTML files!

**After deploying, test again:**
- Go back and try Step 6 (testEmail) again
- The authorization may have been triggered during deployment

### Step 8: Verify URL in HTML Files
1. Check that your HTML files (`gsd.html`, `hsd.html`, `quick-haul.html`) have the correct URL
2. The URL should match the one you just copied from Step 7
3. If it's different, I can help you update the HTML files

## Troubleshooting

### If authorization prompt never appears:
1. **Try deploying first** (Step 7) - deployment often triggers authorization
2. **Check execution logs** - look for "Authorization required" errors
3. **Check your Google account permissions**: https://myaccount.google.com/permissions
4. **Try a different browser** or incognito mode
5. **Make sure you're signed into the correct Google account** in Apps Script

### If you see "Authorization required" in logs but no prompt:
1. Click directly on the error message in the execution log
2. This should open the authorization flow
3. If not, try Method E in Step 6 (remove and re-authorize)

### If testEmail runs but emails still don't send:
1. Check the **Executions** tab (clock icon in left sidebar)
2. Look for errors in recent executions
3. Check if the error mentions "MailApp" or "sendEmail"
4. Verify the email address `ride@from0to2.com` is correct
5. Try sending a test email to your own email first to verify MailApp works

### If the sheet name is wrong:
- Check your actual sheet tab name
- Update `SHEET_NAME` in the script
- The script will try to find the sheet by GID (2065220436) as a backup

### If nothing works - Alternative Solution:
If Google Apps Script authorization continues to be problematic, consider using **EmailJS** instead (see `EMAIL_FIX_GUIDE.md` for details). EmailJS is often more reliable for email sending and doesn't require complex authorization.

## That's It!

Once you complete these steps:
- ✅ Forms will submit to Google Sheets
- ✅ Emails will be sent to `ride@from0to2.com`
- ✅ All data will be logged properly

If you run into any issues, let me know!

