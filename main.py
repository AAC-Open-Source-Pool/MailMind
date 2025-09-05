from flask import Flask, render_template, session, request, redirect, url_for
import secrets, pickle, base64, hashlib
import pandas as pd
from MAILFETCHING import fetch
from models import primarymodel, secondarymodel
from pymongo import MongoClient
from calender import setcalender

Client = MongoClient("mongodb+srv://umeshyenugula2007:K5vP3vmqxv8JwOjX@emails.yy5amep.mongodb.net/")
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def hash_user_id(user_id):
    return hashlib.sha256(user_id.encode()).hexdigest()[:16]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/continuewithgoogle")
def continue_with_google():
    auth_url = fetch.authenticate_user()
    return redirect(auth_url)

@app.route("/dashboard")
def dashboard():
    user_hash_in_url = request.args.get("uid")
    if 'user_id' in session and 'creds' in session:
        user_id = session['user_id']
        creds = pickle.loads(base64.b64decode(session['creds'].encode()))
    else:
        code = request.args.get("code")
        if not code:
            return "Authorization failed"
        user_id, creds = fetch.exchange_code_for_user(code)
        if not user_id:
            return "Authorization failed"
        session['user_id'] = user_id
        session['creds'] = base64.b64encode(pickle.dumps(creds)).decode()
        return redirect(url_for('dashboard', uid=hash_user_id(user_id)))
    if user_hash_in_url != hash_user_id(user_id):
        return "Authorization failed"
    fetch.get_unread_emails(creds, user_id)

    db = Client['Emails']
    emails = list(db[user_id].find())

    if not emails:
        return render_template("dashboard.html",
                               all_emails=[],
                               event_emails=[],
                               summary_emails=[])
    df = pd.DataFrame([{"subject": e['Subject'], "body": e['Body']} for e in emails])
    classified = primarymodel.classify_emails(df)

    event_emails = []
    summary_emails = []

    for email_doc, pred in zip(emails, classified):
        if pred['prediction'] == "Not Spam":
            # Use new integrated function from event_utils.py
            event = secondarymodel.extract_event(email_doc['Body'])
            if event:
                cal_link = secondarymodel.cache_and_add_event(user_id, email_doc['_id'], creds, event)
                event_emails.append({**event, "subject": email_doc['Subject'], "cal_link": cal_link})
            else:
                summary = secondarymodel.summarize_email(email_doc['Body'])
                summary_emails.append({"subject": email_doc['Subject'], "summary": summary})

    return render_template("dashboard.html",
                           all_emails=classified,
                           event_emails=event_emails,
                           summary_emails=summary_emails)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
