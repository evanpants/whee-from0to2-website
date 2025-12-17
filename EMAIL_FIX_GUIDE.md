# Email Sending Fix Guide

## Problem
Forms are successfully submitting to Google Sheets, but emails are not being sent to `ride@from0to2.com`.

## Quick Solution: Fix Google Apps Script Email Permissions

The most likely issue is that your Google Apps Script needs to be authorized to send emails. Here's how to fix it:

### Step 1: Open Your Google Apps Script
1. Go to your Google Sheet: https://docs.google.com/spreadsheets/d/1rlA9JrJyElCr9NEs31Qsa9QA-4GeSQVX5CQJhbDggoc/edit#gid=2065220436
2. Click **Extensions** → **Apps Script**
3. You should see your script code

### Step 2: Authorize the Script
1. Click the **Run** button (▶️) in the toolbar
2. Select the `doPost` function (or any function)
3. Google will ask for authorization - click **Review Permissions**
4. Choose your Google account
5. Click **Advanced** → **Go to [Your Project Name] (unsafe)**
6. Click **Allow** to grant permissions
7. This authorizes the script to:
   - Access your Google Sheets
   - Send emails on your behalf

### Step 3: Test Email Sending
1. In the Apps Script editor, create a test function:
   ```javascript
   function testEmail() {
     MailApp.sendEmail({
       to: 'ride@from0to2.com',
       subject: 'Test Email',
       body: 'This is a test email from Google Apps Script.'
     });
   }
   ```
2. Run this function
3. Check if you receive the email

### Step 4: Check Execution Logs
1. In Apps Script, go to **Executions** (clock icon in left sidebar)
2. Look for recent executions
3. Check for any errors - they'll show what's wrong

### Step 5: Verify Email Settings
Make sure in your `doPost` function, the email code looks like this:
```javascript
MailApp.sendEmail({
  to: 'ride@from0to2.com',
  subject: subject,
  body: body
});
```

## Alternative Solution: Use EmailJS (Recommended for Quick Fix)

If Google Apps Script continues to have issues, EmailJS is a simpler, more reliable alternative:

### Why EmailJS?
- ✅ Free tier: 200 emails/month
- ✅ No server setup required
- ✅ Works directly from your website
- ✅ Easy to set up (5 minutes)
- ✅ More reliable than Google Apps Script for emails

### Setup Steps:

1. **Sign up for EmailJS** (free):
   - Go to https://www.emailjs.com/
   - Sign up with your email
   - Verify your email address

2. **Add Email Service**:
   - In EmailJS dashboard, go to **Email Services**
   - Click **Add New Service**
   - Choose **Gmail** (or your email provider)
   - Connect your Gmail account
   - Service ID will be created (e.g., `service_xxxxx`)

3. **Create Email Template**:
   - Go to **Email Templates**
   - Click **Create New Template**
   - Template name: "Bike Inquiry"
   - To Email: `ride@from0to2.com`
   - Subject: `New {{bike_model}} Inquiry - {{status}}`
   - Content:
     ```
     New inquiry received from from0to2.com:

     Bike Model: {{bike_model}}
     Status: {{status}}
     Email: {{email}}
     Name: {{name}}
     Message: {{message}}

     Additional Information:
     - Referrer: {{referrer}}
     - User Agent: {{user_agent}}
     - Timestamp: {{timestamp}}
     ```
   - Save and note the Template ID (e.g., `template_xxxxx`)

4. **Get Your Public Key**:
   - Go to **Account** → **General**
   - Copy your **Public Key** (e.g., `xxxxxxxxxxxxx`)

5. **Update Your HTML Files**:
   I can update your HTML files to use EmailJS instead of Google Apps Script. Just let me know if you want to proceed with this option.

## Recommendation

**For immediate fix**: Try Step 1-4 above to authorize Google Apps Script.

**For long-term reliability**: Consider switching to EmailJS (it's free and more reliable for this use case).

Let me know which approach you'd like to take!

