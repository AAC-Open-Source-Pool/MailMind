# Coded by Umesh Chandran, Used Model: Naive Bayes (A Probability Based Model)

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

MODEL_PATH = "spam_classifier_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"


def train_model():
    """Train the spam classifier once and save model + vectorizer."""
    print("[INFO] Training model from dataset...")

    # Load dataset
    df = pd.read_csv('datapreprocessing/processeddataset/processed.csv')

    # Combine body + subject
    df['comt'] = df['body'] + ' ' + df['subject']

    # Features and labels
    X = df['comt']
    y = df['is_spam']

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_tfidf = vectorizer.fit_transform(X)

    # Train Naive Bayes model
    model = MultinomialNB()
    model.fit(X_tfidf, y)

    # Save model + vectorizer
    with open(MODEL_PATH, 'wb') as model_file:
        pickle.dump(model, model_file)

    with open(VECTORIZER_PATH, 'wb') as vec_file:
        pickle.dump(vectorizer, vec_file)

    print("[INFO] Training complete. Model saved.")


def load_model_and_vectorizer():
    """Load saved model and vectorizer, train if not present."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        train_model()

    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)

    with open(VECTORIZER_PATH, 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)

    return model, vectorizer


def classify_emails(useremails):
    """
    Classify given emails into Spam/Not Spam.
    useremails: pandas DataFrame with 'subject' and 'body' columns
    """
    # Load pre-trained model and vectorizer
    model, vectorizer = load_model_and_vectorizer()

    # Ensure 'subject' and 'body' exist
    test_df = pd.DataFrame(useremails)
    if test_df.empty:
        return []  # no emails to classify

    test_df['subject'] = test_df.get('subject', '(No Subject)')
    test_df['body'] = test_df.get('body', '(No Body)')
    test_df['combined_text'] = test_df['body'].fillna('') + ' ' + test_df['subject'].fillna('')

    # Transform text
    X_test_tfidf = vectorizer.transform(test_df['combined_text'])

    # Predict
    predictions = model.predict(X_test_tfidf)

    # Collect results
    result = []
    for i, email in test_df.iterrows():
        result.append({
            'subject': email['subject'],
            'body': email['body'],
            'prediction': 'Spam' if predictions[i] == 1 else 'Not Spam'
        })

    return result
