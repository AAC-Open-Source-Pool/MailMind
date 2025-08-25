# Coded by Umesh Chandran, Used Model: Naive Bayes (A Probability Based Model)
# Import necessary libraries
import pandas as pd  # Used for data manipulation and handling CSV files
from sklearn.feature_extraction.text import TfidfVectorizer  # Converts text into a numerical representation(TF-IDF)
from sklearn.naive_bayes import MultinomialNB  # Naive Bayes model for classification
import pickle  # To save and load models for later use
# Define the function for email classification
def classify_emails(useremails):
    # 1. Load the training dataset
    # We are loading a CSV file which contains email data into a pandas DataFrame.
    df = pd.read_csv('processed.csv')  # Accessing the file
    # 2. Combine 'body' and 'subject' columns to create a new column called 'combined_text'
    # The 'combined_text' will be used as input features for the model. 
    # We're essentially combining both the body and subject of each email into one single text.
    df['comt'] = df['body'] + ' ' + df['subject']
    # 3. Prepare the data for training:
    # X is the input features (email text) and y is the target (labels indicating if the email is spam or not).
    X = df['comt']  # This is our email text (features).
    y = df['is_spam']  # This is the label: 1 if spam, 0 if not spam (target).
    # 4. Convert the combined text (emails) into numerical data:
    # We need to convert the raw text data into a format that the model can understand (numerical format).
    # TF-IDF (Term Frequency-Inverse Document Frequency) is used to convert the text data into numbers.
    # max_features=5000 means we only keep the top 5000 most important words based on their frequency.
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_tfidf = vectorizer.fit_transform(X)  # This transforms our text data into numerical vectors.
    # 5. Train the Naive Bayes model:
    # Multinomial Naive Bayes is a probabilistic classifier that's well-suited for text classification tasks.
    # It assumes that the presence of a word in an email is independent of the presence of other words.
    model = MultinomialNB()  # Modal loading
    model.fit(X_tfidf, y)  # Fit the model on the training data (email texts and their labels).
    # Save the trained model and vectorizer to disk:
    # Saving the model and vectorizer means we can load and use them in the future without retraining them.
    # We are using pickle to serialize (save) the objects into files.
    with open('spam_classifier_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)  # Save the trained model.
    with open('vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)  # Save the vectorizer (used to transform text to numbers).
    # 6. Prepare the test email data:
    # We combine the 'body' and 'subject' of the test emails in the same way we did during training.
    test_df = pd.DataFrame(useremails)
    test_df['combined_text'] = test_df['body'] + ' ' + test_df['subject']
    # 7. Load the saved model and vectorizer from disk:
    # Instead of retraining the model each time, we load the saved model and vectorizer using pickle.
    with open('spam_classifier_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)  # Load the trained model.
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)  # Load the vectorizer.
    # 8. Transform the test emails using the same vectorizer:
    # We need to convert the new test emails into the same numerical format as the training data using the loaded vectorizer.
    X_test_tfidf = vectorizer.transform(test_df['combined_text'])
    # 9. Predict using the loaded model:
    # The model is now used to classify whether the test emails are spam or not.
    predictions = model.predict(X_test_tfidf)  # Predict spam (1) or not spam (0).
    # 10. Show the predictions:
    # Finally, we print the prediction for each test email. If the model predicts '1', it means the email is spam.
    # If it predicts '0', it means the email is not spam.
    result = []
    for i, row in test_df.iterrows():
        result.append({
            'subject': row['subject'],
            'prediction': 'Spam' if predictions[i] == 1 else 'Not Spam'
        })

    return result
