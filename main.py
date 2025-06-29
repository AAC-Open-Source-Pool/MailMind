import os
import base64
import json
import requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email import message_from_bytes

# Scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]

# Load credentials and authenticate
def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Fetch unread emails from Gmail
def fetch_emails(service, max_results=5):
    result = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread', maxResults=max_results).execute()
    messages = result.get('messages', [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
        msg_str = base64.urlsafe_b64decode(msg_data['raw'].encode('ASCII'))
        mime_msg = message_from_bytes(msg_str)
        subject = mime_msg['subject']
        payload = mime_msg.get_payload()
        if isinstance(payload, list):
            body = payload[0].get_payload(decode=True).decode(errors='ignore')
        else:
            body = payload if isinstance(payload, str) else payload.decode(errors='ignore')
        emails.append({'subject': subject, 'body': body})
    return emails

# Send prompt to local Ollama
def analyze_email_with_ollama(email_text):
    prompt = f"""
You're an assistant. Analyze this email and return a JSON with:
- "spam": true or false
- "type": "event" or "info"
- "summary": a short summary
- "urgency": from 1 (low) to 5 (high)
- "event_details": with "title", "date", "time", and "location" if it's an event

Email:
\"\"\"
{email_text}
\"\"\"
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    content = response.json()["response"]
    
    try:
        data = json.loads(content.strip())
    except json.JSONDecodeError:
        print("⚠️ Couldn't parse response. Raw model output:")
        print(content)
        return None
    return data

# Add event to Google Calendar
def add_to_calendar(service, event_details):
    try:
        start_time = datetime.strptime(event_details["date"] + " " + event_details["time"], "%Y-%m-%d %H:%M")
        end_time = start_time + timedelta(hours=1)
        event = {
            'summary': event_details.get("title", "Untitled Event"),
            'location': event_details.get("location", ""),
            'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        }
        service.events().insert(calendarId='primary', body=event).execute()
        print(f"📅 Event added: {event['summary']} at {event['start']['dateTime']}")
    except Exception as e:
        print("⚠️ Failed to add event:", e)

# Main pipeline
def main():
    creds = authenticate()
    gmail = build('gmail', 'v1', credentials=creds)
    calendar = build('calendar', 'v3', credentials=creds)

    emails = fetch_emails(gmail)
    if not emails:
        print("📭 No unread emails found.")
        return

    for email in emails:
        print(f"\n📨 Subject: {email['subject']}")
        analysis = analyze_email_with_ollama(email['body'])

        if not analysis:
            continue

        if analysis.get("spam", False):
            print("🚫 Marked as spam.")
            continue

        print(f"📝 Summary: {analysis['summary']}")
        print(f"📊 Type: {analysis['type']}, Urgency: {analysis['urgency']}")

        if analysis['type'] == "event":
            add_to_calendar(calendar, analysis["event_details"])

if __name__ == '__main__':
    main()
