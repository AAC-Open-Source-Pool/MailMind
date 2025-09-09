from google import genai
import json, re, datetime
from pymongo import MongoClient
from calender import setcalender  # import your calendar module here

client = genai.Client(api_key="AIzaSyDbLNXRxyqlvD-VOOsb-QLXh3cd8a4YE7U")

db_client = MongoClient("mongodb+srv://umeshyenugula2007:K5vP3vmqxv8JwOjX@emails.yy5amep.mongodb.net/")
db = db_client['Emails']

def extract_event(email_body):
    if isinstance(email_body, tuple):
        email_body = email_body[0]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
Extract event details from this email and return JSON with keys:
"title", "date", "start_time", "end_time", "location", "description". 
Email:
\"\"\"{email_body}\"\"\""""
    )
    text = response.text.strip()
    match = re.search(r'({.*})', text, re.DOTALL)
    if not match:
        return None
    try:
        event = json.loads(match.group(1))
        if not event.get("title") or not event.get("date"):
            return None
        # Fill missing times
        if not event.get("start_time"):
            event["start_time"] = "00:00"
        if not event.get("end_time"):
            event["end_time"] = "01:00"
        return event
    except:
        return None

def summarize_email(email_body):
    if isinstance(email_body, tuple):
        email_body = email_body[0]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
Summarize the following email in 2-3 sentences:
\"\"\"{email_body}\"\"\""""
    )
    return response.text.strip()

def cache_and_add_event(user_id, email_id, creds, event_details):
    """
    Save the event in MongoDB and add to Google Calendar immediately.
    Returns the Google Calendar link if successful.
    """
    events_collection = db[f"{user_id}_events"]
    existing = events_collection.find_one({"email_id": email_id})
    if not existing:
        events_collection.insert_one({
            "email_id": email_id,
            **event_details,
            "added_at": datetime.datetime.utcnow()
        })

    # Add to Google Calendar and return link
    try:
        cal_link = setcalender.add_events_to_calendar(creds, event_details)
        return cal_link
    except Exception as e:
        print(f"[ERROR] Adding to calendar: {e}")
        return None
