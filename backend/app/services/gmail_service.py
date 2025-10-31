from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional
import base64
from email.mime.text import MIMEText
import logging

logger = logging.getLogger(__name__)

class GmailService:
    """Gmail API service for email operations"""
    
    def __init__(self, credentials: Dict):
        """Initialize Gmail service with user credentials"""
        self.creds = Credentials(
            token=credentials.get('access_token'),
            refresh_token=credentials.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=credentials.get('client_id'),
            client_secret=credentials.get('client_secret')
        )
        self.service = build('gmail', 'v1', credentials=self.creds)
    
    async def fetch_emails(self, max_results: int = 100, query: str = "") -> List[Dict]:
        """
        Fetch emails from Gmail inbox
        
        Args:
            max_results: Maximum number of emails to fetch
            query: Gmail search query (e.g., 'is:unread', 'from:example@gmail.com')
        
        Returns:
            List of email dictionaries
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q=query
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = await self.get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            logger.info(f"Fetched {len(emails)} emails")
            return emails
            
        except HttpError as error:
            logger.error(f"Gmail API error: {error}")
            raise
    
    async def get_email_details(self, message_id: str) -> Optional[Dict]:
        """Get detailed information about a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            # Extract key information
            email_data = {
                'id': message['id'],
                'thread_id': message['threadId'],
                'subject': self._get_header(headers, 'Subject'),
                'from': self._get_header(headers, 'From'),
                'to': self._get_header(headers, 'To'),
                'date': self._get_header(headers, 'Date'),
                'snippet': message.get('snippet', ''),
                'body': self._get_email_body(message['payload']),
                'labels': message.get('labelIds', []),
                'is_unread': 'UNREAD' in message.get('labelIds', [])
            }
            
            return email_data
            
        except HttpError as error:
            logger.error(f"Error fetching email {message_id}: {error}")
            return None
    
    def _get_header(self, headers: List[Dict], name: str) -> str:
        """Extract header value by name"""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ""
    
    def _get_email_body(self, payload: Dict) -> str:
        """Extract email body from payload"""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        
        # If no parts, try direct body
        data = payload.get('body', {}).get('data', '')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8')
        
        return ""
    
    async def mark_as_read(self, message_id: str) -> bool:
        """Mark an email as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except HttpError as error:
            logger.error(f"Error marking email as read: {error}")
            return False
    
    async def add_label(self, message_id: str, label_id: str) -> bool:
        """Add a label to an email"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            return True
        except HttpError as error:
            logger.error(f"Error adding label: {error}")
            return False
    
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email"""
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw}
            ).execute()
            
            logger.info(f"Email sent to {to}")
            return True
            
        except HttpError as error:
            logger.error(f"Error sending email: {error}")
            return False
    
    async def get_unread_count(self) -> int:
        """Get count of unread emails"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread'
            ).execute()
            return results.get('resultSizeEstimate', 0)
        except HttpError as error:
            logger.error(f"Error getting unread count: {error}")
            return 0
