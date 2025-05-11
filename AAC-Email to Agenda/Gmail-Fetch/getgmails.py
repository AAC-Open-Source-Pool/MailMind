import os
import pickle
import re
from base64 import urlsafe_b64decode
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import csv
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_DIR = 'tokens'
def authenticate_user(user_id):
    token_path=os.path.join(TOKEN_DIR, f'{user_id}_tokens.json')
    creds=None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token_file:
            creds=pickle.load(token_file)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds=flow.run_local_server(port=0)
        os.makedirs(TOKEN_DIR, exist_ok=True)
        with open(token_path, 'wb') as token_file:
            pickle.dump(creds, token_file)
    service = build('gmail', 'v1', credentials=creds)
    return service
def clean_full_text(raw_html):
    soup = BeautifulSoup(raw_html,'html.parser')
    for tag in soup(['script','style','img','a']):
        tag.decompose()
    text=soup.get_text(separator=' ')
    text=re.sub(r'!.*?.*?', '', text)
    text=re.sub(r'.*?.*?', '', text)
    text=re.sub(r'[A-Za-z0-9+/=]{30,}','',text)
    text=re.sub(r'[\u200c\u200b\u200d\u202c\u202a\u202b\u2060]','',text)
    text=re.sub(r'[|*#]{2,}',' ',text)
    text=re.sub(r'https?://\S+','',text)
    text=re.sub(r'\a-zA-Z0-9]{1,10}','',text)
    text=re.sub(r'\s+',' ',text)
    return text.strip()
def extract_plain_text(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            mime_type = part.get('mimeType')
            data = part.get('body', {}).get('data')
            if data:
                decoded_data=urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                if mime_type in ['text/plain', 'text/html']:
                    return clean_full_text(decoded_data)
            elif 'parts' in part:
                nested = extract_plain_text(part)
                if nested and nested!="(No clean text found)":
                    return nested
    elif payload.get('mimeType') in ['text/plain', 'text/html']:
        data = payload.get('body', {}).get('data')
        if data:
            decoded_data = urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            return clean_full_text(decoded_data)
    return "(No clean text found)"
def get_unread_emails(user_id):
    service=authenticate_user(user_id)
    results=service.users().messages().list(userId='me', q='is:unread').execute()
    messages=results.get('messages', [])
    print(f"\n[{user_id}] Unread Messages: {len(messages)}")
    for msg in messages:
        msg_data=service.users().messages().get(userId='me', id=msg['id']).execute()
        subject="(No Subject)"
        for header in msg_data['payload']['headers']:
            if header.get('name', '').lower() == 'subject':
                subject=header['value']
                break
        body = extract_plain_text(msg_data['payload'])
        file_name='emails.csv'
        header=['Subject','Body']
        data=[subject,body]
        iffile=os.path.isfile(file_name)
        with open(file_name,mode='a',newline='',encoding='utf-8') as file:
            writer=csv.writer(file)
            if not iffile:
                writer.writerow(header)
            writer.writerow(data)
    print("Emails Extraction Completed!")
get_unread_emails('user2')