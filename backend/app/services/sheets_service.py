from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    """Google Sheets service for exporting email reports"""
    
    def __init__(self, credentials: Dict):
        """Initialize Sheets service with user credentials"""
        self.creds = Credentials(
            token=credentials.get('access_token'),
            refresh_token=credentials.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=credentials.get('client_id'),
            client_secret=credentials.get('client_secret'),
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=self.creds)
    
    async def create_daily_report(self, spreadsheet_id: str, analyzed_emails: List[Dict]) -> bool:
        """
        Create daily email report in Google Sheets
        
        Format:
        | Date | Total Emails | Priority | Action Required | Meetings | Time Saved | Top Sender |
        """
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Calculate metrics
            total_emails = len(analyzed_emails)
            priority_count = sum(1 for e in analyzed_emails if e.get('analysis', {}).get('priority') == 'High')
            action_count = sum(1 for e in analyzed_emails if e.get('analysis', {}).get('requires_response'))
            meeting_count = sum(1 for e in analyzed_emails if e.get('analysis', {}).get('meeting_info', {}).get('is_meeting'))
            time_saved = round(total_emails * 0.05, 1)  # Estimate 3 minutes per email
            
            # Find top sender
            senders = {}
            for email in analyzed_emails:
                sender = email.get('from', 'Unknown')
                senders[sender] = senders.get(sender, 0) + 1
            top_sender = max(senders.items(), key=lambda x: x[1])[0] if senders else "N/A"
            
            # Prepare row data
            row_data = [
                today,
                total_emails,
                priority_count,
                action_count,
                meeting_count,
                f"{time_saved} hrs",
                top_sender
            ]
            
            # Append to sheet
            body = {
                'values': [row_data]
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range='Sheet1!A:G',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Daily report added to sheet: {result.get('updates', {}).get('updatedCells', 0)} cells updated")
            return True
            
        except HttpError as error:
            logger.error(f"Sheets API error: {error}")
            return False
    
    async def create_detailed_report_sheet(self, spreadsheet_id: str, analyzed_emails: List[Dict]) -> bool:
        """Create detailed email breakdown sheet"""
        try:
            # Prepare header
            headers = ['Date', 'From', 'Subject', 'Priority', 'Category', 'Status', 'Tasks', 'Deadlines']
            
            # Prepare data rows
            rows = [headers]
            for email in analyzed_emails:
                analysis = email.get('analysis', {})
                row = [
                    email.get('date', ''),
                    email.get('from', ''),
                    email.get('subject', ''),
                    analysis.get('priority', 'Medium'),
                    analysis.get('category', 'Info'),
                    'Unread' if email.get('is_unread') else 'Read',
                    ', '.join(analysis.get('tasks', [])),
                    ', '.join(analysis.get('deadlines', []))
                ]
                rows.append(row)
            
            # Write to sheet
            body = {
                'values': rows
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Detailed!A1',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Detailed report created: {result.get('updatedCells', 0)} cells updated")
            return True
            
        except HttpError as error:
            logger.error(f"Error creating detailed report: {error}")
            return False
    
    async def create_new_spreadsheet(self, title: str = "Kesu AI Email Intelligence") -> str:
        """Create a new spreadsheet for reports"""
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                },
                'sheets': [
                    {'properties': {'title': 'Daily Summary'}},
                    {'properties': {'title': 'Detailed Report'}}
                ]
            }
            
            result = self.service.spreadsheets().create(body=spreadsheet).execute()
            spreadsheet_id = result.get('spreadsheetId')
            
            # Add headers to Daily Summary
            headers = [['Date', 'Total Emails', 'Priority', 'Action Required', 'Meetings', 'Time Saved', 'Top Sender']]
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Daily Summary!A1:G1',
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()
            
            logger.info(f"New spreadsheet created: {spreadsheet_id}")
            return spreadsheet_id
            
        except HttpError as error:
            logger.error(f"Error creating spreadsheet: {error}")
            return ""
    
    async def get_spreadsheet_url(self, spreadsheet_id: str) -> str:
        """Get shareable URL for spreadsheet"""
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
