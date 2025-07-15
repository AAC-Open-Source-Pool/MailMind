# Importing necessary libraries
import spacy  # SpaCy is used for NLP tasks like Named Entity Recognition (NER)
from transformers import pipeline  # Hugging Face's pipeline for summarization
import pickle  # Pickle is used to save and load models to optimize code execution
# Step 1: Initialize and Save Models
# Load SpaCy's pre-trained model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")  # This loads the pre-trained SpaCy model 'en_core_web_sm' for English
# Save the loaded SpaCy NLP model to a pickle file to optimize loading times in future runs
with open("nlp_model.pkl", "wb") as nlp_file:  # Open 'nlp_model.pkl' file in write-binary mode
    pickle.dump(nlp, nlp_file)  # Dump the 'nlp' object (SpaCy model) to this file
# Load Hugging Face's summarizer pipeline. The pipeline is used for text summarization.
summarizer = pipeline("summarization")  # Using Hugging Face's pre-trained summarizer model
# Save the Hugging Face summarizer model to a pickle file so it can be reused without re-initializing
with open("summarizer.pkl", "wb") as summarizer_file:  # Open 'summarizer.pkl' in write-binary mode
    pickle.dump(summarizer, summarizer_file)  # Dump the summarizer pipeline object to the file

# Step 2: Load Models from Pickle Files (when needed)
# Load the SpaCy model from the pickle file for faster access in future runs
with open("nlp_model.pkl", "rb") as nlp_file:  # Open 'nlp_model.pkl' in read-binary mode
    nlp = pickle.load(nlp_file)  # Load the 'nlp' object (SpaCy model) from the pickle file
# Load the Hugging Face summarizer model from the pickle file for faster access in future runs
with open("summarizer.pkl", "rb") as summarizer_file:  # Open 'summarizer.pkl' in read-binary mode
    summarizer = pickle.load(summarizer_file)  # Load the summarizer pipeline object from the pickle file
# Step 3: Process your emails with these models
# Function to extract event-related details (e.g., date, location, and theme) from the email body
def extract_event_details(text):
    # Extract event-related details like date, time, location, and theme from the email text.
    doc = nlp(text)  # Pass the input text to the SpaCy NLP model for processing
    event_info = {'date': [], 'location': [], 'theme': []}  # Create a dictionary to store event-related details
    # Loop through the named entities detected in the text
    for ent in doc.ents:
        if ent.label_ == "DATE":  # If the entity is a date (e.g., "5th August")
            event_info['date'].append(ent.text)  # Add the date to the 'date' list
        elif ent.label_ == "GPE" or ent.label_ == "LOC":  # If the entity is a location (e.g., "San Francisco")
            event_info['location'].append(ent.text)  # Add the location to the 'location' list
    # Define a list of event-related keywords (e.g., "meeting", "conference")
    event_keywords = ["meeting", "conference", "event", "workshop", "seminar", "webinar"]
    # Loop through the event keywords to see if any of them appear in the text
    for keyword in event_keywords:
        if keyword.lower() in text.lower():  # Case-insensitive comparison
            event_info['theme'].append(keyword)  # If the keyword is found, add it to the 'theme' list

    return event_info  # Return the dictionary containing extracted event details (date, location, theme)
# Function to classify the email as event-based or not and return a summary or event details
def classify_event_or_summary(text):
    # Classifies if an email is event-based or not and returns appropriate information.
    # Define a list of keywords that signify an event-related email
    event_keywords = ["event", "meeting", "conference", "webinar", "workshop", "seminar"] 
    # Check if any of the event-related keywords are present in the text (case-insensitive)
    if any(keyword in text.lower() for keyword in event_keywords):
        # If it's event-based, extract event details from the text
        event_info = extract_event_details(text)  # Call the extract_event_details function to get event info
        return {"type": "Event-Based", "details": event_info}  # Return event info with type 'Event-Based'
    else:
        # If it's not event-based, summarize the email using the Hugging Face summarizer
        summary = summarizer(text, max_length=150, min_length=10, do_sample=False)  # Summarize the email text
        return {"type": "Not Event-Based", "summary": summary[0]['summary_text']}  # Return summary with type 'Not Event-Based'
# Example test emails to classify and extract event details or summarize the email
test_emails = [
    {
        "body": "The annual technology conference will take place in San Francisco on 5th August. Keynote speeches from industry leaders.",
        "subject": "Tech Conference 2025"
    },
    {
        "body": "Your bill for last month is ready. Please make the payment within 5 days.",
        "subject": "Bill Notification"
    },
    {
        "body": "Congrats! You have successfully completed the online coding round, and your next round is scheduled on 30th July in Bangalore.",
        "subject": "You've been selected for the next round"
    }
]
# Process the emails by classifying and extracting details
for emails in test_emails:
    # Combine the body and subject of the email and pass them to classify_event_or_summary function
    classification_result = classify_event_or_summary(emails['body'] + ' ' + emails['subject'])
    # Print the classification result, which will show whether the email is event-based or summarized
    print(classification_result)
