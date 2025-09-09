#!/usr/bin/env python3
"""
Enhanced Email Processor with Google Calendar Integration
"""

import os
import json
import pickle
import socket
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Config
from models.unified_model import email_processor
from firebase_service import firebase_service

class EnhancedEmailProcessor:
    def __init__(self):
        self.config = Config()
        self.gmail_service = None
        self.calendar_service = None
        self.user_id = None
        
    def _find_available_port(self, start_port=8090):
        """Find an available port starting from start_port"""
        for port in range(start_port, start_port + 10):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return None
        
    def authenticate_google_apis(self, user_id):
        """Authenticate with both Gmail and Calendar APIs"""
        try:
            self.user_id = user_id
            
            # Load existing token from Firebase
            token_data = firebase_service.get_gmail_token(user_id)
            creds = None
            
            if token_data:
                try:
                    creds = pickle.loads(token_data.encode('latin1'))
                except Exception as e:
                    print(f"❌ Error loading token: {e}")
            
            # If no valid credentials, authenticate
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.config.CREDENTIALS_FILE, 
                        self.config.GMAIL_SCOPES
                    )
                    
                    # Find an available port
                    port = self._find_available_port(8090)
                    if port is None:
                        print("❌ No available ports found for OAuth server")
                        return False
                    
                    print(f"🔐 Using port {port} for OAuth authentication...")
                    creds = flow.run_local_server(port=port)
                
                # Save token to Firebase
                token_str = pickle.dumps(creds).decode('latin1')
                firebase_service.save_gmail_token(user_id, token_str)
            
            # Build services
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            self.calendar_service = build('calendar', 'v3', credentials=creds)
            
            print("✅ Google APIs authenticated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def fetch_unread_emails(self, max_emails=10):
        """Fetch unread emails from Gmail"""
        try:
            if not self.gmail_service:
                print("❌ Gmail service not initialized")
                return []
            
            # Get unread messages
            results = self.gmail_service.users().messages().list(
                userId='me', 
                q='is:unread',
                maxResults=max_emails
            ).execute()
            
            messages = results.get('messages', [])
            print(f"📧 Found {len(messages)} unread emails")
            
            emails = []
            for msg in messages:
                try:
                    # Get full message details
                    msg_data = self.gmail_service.users().messages().get(
                        userId='me', 
                        id=msg['id'],
                        format='full'
                    ).execute()
                    
                    # Extract headers
                    headers = msg_data['payload']['headers']
                    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '(No Subject)')
                    sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
                    date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
                    
                    # Extract body
                    body = self._extract_email_body(msg_data['payload'])
                    
                    email_data = {
                        'id': msg['id'],
                        'subject': subject,
                        'sender': sender,
                        'date': date,
                        'body': body,
                        'user_id': self.user_id
                    }
                    
                    emails.append(email_data)
                    
                except Exception as e:
                    print(f"❌ Error processing message {msg['id']}: {e}")
                    continue
            
            return emails
            
        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            return []
    
    def _extract_email_body(self, payload):
        """Extract clean text from email payload"""
        try:
            from bs4 import BeautifulSoup
            import re
            
            def clean_html_text(html_text):
                soup = BeautifulSoup(html_text, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                return text
            
            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('mimeType') in ['text/plain', 'text/html']:
                        data = part['body'].get('data', '')
                        if data:
                            import base64
                            decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                            if part.get('mimeType') == 'text/html':
                                return clean_html_text(decoded)
                            return decoded
            elif payload.get('mimeType') in ['text/plain', 'text/html']:
                data = payload['body'].get('data', '')
                if data:
                    import base64
                    decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    if payload.get('mimeType') == 'text/html':
                        return clean_html_text(decoded)
                    return decoded
            
            return "(No readable content found)"
            
        except Exception as e:
            print(f"❌ Error extracting email body: {e}")
            return "(Error extracting content)"
    
    def process_emails_with_ai(self, emails):
        """Process emails with AI models and extract events"""
        try:
            if not emails:
                return [], []
            
            print(f"🤖 Processing {len(emails)} emails with AI...")
            
            processed_emails = []
            event_emails = []
            
            for email in emails:
                try:
                    # Process with unified model
                    result = email_processor.process_emails([email])
                    
                    if result and len(result) > 0:
                        processed_email = result[0]
                        
                        # Check if it's an event-based email
                        if processed_email.get('event_extracted', False):
                            event_emails.append(processed_email)
                            print(f"📅 Event detected in: {email['subject']}")
                        
                        processed_emails.append(processed_email)
                        
                        # Save to Firebase
                        firebase_service.save_email_data(self.user_id, processed_email)
                    
                except Exception as e:
                    print(f"❌ Error processing email {email['id']}: {e}")
                    continue
            
            print(f"✅ Processed {len(processed_emails)} emails, found {len(event_emails)} events")
            return processed_emails, event_emails
            
        except Exception as e:
            print(f"❌ Error in AI processing: {e}")
            return [], []
    
    def create_calendar_events(self, event_emails):
        """Create Google Calendar events for event-based emails"""
        try:
            if not self.calendar_service:
                print("❌ Calendar service not initialized")
                return []
            
            if not event_emails:
                print("📅 No events to create")
                return []
            
            created_events = []
            
            for email in event_emails:
                try:
                    # Extract event details from email analysis
                    analysis = email.get('analysis', {})
                    event_details = analysis.get('event_details', {})
                    
                    if not event_details:
                        continue
                    
                    # Parse and format time
                    start_time = event_details.get('start_time', '')
                    end_time = event_details.get('end_time', '')
                    
                    # Convert relative times to ISO format
                    if start_time:
                        if 'tomorrow' in start_time.lower():
                            start_dt = datetime.now() + timedelta(days=1)
                            start_time = start_dt.strftime('%Y-%m-%dT%H:%M:%S')
                        elif 'today' in start_time.lower():
                            start_dt = datetime.now()
                            start_time = start_dt.strftime('%Y-%m-%dT%H:%M:%S')
                        elif not start_time.startswith('20'):  # Not ISO format
                            # Try to parse common time formats
                            try:
                                # Add current date if only time is provided
                                if re.match(r'\d{1,2}:\d{2}', start_time):
                                    start_dt = datetime.now().replace(
                                        hour=int(start_time.split(':')[0]),
                                        minute=int(start_time.split(':')[1])
                                    )
                                    start_time = start_dt.strftime('%Y-%m-%dT%H:%M:%S')
                            except:
                                start_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                    
                    # Set end time to 1 hour after start if not provided
                    if not end_time and start_time:
                        try:
                            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                            end_dt = start_dt + timedelta(hours=1)
                            end_time = end_dt.strftime('%Y-%m-%dT%H:%M:%S')
                        except:
                            end_time = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
                    
                    # Create calendar event
                    event = {
                        'summary': event_details.get('title', email['subject'])[:100],  # Limit length
                        'location': event_details.get('location', '')[:100],
                        'description': f"Event extracted from email: {email['subject']}\n\n{email['body'][:500]}...",
                        'start': {
                            'dateTime': start_time,
                            'timeZone': 'Asia/Kolkata',
                        },
                        'end': {
                            'dateTime': end_time,
                            'timeZone': 'Asia/Kolkata',
                        },
                        'reminders': {
                            'useDefault': False,
                            'overrides': [
                                {'method': 'email', 'minutes': 24 * 60},
                                {'method': 'popup', 'minutes': 30},
                            ],
                        },
                    }
                    
                    # Create the event
                    created_event = self.calendar_service.events().insert(
                        calendarId='primary',
                        body=event
                    ).execute()
                    
                    # Add Google Calendar link
                    event['htmlLink'] = created_event.get('htmlLink', '')
                    event['id'] = created_event.get('id', '')
                    
                    created_events.append({
                        'email_id': email['id'],
                        'email_subject': email['subject'],
                        'event_id': event['id'],
                        'event_title': event['summary'],
                        'calendar_link': event['htmlLink'],
                        'created_at': datetime.now().isoformat()
                    })
                    
                    print(f"✅ Created calendar event: {event['summary']}")
                    
                except Exception as e:
                    print(f"❌ Error creating calendar event for {email['subject']}: {e}")
                    continue
            
            return created_events
            
        except Exception as e:
            print(f"❌ Error creating calendar events: {e}")
            return []
    
    def mark_emails_as_read(self, email_ids):
        """Mark processed emails as read"""
        try:
            if not self.gmail_service:
                return False
            
            for email_id in email_ids:
                try:
                    self.gmail_service.users().messages().modify(
                        userId='me',
                        id=email_id,
                        body={'removeLabelIds': ['UNREAD']}
                    ).execute()
                except Exception as e:
                    print(f"❌ Error marking email {email_id} as read: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error marking emails as read: {e}")
            return False
    
    def generate_summary_report(self, processed_emails, event_emails, created_events):
        """Generate a summary report of the processing"""
        try:
            total_emails = len(processed_emails)
            spam_count = sum(1 for email in processed_emails if email.get('spam_detected', False))
            event_count = len(event_emails)
            calendar_events_created = len(created_events)
            
            # Get regular emails (non-spam, non-event)
            regular_emails = [email for email in processed_emails 
                            if not email.get('spam_detected', False) and not email.get('event_extracted', False)]
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'user_id': self.user_id,
                'summary': {
                    'total_emails_processed': total_emails,
                    'spam_detected': spam_count,
                    'events_extracted': event_count,
                    'calendar_events_created': calendar_events_created,
                    'regular_emails': len(regular_emails)
                },
                'calendar_events': created_events,
                'event_emails': [
                    {
                        'subject': email['subject'],
                        'event_details': email.get('analysis', {}).get('event_details', {}),
                        'calendar_link': next((e['calendar_link'] for e in created_events if e['email_id'] == email['id']), None)
                    }
                    for email in event_emails
                ],
                'regular_emails': [
                    {
                        'subject': email['subject'],
                        'sender': email.get('sender', 'Unknown'),
                        'summary': email.get('summary', 'No summary available'),
                        'entities': email.get('entities', {})
                    }
                    for email in regular_emails
                ]
            }
            
            # Save analytics to Firebase
            analytics_data = {
                'total_emails': total_emails,
                'spam_detected': spam_count,
                'events_extracted': event_count,
                'avg_processing_time': 0,
                'timestamp': datetime.now().isoformat()
            }
            firebase_service.save_analytics(self.user_id, analytics_data)
            
            return report
            
        except Exception as e:
            print(f"❌ Error generating summary report: {e}")
            return None

# Global instance
enhanced_processor = EnhancedEmailProcessor()
