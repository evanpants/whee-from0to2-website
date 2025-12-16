/**
 * Google Apps Script to handle form submissions from from0to2.com
 * 
 * This script receives form data and writes it to a Google Sheet,
 * then sends an email notification to ride@from0to2.com
 * 
 * SETUP INSTRUCTIONS:
 * 1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1rlA9JrJyElCr9NEs31Qsa9QA-4GeSQVX5CQJhbDggoc/edit#gid=2065220436
 * 2. Go to Extensions > Apps Script
 * 3. Delete any existing code and paste this entire file
 * 4. Replace 'YOUR_SHEET_NAME' with the actual name of the tab (gid=2065220436)
 * 5. Click "Deploy" > "New deployment"
 * 6. Select type: "Web app"
 * 7. Execute as: "Me"
 * 8. Who has access: "Anyone"
 * 9. Click "Deploy" and copy the Web App URL
 * 10. Replace 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE' in all HTML files with this URL
 */

// Configuration - UPDATE THESE VALUES
const SHEET_NAME = 'YOUR_SHEET_NAME'; // Replace with your actual sheet tab name
const EMAIL_TO = 'ride@from0to2.com';

function doPost(e) {
  try {
    // Handle both JSON and form-encoded data
    let data;
    if (e.postData && e.postData.contents) {
      try {
        // Try to parse as JSON first
        data = JSON.parse(e.postData.contents);
      } catch (jsonError) {
        // If not JSON, parse as form data
        data = {};
        const params = e.parameter;
        for (const key in params) {
          data[key] = params[key];
        }
      }
    } else {
      // Fallback to parameters
      data = e.parameter || {};
    }
    
    // Get the active spreadsheet
    const ss = SpreadsheetApp.openById('1rlA9JrJyElCr9NEs31Qsa9QA-4GeSQVX5CQJhbDggoc');
    
    // Get the specific sheet by GID (2065220436) or by name
    let sheet;
    try {
      // Try to get sheet by GID first
      const sheets = ss.getSheets();
      for (let i = 0; i < sheets.length; i++) {
        if (sheets[i].getSheetId() == 2065220436) {
          sheet = sheets[i];
          break;
        }
      }
      // If not found, try by name
      if (!sheet) {
        sheet = ss.getSheetByName(SHEET_NAME);
      }
      // If still not found, use first sheet
      if (!sheet) {
        sheet = ss.getSheets()[0];
      }
    } catch (error) {
      sheet = ss.getSheets()[0];
    }
    
    // Get headers if sheet is empty, otherwise use existing headers
    let headers = [];
    const lastRow = sheet.getLastRow();
    
    if (lastRow === 0) {
      // Sheet is empty, create headers
      headers = [
        'Timestamp',
        'Email',
        'Name',
        'Message',
        'Bike Model',
        'Status',
        'Referrer',
        'User Agent',
        'IP Address',
        'Date',
        'Time'
      ];
      sheet.appendRow(headers);
    } else {
      // Get existing headers
      headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    }
    
    // Get IP address from the request
    const ipAddress = e.parameter.ipAddress || getClientIP(e);
    
    // Get current date and time
    const now = new Date();
    const dateStr = Utilities.formatDate(now, Session.getScriptTimeZone(), 'yyyy-MM-dd');
    const timeStr = Utilities.formatDate(now, Session.getScriptTimeZone(), 'HH:mm:ss');
    
    // Prepare row data matching headers
    const rowData = [];
    headers.forEach(function(header) {
      switch(header.toLowerCase()) {
        case 'timestamp':
          rowData.push(data.timestamp || now.toISOString());
          break;
        case 'email':
          rowData.push(data.email || '');
          break;
        case 'name':
          rowData.push(data.name || '');
          break;
        case 'message':
          rowData.push(data.message || '');
          break;
        case 'bike model':
        case 'bike_model':
          rowData.push(data.bike_model || '');
          break;
        case 'status':
          rowData.push(data.status || '');
          break;
        case 'referrer':
          rowData.push(data.referrer || '');
          break;
        case 'user agent':
        case 'user_agent':
          rowData.push(data.user_agent || '');
          break;
        case 'ip address':
        case 'ip_address':
          rowData.push(ipAddress);
          break;
        case 'date':
          rowData.push(dateStr);
          break;
        case 'time':
          rowData.push(timeStr);
          break;
        default:
          rowData.push('');
      }
    });
    
    // Append the row
    sheet.appendRow(rowData);
    
    // Send email notification
    try {
      const subject = `New ${data.bike_model || 'E-bike'} Inquiry - ${data.status || 'Inquiry'}`;
      const body = `
New inquiry received from from0to2.com:

Bike Model: ${data.bike_model || 'N/A'}
Status: ${data.status || 'N/A'}
Email: ${data.email || 'N/A'}
Name: ${data.name || 'Not provided'}
Message: ${data.message || 'None'}

Additional Information:
- Referrer: ${data.referrer || 'Direct'}
- User Agent: ${data.user_agent || 'N/A'}
- IP Address: ${ipAddress}
- Timestamp: ${data.timestamp || now.toISOString()}
- Date: ${dateStr}
- Time: ${timeStr}

This information has been automatically saved to the Google Sheet.
      `;
      
      MailApp.sendEmail({
        to: EMAIL_TO,
        subject: subject,
        body: body
      });
    } catch (emailError) {
      // Log error but don't fail the request
      console.error('Email send error:', emailError);
    }
    
    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        'success': true,
        'message': 'Inquiry submitted successfully'
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        'success': false,
        'error': error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Helper function to get client IP address
function getClientIP(e) {
  // Try to get IP from various headers
  const ip = e.parameter.ipAddress || 
             e.parameter['X-Forwarded-For'] || 
             e.parameter['X-Real-IP'] ||
             '';
  return ip.split(',')[0].trim() || 'Unknown';
}

// Test function (optional - for testing in Apps Script editor)
function testDoPost() {
  const mockEvent = {
    postData: {
      contents: JSON.stringify({
        email: 'test@example.com',
        name: 'Test User',
        message: 'Test message',
        bike_model: 'TERN GSD',
        status: 'Available',
        referrer: 'https://from0to2.com',
        user_agent: 'Mozilla/5.0 Test',
        timestamp: new Date().toISOString()
      })
    },
    parameter: {
      ipAddress: '127.0.0.1'
    }
  };
  
  const result = doPost(mockEvent);
  Logger.log(result.getContent());
}

