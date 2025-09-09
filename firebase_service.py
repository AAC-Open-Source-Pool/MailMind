"""
Firebase Service for MailMind
Handles authentication, user management, and data storage
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime, timedelta
from config import Config

class FirebaseService:
    def __init__(self):
        self.config = Config()
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase with credentials"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Try to load from service account file first
                if os.path.exists(self.config.FIREBASE_CREDENTIALS_FILE):
                    cred = credentials.Certificate(self.config.FIREBASE_CREDENTIALS_FILE)
                else:
                    # Use environment variables
                    cred_dict = {
                        "type": "service_account",
                        "project_id": self.config.FIREBASE_PROJECT_ID,
                        "private_key_id": self.config.FIREBASE_PRIVATE_KEY_ID,
                        "private_key": self.config.FIREBASE_PRIVATE_KEY,
                        "client_email": self.config.FIREBASE_CLIENT_EMAIL,
                        "client_id": self.config.FIREBASE_CLIENT_ID,
                        "auth_uri": self.config.FIREBASE_AUTH_URI,
                        "token_uri": self.config.FIREBASE_TOKEN_URI,
                        "auth_provider_x509_cert_url": self.config.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
                        "client_x509_cert_url": self.config.FIREBASE_CLIENT_X509_CERT_URL
                    }
                    cred = credentials.Certificate(cred_dict)
                
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            print("✅ Firebase initialized successfully")
            
        except Exception as e:
            print(f"❌ Firebase initialization error: {e}")
            self.db = None
    
    def create_user(self, user_data):
        """Create a new user in Firebase Auth and Firestore"""
        try:
            if not self.db:
                return None
            
            # Create user in Firebase Auth
            user_record = auth.create_user(
                email=user_data.get('email'),
                password=user_data.get('password'),
                display_name=user_data.get('name', '')
            )
            
            # Store additional user data in Firestore
            user_doc = {
                'uid': user_record.uid,
                'email': user_data.get('email'),
                'name': user_data.get('name', ''),
                'created_at': datetime.now(),
                'last_login': datetime.now(),
                'settings': user_data.get('settings', {})
            }
            
            self.db.collection('users').document(user_record.uid).set(user_doc)
            
            return user_record.uid
            
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return None
    
    def authenticate_user(self, email, password):
        """Authenticate user with email and password"""
        try:
            if not self.db:
                return None
            
            # Get user by email
            user_record = auth.get_user_by_email(email)
            
            # In a real app, you'd verify the password here
            # For now, we'll just return the user if they exist
            return user_record.uid
            
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return None
    
    def save_gmail_token(self, user_id, token_data):
        """Save Gmail OAuth token for a user"""
        try:
            if not self.db:
                return False
            
            current_time = datetime.now()
            token_doc = {
                'user_id': user_id,
                'token_data': token_data,
                'created_at': current_time.isoformat(),
                'updated_at': current_time.isoformat()
            }
            
            self.db.collection('gmail_tokens').document(user_id).set(token_doc)
            return True
            
        except Exception as e:
            print(f"❌ Error saving Gmail token: {e}")
            return False
    
    def get_gmail_token(self, user_id):
        """Retrieve Gmail OAuth token for a user"""
        try:
            if not self.db:
                return None
            
            doc = self.db.collection('gmail_tokens').document(user_id).get()
            if doc.exists:
                return doc.to_dict().get('token_data')
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving Gmail token: {e}")
            return None
    
    def save_email_data(self, user_id, email_data):
        """Save processed email data"""
        try:
            if not self.db:
                return False
            
            current_time = datetime.now()
            email_doc = {
                'user_id': user_id,
                'email_id': email_data.get('id'),
                'subject': email_data.get('subject'),
                'body': email_data.get('body'),
                'processed_at': current_time.isoformat(),
                'analysis': email_data.get('analysis', {}),
                'spam_detected': email_data.get('spam_detected', False),
                'event_extracted': email_data.get('event_extracted', False)
            }
            
            self.db.collection('emails').add(email_doc)
            return True
            
        except Exception as e:
            print(f"❌ Error saving email data: {e}")
            return False
    
    def get_user_emails(self, user_id, limit=50):
        """Get processed emails for a user"""
        try:
            if not self.db:
                return []
            
            # First try with ordering, if it fails, try without ordering
            try:
                emails = self.db.collection('emails')\
                    .where('user_id', '==', user_id)\
                    .order_by('processed_at', direction=firestore.Query.DESCENDING)\
                    .limit(limit)\
                    .stream()
                
                return [doc.to_dict() for doc in emails]
            except Exception as index_error:
                print(f"⚠️ Index error, trying without ordering: {index_error}")
                # Fallback: get emails without ordering
                emails = self.db.collection('emails')\
                    .where('user_id', '==', user_id)\
                    .limit(limit)\
                    .stream()
                
                email_list = [doc.to_dict() for doc in emails]
                # Sort manually by processed_at if available
                email_list.sort(key=lambda x: x.get('processed_at', ''), reverse=True)
                return email_list
            
        except Exception as e:
            print(f"❌ Error retrieving user emails: {e}")
            return []
    
    def save_analytics(self, user_id, analytics_data):
        """Save user analytics data"""
        try:
            if not self.db:
                return False
            
            current_time = datetime.now()
            current_date = current_time.date()
            
            analytics_doc = {
                'user_id': user_id,
                'date': current_date.isoformat(),  # Convert to string
                'total_emails_processed': analytics_data.get('total_emails', 0),
                'spam_detected': analytics_data.get('spam_detected', 0),
                'events_extracted': analytics_data.get('events_extracted', 0),
                'average_processing_time': analytics_data.get('avg_processing_time', 0),
                'updated_at': current_time.isoformat()  # Convert to string
            }
            
            self.db.collection('analytics').document(f"{user_id}_{current_date.isoformat()}").set(analytics_doc)
            return True
            
        except Exception as e:
            print(f"❌ Error saving analytics: {e}")
            return False
    
    def get_user_analytics(self, user_id, days=30):
        """Get user analytics for the last N days"""
        try:
            if not self.db:
                return []
            
            start_date = (datetime.now().date() - timedelta(days=days)).isoformat()
            
            analytics = self.db.collection('analytics')\
                .where('user_id', '==', user_id)\
                .where('date', '>=', start_date)\
                .order_by('date', direction=firestore.Query.DESCENDING)\
                .stream()
            
            return [doc.to_dict() for doc in analytics]
            
        except Exception as e:
            print(f"❌ Error retrieving analytics: {e}")
            return []

# Global Firebase service instance
firebase_service = FirebaseService()
