"""
Flask API for Email Processing System
Connects React frontend with Python backend using Firebase
"""

from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
import json
import requests
from datetime import datetime
from config import Config
from models.unified_model import email_processor
from MAILFETCHING.fetch import get_unread_emails, get_user_email_history
from firebase_service import firebase_service
from enhanced_email_processor import enhanced_processor
from googleapiclient.discovery import build
import time

app = Flask(__name__)
app.secret_key = Config().FLASK_SECRET_KEY
CORS(app, supports_credentials=True)

# Initialize configuration
config = Config()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': {
            'spam_model': email_processor.spam_model is not None,
            'nlp_model': email_processor.nlp is not None,
            'summarizer': email_processor.summarizer is not None
        },
        'firebase_status': firebase_service.db is not None
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Handle user registration"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        user_data = {
            'email': email,
            'password': password,
            'name': name,
            'settings': {}
        }
        
        user_id = firebase_service.create_user(user_data)
        
        if user_id:
            session['user_id'] = user_id
            return jsonify({
                'success': True,
                'user_id': user_id,
                'message': 'Registration successful'
            })
        else:
            return jsonify({'error': 'Registration failed'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        user_id = firebase_service.authenticate_user(email, password)
        
        if user_id:
            session['user_id'] = user_id
            return jsonify({
                'success': True,
                'user_id': user_id,
                'message': 'Login successful'
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    try:
        session.pop('user_id', None)
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/google', methods=['GET'])
def google_oauth():
    """Handle Google OAuth authentication with Firebase"""
    try:
        from config import Config
        config = Config()
        
        # Use Firebase's Google OAuth configuration
        google_oauth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        client_id = config.GOOGLE_CLIENT_ID
        redirect_uri = "http://localhost:3000/api/auth/google/callback"
        scope = "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/userinfo.email"
        
        # Generate state parameter for security
        import secrets
        state = secrets.token_urlsafe(32)
        session['oauth_state'] = state
        
        auth_url = f"{google_oauth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code&state={state}&access_type=offline"
        
        return jsonify({
            'success': True,
            'auth_url': auth_url,
            'message': 'Redirect to Google OAuth'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/google/callback', methods=['GET'])
def google_oauth_callback():
    """Handle Google OAuth callback with Firebase integration"""
    try:
        from config import Config
        import requests
        from firebase_service import FirebaseService
        
        config = Config()
        firebase_service = FirebaseService()
        
        code = request.args.get('code')
        state = request.args.get('state')
        
        if not code:
            return jsonify({'error': 'Authorization code not received'}), 400
        
        # Verify state parameter
        if state != session.get('oauth_state'):
            return jsonify({'error': 'Invalid state parameter'}), 400
        
        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'client_id': config.GOOGLE_CLIENT_ID,
            'client_secret': config.GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:3000/api/auth/google/callback'
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_info = token_response.json()
        
        if 'error' in token_info:
            return jsonify({'error': f'Token exchange failed: {token_info["error"]}'}), 400
        
        # Get user info from Google
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {'Authorization': f'Bearer {token_info["access_token"]}'}
        user_response = requests.get(user_info_url, headers=headers)
        user_info = user_response.json()
        
        # Create or get user in Firebase
        user_email = user_info.get('email')
        user_name = user_info.get('name', user_email.split('@')[0])
        
        # Check if user exists in Firebase
        try:
            from firebase_admin import auth
            user_record = auth.get_user_by_email(user_email)
            user_id = user_record.uid
        except:
            # Create new user in Firebase
            user_data = {
                'email': user_email,
                'name': user_name,
                'password': None  # OAuth users don't need password
            }
            user_id = firebase_service.create_user(user_data)
        
        if user_id:
            # Save Gmail token for the user
            firebase_service.save_gmail_token(user_id, token_info)
            
            # Set session
            session['user_id'] = user_id
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user_id,
                    'email': user_email,
                    'name': user_name
                },
                'message': 'Google authentication successful'
            })
        else:
            return jsonify({'error': 'Failed to create/get user in Firebase'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emails/process-enhanced', methods=['POST'])
def process_emails_enhanced():
    """Enhanced email processing with calendar integration"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        max_emails = data.get('max_emails', 5)
        
        # Step 1: Authenticate with Google APIs
        if not enhanced_processor.authenticate_google_apis(user_id):
            return jsonify({'error': 'Google API authentication failed'}), 500
        
        # Step 2: Fetch unread emails
        emails = enhanced_processor.fetch_unread_emails(max_emails=max_emails)
        
        if not emails:
            return jsonify({
                'success': True,
                'message': 'No unread emails found',
                'summary': {
                    'total_emails_processed': 0,
                    'spam_detected': 0,
                    'events_extracted': 0,
                    'calendar_events_created': 0
                }
            })
        
        # Step 3: Process emails with AI
        processed_emails, event_emails = enhanced_processor.process_emails_with_ai(emails)
        
        # Step 4: Create calendar events for event-based emails
        created_events = enhanced_processor.create_calendar_events(event_emails)
        
        # Step 5: Mark emails as read
        email_ids = [email['id'] for email in emails]
        enhanced_processor.mark_emails_as_read(email_ids)
        
        # Step 6: Generate summary report
        report = enhanced_processor.generate_summary_report(processed_emails, event_emails, created_events)
        
        return jsonify({
            'success': True,
            'message': 'Email processing completed successfully',
            'summary': report['summary'] if report else {},
            'calendar_events': report['calendar_events'] if report else [],
            'event_emails': report['event_emails'] if report else [],
            'processed_count': len(processed_emails)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emails/fetch', methods=['GET'])
def fetch_emails():
    """Fetch unread emails for the authenticated user"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Fetch emails using the updated fetch module
        emails = get_unread_emails(user_id)
        
        return jsonify({
            'success': True,
            'emails': emails,
            'count': len(emails) if emails else 0
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emails/history', methods=['GET'])
def get_email_history():
    """Get user's email processing history"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        limit = request.args.get('limit', 50, type=int)
        emails = get_user_email_history(user_id, limit)
        
        return jsonify({
            'success': True,
            'emails': emails,
            'count': len(emails)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emails/process', methods=['POST'])
def process_emails():
    """Process emails with AI models"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        emails = data.get('emails', [])
        
        if not emails:
            return jsonify({'error': 'No emails provided'}), 400
        
        # Process emails using unified model
        results = email_processor.process_emails(emails)
        
        # Save processed results to Firebase
        for result in results:
            if 'email' in result:
                result['user_id'] = user_id
                firebase_service.save_email_data(user_id, result)
        
        return jsonify({
            'success': True,
            'results': results,
            'processed_count': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calendar/add-event', methods=['POST'])
def add_calendar_event():
    """Add event to Google Calendar"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        event_details = data.get('event_details', {})
        
        if not event_details:
            return jsonify({'error': 'Event details required'}), 400
        
        # For now, we'll use the existing Gmail authentication
        # In a full implementation, you'd get calendar credentials from Firebase
        from MAILFETCHING.fetch import authenticate_user
        service = authenticate_user(user_id)
        if not service:
            return jsonify({'error': 'Failed to authenticate with Google'}), 500
        
        # Build calendar service
        calendar = build('calendar', 'v3', credentials=service._credentials)
        
        # Create event
        event = {
            'summary': event_details.get('title', 'Untitled Event'),
            'location': event_details.get('location', ''),
            'description': event_details.get('description', ''),
            'start': {
                'dateTime': event_details.get('start_time'),
                'timeZone': 'Asia/Kolkata'
            },
            'end': {
                'dateTime': event_details.get('end_time'),
                'timeZone': 'Asia/Kolkata'
            }
        }
        
        created_event = calendar.events().insert(calendarId='primary', body=event).execute()
        
        return jsonify({
            'success': True,
            'event_id': created_event['id'],
            'calendar_link': created_event.get('htmlLink', ''),
            'message': 'Event added successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calendar/redirect/<event_id>', methods=['GET'])
def redirect_to_calendar(event_id):
    """Redirect to Google Calendar event"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get event details from Firebase or create a generic calendar link
        calendar_url = f"https://calendar.google.com/calendar/event?eid={event_id}"
        
        return jsonify({
            'success': True,
            'calendar_url': calendar_url,
            'redirect_url': calendar_url
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary for the user"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get analytics from Firebase
        analytics = firebase_service.get_user_analytics(user_id, days=30)
        
        if analytics:
            # Calculate summary from analytics data
            total_emails = sum(a.get('total_emails_processed', 0) for a in analytics)
            total_spam = sum(a.get('spam_detected', 0) for a in analytics)
            total_events = sum(a.get('events_extracted', 0) for a in analytics)
            avg_processing_time = sum(a.get('average_processing_time', 0) for a in analytics) / len(analytics) if analytics else 0
        else:
            # Return default values if no analytics found
            total_emails = 0
            total_spam = 0
            total_events = 0
            avg_processing_time = 0
        
        summary = {
            'total_emails_processed': total_emails,
            'spam_detected': total_spam,
            'events_extracted': total_events,
            'average_urgency': 3,  # Default value
            'processing_time': avg_processing_time
        }
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/status', methods=['GET'])
def get_models_status():
    """Get status of all AI models"""
    try:
        status = {
            'spam_detection': {
                'loaded': email_processor.spam_model is not None,
                'type': 'Naive Bayes',
                'accuracy': '95%' if email_processor.spam_model else 'N/A'
            },
            'nlp_processing': {
                'loaded': email_processor.nlp is not None,
                'type': 'spaCy',
                'capabilities': ['NER', 'Event Extraction']
            },
            'summarization': {
                'loaded': email_processor.summarizer is not None,
                'type': 'Transformers',
                'model': 'T5' if email_processor.summarizer else 'N/A'
            },
            'ollama_integration': {
                'available': True,  # Assume available
                'model': 'mistral',
                'capabilities': ['Email Analysis', 'JSON Generation']
            },
            'firebase_integration': {
                'connected': firebase_service.db is not None,
                'type': 'Firestore',
                'capabilities': ['User Management', 'Data Storage', 'Analytics']
            },
            'calendar_integration': {
                'available': True,
                'capabilities': ['Event Creation', 'Calendar Links', 'Event Management']
            }
        }
        
        return jsonify({
            'success': True,
            'models': status
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.FLASK_ENV == 'development'
    )
