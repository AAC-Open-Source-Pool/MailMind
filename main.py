from flask import Flask, render_template, session, request, redirect, url_for
import secrets
import pickle
import base64
import hashlib
import pandas as pd
from MAILFETCHING import fetch
from models import primarymodel, secondarymodel
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from emails_clean import cleanup_old_emails
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# --- Mongo ---
mongo_uri = os.getenv("mongo_uri")
Client = MongoClient(mongo_uri)
db = Client["Emails"]

# --- Flask ---
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# --- Hash helper ---
def hash_user_id(user_id):
    return hashlib.sha256(user_id.encode()).hexdigest()[:16]

# --- Background Jobs ---
def process_emails_background():
    print("[INFO] Running background email processing...")
    for user_id in db.list_collection_names():
        if user_id in ["tokens"]:
            continue
        token_doc = db["tokens"].find_one({"user_id": user_id})
        if not token_doc or "creds" not in token_doc:
            continue
        try:
            creds = pickle.loads(base64.b64decode(token_doc["creds"]))
        except:
            continue

        # Fetch new unread emails
        fetch.get_unread_emails(creds, user_id)
        emails = list(db[user_id].find({"processed": {"$ne": True}}))
        if not emails:
            continue

        df = pd.DataFrame([{"subject": e['Subject'], "body": e['Body']} for e in emails])
        classified = primarymodel.classify_emails(df)

        for email_doc, pred in zip(emails, classified):
            update = {"spam": pred['prediction'] == "Spam", "processed": True}
            if pred['prediction'] == "Not Spam":
                event = secondarymodel.extract_event(email_doc['Body'])
                if event:
                    cal_link = secondarymodel.cache_and_add_event(user_id, email_doc['_id'], creds, event)
                    update["event"] = event
                    update["cal_link"] = cal_link
                else:
                    update["summary"] = secondarymodel.summarize_email(email_doc['Body'])
            db[user_id].update_one({"_id": email_doc["_id"]}, {"$set": update})

    print("[INFO] Background job finished.")
# --- Run initial processing immediately on startup ---
from threading import Thread

def run_initial_processing():
    print("[INFO] Running initial email processing...")
    process_emails_background()
    print("[INFO] Initial email processing done.")

# Start in a separate thread so Flask can continue starting
Thread(target=run_initial_processing).start()
scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup_old_emails, trigger="interval", hours=1)
scheduler.add_job(func=process_emails_background, trigger="interval", minutes=2)
scheduler.start()

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/continuewithgoogle")
def continue_with_google():
    auth_url = fetch.authenticate_user()
    return redirect(auth_url)

# --- OAuth callback route ---
@app.route("/oauth2callback")
def oauthcallback():
    code = request.args.get("code")
    if not code:
        return redirect("/")

    user_id, creds = fetch.exchange_code_for_user(code)
    if not user_id:
        return redirect("/")

    session['user_id'] = user_id
    session['creds'] = base64.b64encode(pickle.dumps(creds)).decode()

    # Save creds in Mongo for background jobs
    db["tokens"].update_one(
        {"user_id": user_id},
        {"$set": {"creds": session['creds']}},
        upsert=True
    )

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")

    user_id = session['user_id']
    emails = list(db[user_id].find())

    all_emails = []
    event_emails = []
    summary_emails = []

    for e in emails:
        # Ensure body exists
        body = e.get("Body", "(No body)")
        subject = e.get("Subject", "(No subject)")

        # For all emails view
        all_emails.append({"subject": subject, "body": body, "spam": e.get("spam", False)})

        # For event emails view
        if "event" in e:
            event_details = e["event"]
            event_emails.append({
                "subject": subject,
                "title": event_details.get("title", ""),
                "date": event_details.get("date", ""),
                "start_time": event_details.get("start_time", ""),
                "end_time": event_details.get("end_time", ""),
                "location": event_details.get("location", ""),
                "description": event_details.get("description", ""),
                "cal_link": e.get("cal_link")  # calendar link
            })

        # For summary emails view
        if "summary" in e:
            summary_emails.append({
                "subject": subject,
                "summary": e["summary"]
            })

    return render_template(
        "dashboard.html",
        all_emails=all_emails,
        event_emails=event_emails,
        summary_emails=summary_emails,
        last_synced=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
