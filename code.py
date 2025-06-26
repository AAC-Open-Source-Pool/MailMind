import pandas as pd
import numpy as np
import os
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# 1. Load dataset
df = pd.read_csv('dataset.csv')

# 2. Preprocess text fields
def preprocess_text(text):
    if pd.isna(text):
        return ""
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(f'[{string.punctuation}]', '', text)
    text = re.sub('\d+', '', text)
    return text

# 3. Combine subject and body, handle missing values
df['subject'] = df['subject'].fillna('')
df['body'] = df['body'].fillna('')
df['combined_text'] = df['subject'] + ' ' + df['body']
df['combined_text'] = df['combined_text'].apply(preprocess_text)

# 4. Remove rows with missing spam label
print("NaN in is_spam before:", df['is_spam'].isna().sum())
df = df.dropna(subset=['is_spam'])
print("NaN in is_spam after:", df['is_spam'].isna().sum())

# 5. Split data for spam classification
X = df['combined_text']
y_spam = df['is_spam'].astype(int)  # ensure labels are int (0/1)
X_train, X_test, y_train, y_test = train_test_split(X, y_spam, test_size=0.2, random_state=42)

# 6. Spam classification pipeline
spam_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000)),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])
spam_pipeline.fit(X_train, y_train)

# 7. Evaluate spam model
y_pred = spam_pipeline.predict(X_test)
print("Spam Classification Report:")
print(classification_report(y_test, y_pred))

# 8. Prepare event data (non-spam only), remove missing event labels
non_spam_df = df[df['is_spam'] == 0].copy()
print("NaN in is_event before:", non_spam_df['is_event'].isna().sum())
non_spam_df = non_spam_df.dropna(subset=['is_event'])
print("NaN in is_event after:", non_spam_df['is_event'].isna().sum())

X_event = non_spam_df['combined_text']
y_event = non_spam_df['is_event'].astype(int)
Xe_train, Xe_test, ye_train, ye_test = train_test_split(X_event, y_event, test_size=0.2, random_state=42)

# 9. Event classification pipeline
event_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000)),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])
event_pipeline.fit(Xe_train, ye_train)

# 10. Evaluate event model
ye_pred = event_pipeline.predict(Xe_test)
print("\nEvent Classification Report:")
print(classification_report(ye_test, ye_pred))

# 11. Storage function
def classify_and_store(email_dict, spam_model, event_model):
    """Classifies and stores emails in appropriate folders"""
    # Create folders if they don't exist
    os.makedirs('spam_emails', exist_ok=True)
    os.makedirs('event_emails', exist_ok=True)
    os.makedirs('other_emails', exist_ok=True)
    
    # Validate and sanitize input
    required_keys = ['id', 'from', 'to', 'subject', 'body']
    for key in required_keys:
        if key not in email_dict or pd.isna(email_dict[key]):
            email_dict[key] = ""
    
    # Preprocess email
    combined_text = str(email_dict['subject']) + ' ' + str(email_dict['body'])
    cleaned_text = preprocess_text(combined_text)
    
    # Classify spam
    is_spam = spam_model.predict([cleaned_text])[0]
    
    if is_spam:
        email_dict['category'] = 'spam'
        with open(f"spam_emails/email_{email_dict['id']}.txt", 'w', encoding='utf-8') as f:
            f.write(f"From: {email_dict['from']}\nTo: {email_dict['to']}\nSubject: {email_dict['subject']}\n\n{email_dict['body']}")
        return 'spam'
    
    # Classify event if not spam
    is_event = event_model.predict([cleaned_text])[0]
    
    if is_event:
        email_dict['category'] = 'event'
        with open(f"event_emails/email_{email_dict['id']}.txt", 'w', encoding='utf-8') as f:
            f.write(f"From: {email_dict['from']}\nTo: {email_dict['to']}\nSubject: {email_dict['subject']}\n\n{email_dict['body']}")
        return 'event'
    
    email_dict['category'] = 'other'
    with open(f"other_emails/email_{email_dict['id']}.txt", 'w', encoding='utf-8') as f:
        f.write(f"From: {email_dict['from']}\nTo: {email_dict['to']}\nSubject: {email_dict['subject']}\n\n{email_dict['body']}")
    return 'other'

# 12. Example usage
if __name__ == "__main__":
    # Example test emails
    test_emails = [
        {
            'id': 101,
            'from': 'spammer@phish.com',
            'to': 'user@example.com',
            'subject': 'Win a Free iPhone!',
            'body': 'Click here to claim your prize now!'
        },
        {
            'id': 102,
            'from': 'hr@company.com',
            'to': 'staff@example.com',
            'subject': 'Invitation: Annual Townhall Meeting',
            'body': 'Join us for the annual townhall meeting on July 10th at 2 PM.'
        },
        {
            'id': 103,
            'from': 'colleague@work.com',
            'to': 'user@example.com',
            'subject': 'Lunch plans',
            'body': 'Do you want to grab lunch together today?'
        }
    ]
    for email in test_emails:
        result = classify_and_store(email, spam_pipeline, event_pipeline)
        print(f"Email {email['id']} classified as: {result}")
from sklearn.metrics import confusion_matrix
print("Spam Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Event Confusion Matrix:")
print(confusion_matrix(ye_test, ye_pred))
from sklearn.model_selection import cross_val_score

scores = cross_val_score(spam_pipeline, X, y_spam, cv=5)
print("Cross-validation scores:", scores)
print("Mean accuracy:", scores.mean())
print(df['is_spam'].value_counts())
print(non_spam_df['is_event'].value_counts())
test_emails = [
    {
        'id': 201,
        'from': 'lottery@bigwinnings.com',
        'to': 'you@example.com',
        'subject': 'Congratulations! You have won $1,000,000',
        'body': 'Dear user, You have been selected as the lucky winner of our grand prize! To claim your winnings, please reply with your bank details immediately.'
    },
    {
        'id': 202,
        'from': 'phishing@securebank-alert.com',
        'to': 'you@example.com',
        'subject': 'URGENT: Account Suspended',
        'body': 'Your bank account has been suspended due to suspicious activity. Click the link below to verify your account and restore access: http://fakebank.com/verify'
    },
    {
        'id': 203,
        'from': 'events@university.edu',
        'to': 'student@example.com',
        'subject': 'Invitation: Guest Lecture on AI',
        'body': 'Dear student, You are invited to attend a guest lecture on Artificial Intelligence scheduled for July 30th at 3 PM in the main auditorium.'
    },
    {
        'id': 204,
        'from': 'friend@gmail.com',
        'to': 'you@example.com',
        'subject': 'Catching up!',
        'body': 'Hey! It’s been a while since we last talked. Want to grab coffee this weekend?'
    }
]
for email in test_emails:
    result = classify_and_store(email, spam_pipeline, event_pipeline)
    print(f"Email {email['id']} classified as: {result}")
