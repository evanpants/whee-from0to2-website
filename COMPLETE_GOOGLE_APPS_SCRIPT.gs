/**
 * Complete Google Apps Script for from0to2.com Form Submissions
 * 
 * INSTRUCTIONS:
 * 1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1rlA9JrJyElCr9NEs31Qsa9QA-4GeSQVX5CQJhbDggoc/edit#gid=2065220436
 * 2. Go to Extensions > Apps Script
 * 3. DELETE ALL EXISTING CODE
 * 4. Copy and paste this ENTIRE file
 * 5. Replace 'website_inquiries' below with your actual sheet tab name (or leave it if that's correct)
 * 6. Click "Deploy" > "New deployment"
 * 7. Select type: "Web app"
 * 8. Execute as: "Me"
 * 9. Who has access: "Anyone"
 * 10. Click "Deploy" and copy the Web App URL
 * 11. Make sure the URL in your HTML files matches this new URL
 */

// Configuration
const SPREADSHEET_ID = '1rlA9JrJyElCr9NEs31Qsa9QA-4GeSQVX5CQJhbDggoc';
const SHEET_NAME = 'website_inquiries'; // Change this to your actual sheet tab name
const EMAIL_TO = 'ride@from0to2.com';

/**
 * Main function to handle form submissions
 */
function doPost(e) {
  try {
    // Parse the incoming data
    let data = {};
    
    if (e.postData && e.postData.contents) {
      try {
        // Try to parse as JSON
        data = JSON.parse(e.postData.contents);
      } catch (jsonError) {
        // If not JSON, parse as form data
        const params = e.parameter;
        for (const key in params) {
          data[key] = params[key];
        }
      }
    } else {
      // Fallback to parameters
      data = e.parameter || {};
    }
    
    // Get the spreadsheet
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    
    // Get the sheet by name or create it if it doesn't exist
    let sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      // Try to find sheet by GID (2065220436)
      const sheets = ss.getSheets();
      for (let i = 0; i < sheets.length; i++) {
        if (sheets[i].getSheetId() == 2065220436) {
          sheet = sheets[i];
          break;
        }
      }
      // If still not found, use first sheet
      if (!sheet) {
        sheet = ss.getSheets()[0];
      }
    }
    
    // Set up headers if sheet is empty
    const lastRow = sheet.getLastRow();
    let headers = [];
    
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
    
    // Get current date and time
    const now = new Date();
    const dateStr = Utilities.formatDate(now, Session.getScriptTimeZone(), 'yyyy-MM-dd');
    const timeStr = Utilities.formatDate(now, Session.getScriptTimeZone(), 'HH:mm:ss');
    
    // Get IP address (if available)
    const ipAddress = data.ipAddress || data.ip_address || 'Unknown';
    
    // Prepare row data matching headers
    const rowData = [];
    headers.forEach(function(header) {
      const headerLower = header.toLowerCase().trim();
      switch(headerLower) {
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
          rowData.push(data.bike_model || data['bike_model'] || '');
          break;
        case 'status':
          rowData.push(data.status || '');
          break;
        case 'referrer':
          rowData.push(data.referrer || '');
          break;
        case 'user agent':
        case 'user_agent':
          rowData.push(data.user_agent || data['user_agent'] || '');
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
    
    // Append the row to the sheet
    sheet.appendRow(rowData);
    
    // Send email notification
    try {
      const subject = 'New ' + (data.bike_model || 'E-bike') + ' Inquiry - ' + (data.status || 'Inquiry');
      const body = 'New inquiry received from from0to2.com:\n\n' +
        'Bike Model: ' + (data.bike_model || 'N/A') + '\n' +
        'Status: ' + (data.status || 'N/A') + '\n' +
        'Email: ' + (data.email || 'N/A') + '\n' +
        'Name: ' + (data.name || 'Not provided') + '\n' +
        'Message: ' + (data.message || 'None') + '\n\n' +
        'Additional Information:\n' +
        '- Referrer: ' + (data.referrer || 'Direct') + '\n' +
        '- User Agent: ' + (data.user_agent || 'N/A') + '\n' +
        '- IP Address: ' + ipAddress + '\n' +
        '- Timestamp: ' + (data.timestamp || now.toISOString()) + '\n' +
        '- Date: ' + dateStr + '\n' +
        '- Time: ' + timeStr + '\n\n' +
        'This information has been automatically saved to the Google Sheet.';
      
      MailApp.sendEmail({
        to: EMAIL_TO,
        subject: subject,
        body: body
      });
    } catch (emailError) {
      // Log error but don't fail the request
      Logger.log('Email send error: ' + emailError.toString());
      // Still return success since data was saved
    }
    
    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        'success': true,
        'message': 'Inquiry submitted successfully'
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Log the error
    Logger.log('Error in doPost: ' + error.toString());
    Logger.log('Stack trace: ' + error.stack);
    
    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        'success': false,
        'error': error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Test function to verify email sending works
 * Run this function to trigger authorization if needed
 */
function testEmail() {
  try {
    MailApp.sendEmail({
      to: EMAIL_TO,
      subject: 'Test Email from Google Apps Script',
      body: 'This is a test email. If you receive this, email sending is working correctly!'
    });
    Logger.log('Test email sent successfully!');
  } catch (error) {
    Logger.log('Error sending test email: ' + error.toString());
  }
}

/**
 * Test function to verify sheet access works
 */
function testSheetAccess() {
  try {
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
    Logger.log('Sheet accessed successfully: ' + sheet.getName());
    Logger.log('Last row: ' + sheet.getLastRow());
    return true;
  } catch (error) {
    Logger.log('Error accessing sheet: ' + error.toString());
    return false;
  }
}

