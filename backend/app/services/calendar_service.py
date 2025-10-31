from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class GoogleCalendarService:
    """Google Calendar service for meeting management"""
    
    def __init__(self, credentials: Dict):
        """Initialize Calendar service with user credentials"""
        self.creds = Credentials(
            token=credentials.get('access_token'),
            refresh_token=credentials.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=credentials.get('client_id'),
            client_secret=credentials.get('client_secret'),
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        self.service = build('calendar', 'v3', credentials=self.creds)
    
    async def create_event_from_email(self, meeting_info: Dict, email_data: Dict) -> Optional[str]:
        """
        Create calendar event from email meeting information
        
        Args:
            meeting_info: Extracted meeting details from email analysis
            email_data: Original email data
        
        Returns:
            Event ID if successful, None otherwise
        """
        if not meeting_info.get('is_meeting'):
            return None
        
        try:
            # Parse date and time
            start_time = self._parse_datetime(
                meeting_info.get('date'),
                meeting_info.get('time')
            )
            
            if not start_time:
                logger.warning("Could not parse meeting date/time")
                return None
            
            # Default 1-hour duration
            end_time = start_time + timedelta(hours=1)
            
            # Create event
            event = {
                'summary': email_data.get('subject', 'Meeting'),
                'description': f"From email: {email_data.get('from')}\n\n{email_data.get('body', '')[:500]}",
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            # Add location if available
            if meeting_info.get('location'):
                event['location'] = meeting_info['location']
            
            # Create event
            result = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            event_id = result.get('id')
            logger.info(f"Calendar event created: {event_id}")
            return event_id
            
        except HttpError as error:
            logger.error(f"Calendar API error: {error}")
            return None
    
    async def get_upcoming_meetings(self, days: int = 7) -> list:
        """Get upcoming meetings for the next N days"""
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            end_date = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                timeMax=end_date,
                maxResults=50,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            meetings = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                meetings.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'No title'),
                    'start': start,
                    'location': event.get('location', ''),
                    'link': event.get('htmlLink', '')
                })
            
            logger.info(f"Found {len(meetings)} upcoming meetings")
            return meetings
            
        except HttpError as error:
            logger.error(f"Error fetching meetings: {error}")
            return []
    
    async def get_todays_meetings(self) -> list:
        """Get today's meetings"""
        try:
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0).isoformat() + 'Z'
            today_end = datetime.utcnow().replace(hour=23, minute=59, second=59).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=today_start,
                timeMax=today_end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            meetings = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                meetings.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'No title'),
                    'start': start,
                    'location': event.get('location', ''),
                    'link': event.get('htmlLink', '')
                })
            
            return meetings
            
        except HttpError as error:
            logger.error(f"Error fetching today's meetings: {error}")
            return []
    
    def _parse_datetime(self, date_str: Optional[str], time_str: Optional[str]) -> Optional[datetime]:
        """Parse date and time strings into datetime object"""
        if not date_str:
            return None
        
        try:
            # Try various date formats
            date_formats = [
                '%Y-%m-%d',
                '%m/%d/%Y',
                '%d/%m/%Y',
                '%B %d, %Y',
                '%b %d, %Y'
            ]
            
            parsed_date = None
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            
            if not parsed_date:
                return None
            
            # Add time if provided
            if time_str:
                # Simple time parsing (extend as needed)
                time_parts = time_str.replace(':', ' ').split()
                if len(time_parts) >= 2:
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    
                    # Handle AM/PM
                    if 'pm' in time_str.lower() and hour < 12:
                        hour += 12
                    elif 'am' in time_str.lower() and hour == 12:
                        hour = 0
                    
                    parsed_date = parsed_date.replace(hour=hour, minute=minute)
            
            return parsed_date
            
        except Exception as error:
            logger.error(f"Error parsing datetime: {error}")
            return None
