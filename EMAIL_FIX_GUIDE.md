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

**If the authorization prompt doesn't appear automatically, try these methods:**

#### Method 1: Run a Test Function
1. In the Apps Script editor, add this test function at the end of your code:
   ```javascript
   function testAuthorization() {
     try {
       MailApp.sendEmail({
         to: 'ride@from0to2.com',
         subject: 'Authorization Test',
         body: 'Testing email permissions'
       });
       Logger.log('Email sent successfully');
     } catch (error) {
       Logger.log('Error: ' + error.toString());
     }
   }
   ```
2. Select `testAuthorization` from the function dropdown (top of editor)
3. Click the **Run** button (▶️)
4. **This should trigger the authorization prompt**

#### Method 2: Check Existing Authorizations
1. In Apps Script, click the **🔒 Lock icon** (or "View" → "Show execution transcript")
2. Look for any authorization errors
3. If you see "Authorization required", click it to start the authorization flow

#### Method 3: Manual Authorization
1. In Apps Script, go to **Overview** (left sidebar, icon looks like `</>`)
2. Click **Project Settings** (gear icon)
3. Scroll down to **Google Cloud Platform (GCP) Project**
4. Click **Change project**
5. This may trigger re-authorization

#### Method 4: Deploy as Web App (Triggers Authorization)
1. Click **Deploy** → **New deployment**
2. Click the gear icon ⚙️ next to "Select type"
3. Choose **Web app**
4. Set:
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Click **Deploy**
6. This process will trigger authorization prompts

#### Method 5: Check Your Google Account Permissions
1. Go to: https://myaccount.google.com/permissions
2. Look for "Apps with access to your account"
3. Find your Google Apps Script project
4. If it's there but emails still don't work, remove it and re-authorize

**Once authorization appears:**
1. Click **Review Permissions**
2. Choose your Google account
3. You may see a warning - click **Advanced** → **Go to [Your Project Name] (unsafe)**
4. Click **Allow** to grant permissions
5. This authorizes the script to:
   - Access your Google Sheets
   - Send emails on your behalf

### Step 3: Test Email Sending
1. Use the `testAuthorization` function you created in Step 2 (Method 1)
2. Or create a new test function:
   ```javascript
   function testEmail() {
     MailApp.sendEmail({
       to: 'ride@from0to2.com',
       subject: 'Test Email',
       body: 'This is a test email from Google Apps Script.'
     });
     Logger.log('Test email sent!');
   }
   ```
3. Select the function from the dropdown
4. Click **Run** (▶️)
5. Check the **Execution log** (View → Logs, or press Ctrl+Enter / Cmd+Enter)
6. Look for "Email sent successfully" or any error messages
7. Check your inbox at `ride@from0to2.com` for the test email

**If you see errors in the log:**
- "Authorization required" → Follow Step 2 methods above
- "Invalid email" → Check the email address is correct
- "Service invoked too many times" → Wait a few minutes and try again

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

