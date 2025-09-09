# Email fetching module using Firebase instead of MongoDB
import pickle
import re
from base64 import urlsafe_b64decode
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from firebase_service import firebase_service
from config import Config

config = Config()
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def load_token_from_firebase(user_id):
    """Load Gmail token from Firebase for a user"""
    try:
        token_data = firebase_service.get_gmail_token(user_id)
        if token_data:
            # Convert token data back to credentials object
            creds = pickle.loads(token_data.encode('latin1'))
            return creds
        return None
    except Exception as e:
        print(f"[ERROR] Loading token from Firebase for user '{user_id}': {e}")
        return None

def save_token_to_firebase(user_id, creds):
    """Save Gmail token to Firebase for a user"""
    try:
        # Convert credentials to string for storage
        token_data = pickle.dumps(creds).decode('latin1')
        firebase_service.save_gmail_token(user_id, token_data)
        print(f"[INFO] Token saved to Firebase for user '{user_id}'")
    except Exception as e:
        print(f"[ERROR] Saving token to Firebase for user '{user_id}': {e}")

def authenticate_user(user_id):
    """Authenticate user with Gmail API using Firebase token storage"""
    creds = load_token_from_firebase(user_id)
    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(config.CREDENTIALS_FILE, SCOPES)
                # Use port 8090 to avoid conflicts
                creds = flow.run_local_server(port=8090)
            save_token_to_firebase(user_id, creds)
        
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"[ERROR] Authentication failed for user '{user_id}': {e}")
        return None

def clean_full_text(raw_html):
    """Clean HTML text from email content"""
    try:
        soup = BeautifulSoup(raw_html, 'html.parser')
        for tag in soup(['script', 'style', 'img', 'a']):
            tag.decompose()
        text = soup.get_text(separator=' ')
        text = re.sub(r'!.*?.*?', '', text)
        text = re.sub(r'.*?.*?', '', text)
        text = re.sub(r'[A-Za-z0-9+/=]{30,}', '', text)
        text = re.sub(r'[\u200c\u200b\u200d\u202c\u202a\u202b\u2060]', '', text)
        text = re.sub(r'[|*#]{2,}', ' ', text)
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'\\[a-zA-Z0-9]{1,10}', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    except Exception as e:
        print(f"[ERROR] Failed to clean HTML text: {e}")
        return "(Clean failed)"

def extract_plain_text(payload):
    """Extract plain text from email payload"""
    try:
        if 'parts' in payload:
            for part in payload['parts']:
                mime_type = part.get('mimeType')
                data = part.get('body', {}).get('data')
                if data:
                    try:
                        decoded_data = urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                        if mime_type in ['text/plain', 'text/html']:
                            return clean_full_text(decoded_data)
                    except Exception as e:
                        print(f"[ERROR] Decoding error in part: {e}")
                        continue
                elif 'parts' in part:
                    nested = extract_plain_text(part)
                    if nested and nested != "(No clean text found)":
                        return nested
        elif payload.get('mimeType') in ['text/plain', 'text/html']:
            data = payload.get('body', {}).get('data')
            if data:
                try:
                    decoded_data = urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    return clean_full_text(decoded_data)
                except Exception as e:
                    print(f"[ERROR] Decoding error in root payload: {e}")
        return "(No clean text found)"
    except Exception as e:
        print(f"[ERROR] Failed to extract plain text: {e}")
        return "(Extraction failed)"

def get_unread_emails(user_id):
    """Fetch unread emails for a user using Firebase authentication"""
    service = authenticate_user(user_id)
    if service is None:
        print(f"[ERROR] Gmail service not initialized for user: {user_id}")
        return []
    
    try:
        results = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = results.get('messages', [])
        print(f"\n[{user_id}] Unread Messages: {len(messages)}")
        
        emails = []
        for msg in messages:
            try:
                msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
                subject = "(No Subject)"
                
                for header in msg_data['payload']['headers']:
                    if header.get('name', '').lower() == 'subject':
                        subject = header['value']
                        break
                
                body = extract_plain_text(msg_data['payload'])
                
                email_data = {
                    'id': msg['id'],
                    'subject': subject,
                    'body': body,
                    'user_id': user_id
                }
                
                emails.append(email_data)
                
                # Mark email as read
                service.users().messages().modify(
                    userId='me',
                    id=msg['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()
                
                # Save email data to Firebase
                firebase_service.save_email_data(user_id, email_data)
                
            except Exception as e:
                print(f"[ERROR] Processing message {msg['id']}: {e}")
                continue
        
        return emails
        
    except Exception as e:
        print(f"[ERROR] Fetching unread messages: {e}")
        return []

def get_user_email_history(user_id, limit=50):
    """Get user's email processing history from Firebase"""
    try:
        return firebase_service.get_user_emails(user_id, limit)
    except Exception as e:
        print(f"[ERROR] Getting email history for user '{user_id}': {e}")
        return []