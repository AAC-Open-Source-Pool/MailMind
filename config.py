import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Google API Configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
    
    # Firebase Configuration
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', '')
    FIREBASE_PRIVATE_KEY_ID = os.getenv('FIREBASE_PRIVATE_KEY_ID', '')
    FIREBASE_PRIVATE_KEY = os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n')
    FIREBASE_CLIENT_EMAIL = os.getenv('FIREBASE_CLIENT_EMAIL', '')
    FIREBASE_CLIENT_ID = os.getenv('FIREBASE_CLIENT_ID', '')
    FIREBASE_AUTH_URI = os.getenv('FIREBASE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth')
    FIREBASE_TOKEN_URI = os.getenv('FIREBASE_TOKEN_URI', 'https://oauth2.googleapis.com/token')
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL = os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL', 'https://www.googleapis.com/oauth2/v1/certs')
    FIREBASE_CLIENT_X509_CERT_URL = os.getenv('FIREBASE_CLIENT_X509_CERT_URL', '')
    
    # Google Generative AI
    GOOGLE_GEN_AI_API_KEY = os.getenv('GOOGLE_GEN_AI_API_KEY', 'AIzaSyAH6IMECeM07yMeeGwfhnnRsue0A4Xt2Y4')
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    # Application Configuration
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # File paths
    CREDENTIALS_FILE = 'credentials.json'
    TOKEN_FILE = 'token.json'
    FIREBASE_CREDENTIALS_FILE = 'firebase-credentials.json'
    
    # Model paths
    SPAM_MODEL_PATH = 'spam_classifier_model.pkl'
    VECTORIZER_PATH = 'vectorizer.pkl'
    NLP_MODEL_PATH = 'nlp_model.pkl'
    
    # Gmail API Scopes
    GMAIL_SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/calendar.events'
    ]
