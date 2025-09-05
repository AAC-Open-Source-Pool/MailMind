# fetch.py
from bson.binary import Binary
import pickle
import re
import datetime
from base64 import urlsafe_b64decode
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from pymongo import MongoClient

Client = MongoClient("mongodb+srv://umeshyenugula2007:K5vP3vmqxv8JwOjX@emails.yy5amep.mongodb.net/")
db = Client['Emails']
TokenDB = Client['gmail_auth']
tokens_collection = TokenDB['tokens']

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar'
]
REDIRECT_URI = "http://localhost:5000/dashboard"

# ------------------ Utils ------------------
def sanitize_email_for_collection(email):
    return email.replace("@", "_at_").replace(".", "_dot_")

# ------------------ Tokens ------------------
def load_token_from_db(email):
    try:
        record = tokens_collection.find_one({"email": email})
        if record and 'token' in record:
            creds = pickle.loads(record['token'])
            return creds, record.get("user_id")
        return None, None
    except Exception as e:
        print(f"[ERROR] Loading token: {e}")
        return None, None

def save_token_to_db(email, user_id, creds):
    try:
        token_blob = Binary(pickle.dumps(creds))
        tokens_collection.update_one(
            {"email": email},
            {"$set": {"token": token_blob, "user_id": user_id}},
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR] Saving token: {e}")

# ------------------ OAuth ------------------
def authenticate_user():
    try:
        flow = Flow.from_client_secrets_file('credentials.json', scopes=SCOPES, redirect_uri=REDIRECT_URI)
        auth_url, _ = flow.authorization_url(access_type="offline", include_granted_scopes="true", prompt="consent")
        return auth_url
    except Exception as e:
        print(f"[ERROR] Authentication failed: {e}")
        return None

def exchange_code_for_user(code):
    try:
        flow = Flow.from_client_secrets_file('credentials.json', scopes=SCOPES, redirect_uri=REDIRECT_URI)
        flow.fetch_token(code=code)
        creds = flow.credentials

        gmail_service = build('gmail', 'v1', credentials=creds)
        profile = gmail_service.users().getProfile(userId='me').execute()
        email = profile.get("emailAddress", "unknown")

        # Generate a fixed user_id based on email
        user_id = sanitize_email_for_collection(email)

        # Check token DB
        old_creds, _ = load_token_from_db(email)
        if old_creds and old_creds.valid:
            return user_id, old_creds

        save_token_to_db(email, user_id, creds)
        return user_id, creds
    except Exception as e:
        print(f"[ERROR] Exchange code failed: {e}")
        return None, None

# ------------------ Email Cleaning ------------------
def clean_full_text(raw_html):
    try:
        soup = BeautifulSoup(raw_html, 'html.parser')
        for tag in soup(['script', 'style', 'img', 'a']):
            tag.decompose()
        text = soup.get_text(separator=' ')
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    except:
        return "(Clean failed)"

def extract_plain_text(payload):
    try:
        if 'parts' in payload:
            for part in payload['parts']:
                data = part.get('body', {}).get('data')
                if data:
                    decoded = urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    return clean_full_text(decoded)
        elif payload.get('mimeType') in ['text/plain', 'text/html']:
            data = payload.get('body', {}).get('data')
            if data:
                decoded = urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                return clean_full_text(decoded)
        return "(No clean text found)"
    except:
        return "(Extraction failed)"

# ------------------ Fetch Emails ------------------
def get_unread_emails(creds, user_id):
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])

    # Use sanitized user_id as collection name
    mails = db[user_id]

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        subject = next((h['value'] for h in msg_data['payload']['headers'] if h['name'].lower()=='subject'), "(No Subject)")
        body = extract_plain_text(msg_data['payload'])
        mails.insert_one({'Subject': subject, 'Body': body, 'fetched_at': datetime.datetime.utcnow()})
        service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()
