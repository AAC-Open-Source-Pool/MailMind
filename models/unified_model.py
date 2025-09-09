#!/usr/bin/env python3
"""
Unified Email Processing Model
Combines spam detection, event extraction, and summarization
"""

import os
import re
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import spacy
from transformers import pipeline
import google.generativeai as genai
from config import Config

class UnifiedEmailProcessor:
    def __init__(self):
        self.config = Config()
        self.spam_model = None
        self.vectorizer = None
        self.nlp = None
        self.summarizer = None
        self.gemini_model = None
        
        # Initialize components
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize all AI models"""
        try:
            print("🤖 Initializing AI models...")
            
            # Initialize spaCy for NLP
            try:
                self.nlp = spacy.load("en_core_web_sm")
                print("✅ spaCy model loaded")
            except OSError:
                print("⚠️ spaCy model not found, installing...")
                os.system("python -m spacy download en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
                print("✅ spaCy model installed and loaded")
            
            # Initialize Gemini
            if self.config.GOOGLE_GEN_AI_API_KEY:
                try:
                    genai.configure(api_key=self.config.GOOGLE_GEN_AI_API_KEY)
                    self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                    print("✅ Gemini model initialized")
                except Exception as e:
                    print(f"⚠️ Gemini initialization failed: {e}")
                    self.gemini_model = None
            
            # Initialize spam detection model
            self._initialize_spam_model()
            
            # Initialize summarizer
            try:
                self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
                print("✅ Summarizer model loaded")
            except Exception as e:
                print(f"⚠️ Summarizer initialization failed: {e}")
                self.summarizer = None
            
            print("🎉 All models initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing models: {e}")
    
    def _initialize_spam_model(self):
        """Initialize or load spam detection model"""
        try:
            model_file = "spam_model.pkl"
            
            if os.path.exists(model_file):
                # Load existing model
                with open(model_file, 'rb') as f:
                    model_data = pickle.load(f)
                    self.spam_model = model_data['model']
                    self.vectorizer = model_data['vectorizer']
                print("✅ Spam model loaded from file")
            else:
                # Create a simple spam model with sample data
                print("📝 Creating new spam detection model...")
                
                # Sample spam and ham data
                spam_texts = [
                    "URGENT: You've won $1,000,000! Click here to claim",
                    "FREE VIAGRA NOW! Limited time offer",
                    "Make money fast from home! Guaranteed income",
                    "CONGRATULATIONS! You're our lucky winner",
                    "Hot singles in your area! Meet now",
                    "Lose weight fast! Miracle diet pills",
                    "Get rich quick! Investment opportunity",
                    "FREE iPhone! Claim your prize now",
                    "Make $5000 per day working from home",
                    "Viagra for sale! Best prices guaranteed"
                ]
                
                ham_texts = [
                    "Meeting tomorrow at 2 PM in conference room",
                    "Please review the attached document",
                    "Project update: Phase 1 completed successfully",
                    "Team lunch on Friday at 12:30 PM",
                    "New software update available for download",
                    "Client presentation scheduled for next week",
                    "Budget approval needed for Q2 expenses",
                    "Training session on new procedures",
                    "Office closed for holiday on Monday",
                    "Please submit your timesheet by Friday"
                ]
                
                # Create training data
                texts = spam_texts + ham_texts
                labels = [1] * len(spam_texts) + [0] * len(ham_texts)
                
                # Create and train model
                self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
                X = self.vectorizer.fit_transform(texts)
                
                self.spam_model = MultinomialNB()
                self.spam_model.fit(X, labels)
                
                # Save model
                model_data = {
                    'model': self.spam_model,
                    'vectorizer': self.vectorizer
                }
                with open(model_file, 'wb') as f:
                    pickle.dump(model_data, f)
                
                print("✅ New spam model created and saved")
                
        except Exception as e:
            print(f"❌ Error initializing spam model: {e}")
            # Create fallback model
            self._create_fallback_spam_model()
    
    def _create_fallback_spam_model(self):
        """Create a simple fallback spam detection"""
        try:
            self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            self.spam_model = MultinomialNB()
            
            # Simple training data
            texts = ["spam", "ham"]
            labels = [1, 0]
            X = self.vectorizer.fit_transform(texts)
            self.spam_model.fit(X, labels)
            
            print("✅ Fallback spam model created")
        except Exception as e:
            print(f"❌ Fallback spam model failed: {e}")
    
    def detect_spam(self, text):
        """Detect if email is spam"""
        try:
            if not self.spam_model or not self.vectorizer:
                return False
            
            # Clean and preprocess text
            cleaned_text = self._clean_text(text)
            
            # Vectorize text
            X = self.vectorizer.transform([cleaned_text])
            
            # Predict
            prediction = self.spam_model.predict(X)[0]
            probability = self.spam_model.predict_proba(X)[0]
            
            return bool(prediction), max(probability)
            
        except Exception as e:
            print(f"Error in spam detection: {e}")
            return False, 0.0
    
    def extract_events_with_gemini(self, text):
        """Extract event details using Gemini"""
        try:
            if not self.gemini_model:
                return self._extract_events_fallback(text)
            
            prompt = f"""
            Analyze this email text and extract event information if present.
            Return the result as a JSON object with these fields:
            - event_detected: boolean
            - title: string (event title)
            - start_time: string (ISO format if found)
            - end_time: string (ISO format if found)
            - location: string
            - description: string
            
            Email text:
            {text[:2000]}
            
            Return only the JSON object, no other text.
            """
            
            response = self.gemini_model.generate_content(prompt)
            
            if response.text:
                # Try to extract JSON from response
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    import json
                    event_data = json.loads(json_match.group())
                    return event_data
            
            return self._extract_events_fallback(text)
            
        except Exception as e:
            print(f"Error in Gemini event extraction: {e}")
            return self._extract_events_fallback(text)
    
    def _extract_events_fallback(self, text):
        """Fallback event extraction using rule-based approach"""
        try:
            # Event keywords
            event_keywords = [
                'meeting', 'conference', 'event', 'workshop', 'seminar', 
                'webinar', 'appointment', 'call', 'presentation', 'training'
            ]
            
            # Time patterns
            time_patterns = [
                r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b',
                r'\b(?:tomorrow|today|next week|this week)\b',
                r'\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
                r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b'
            ]
            
            # Location patterns
            location_patterns = [
                r'\b(?:room|office|building|conference|meeting)\s+\w+\b',
                r'\b(?:at|in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
            ]
            
            text_lower = text.lower()
            
            # Check if it's an event
            is_event = any(keyword in text_lower for keyword in event_keywords)
            
            if not is_event:
                return {
                    'event_detected': False,
                    'title': '',
                    'start_time': '',
                    'end_time': '',
                    'location': '',
                    'description': ''
                }
            
            # Extract title (use subject or first sentence)
            title = text.split('.')[0][:100] if text else ''
            
            # Extract time
            start_time = ''
            for pattern in time_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    start_time = match.group()
                    break
            
            # Extract location
            location = ''
            for pattern in location_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    location = match.group()
                    break
            
            return {
                'event_detected': True,
                'title': title,
                'start_time': start_time,
                'end_time': '',
                'location': location,
                'description': text[:200]
            }
            
        except Exception as e:
            print(f"Error in fallback event extraction: {e}")
            return {
                'event_detected': False,
                'title': '',
                'start_time': '',
                'end_time': '',
                'location': '',
                'description': ''
            }
    
    def summarize_with_gemini(self, text):
        """Summarize text using Gemini"""
        try:
            if not self.gemini_model:
                return self._summarize_fallback(text)
            
            prompt = f"""
            Summarize this email text in 2-3 sentences:
            
            {text[:3000]}
            
            Provide a concise summary focusing on the main points.
            """
            
            response = self.gemini_model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            
            return self._summarize_fallback(text)
            
        except Exception as e:
            print(f"Error in Gemini summarization: {e}")
            return self._summarize_fallback(text)
    
    def _summarize_fallback(self, text):
        """Fallback summarization using simple text processing"""
        try:
            if len(text) <= 200:
                return text
            
            # Split into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= 2:
                return text[:200] + "..."
            
            # Take first 2-3 sentences
            summary_sentences = sentences[:3]
            summary = '. '.join(summary_sentences) + '.'
            
            if len(summary) > 300:
                summary = summary[:300] + "..."
            
            return summary
            
        except Exception as e:
            print(f"Error in fallback summarization: {e}")
            return text[:200] + "..." if len(text) > 200 else text
    
    def extract_entities(self, text):
        """Extract named entities using spaCy"""
        try:
            if not self.nlp:
                return {}
            
            doc = self.nlp(text[:1000])  # Limit text length
            
            entities = {
                'persons': [],
                'organizations': [],
                'locations': [],
                'dates': [],
                'times': []
            }
            
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    entities['persons'].append(ent.text)
                elif ent.label_ == 'ORG':
                    entities['organizations'].append(ent.text)
                elif ent.label_ == 'GPE' or ent.label_ == 'LOC':
                    entities['locations'].append(ent.text)
                elif ent.label_ == 'DATE':
                    entities['dates'].append(ent.text)
                elif ent.label_ == 'TIME':
                    entities['times'].append(ent.text)
            
            return entities
            
        except Exception as e:
            print(f"Error in entity extraction: {e}")
            return {}
    
    def _clean_text(self, text):
        """Clean and preprocess text"""
        try:
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            
            # Remove URLs
            text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
            
            # Remove email addresses
            text = re.sub(r'\S+@\S+', '', text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            
            return text.strip()
            
        except Exception as e:
            print(f"Error in text cleaning: {e}")
            return text
    
    def process_emails(self, emails):
        """Process a list of emails"""
        try:
            processed_emails = []
            
            for email in emails:
                try:
                    # Extract text content
                    text = email.get('body', '')
                    if not text:
                        continue
                    
                    # Clean text
                    cleaned_text = self._clean_text(text)
                    
                    # Detect spam
                    is_spam, spam_probability = self.detect_spam(cleaned_text)
                    
                    # Extract entities
                    entities = self.extract_entities(cleaned_text)
                    
                    # Extract events using Gemini
                    event_details = self.extract_events_with_gemini(cleaned_text)
                    
                    # Summarize using Gemini
                    summary = self.summarize_with_gemini(cleaned_text)
                    
                    # Determine if it's an event-based email
                    event_extracted = event_details and event_details.get('event_detected', False)
                    
                    # Create processed email object
                    processed_email = {
                        'id': email.get('id'),
                        'subject': email.get('subject', ''),
                        'sender': email.get('sender', ''),
                        'date': email.get('date', ''),
                        'body': cleaned_text,
                        'user_id': email.get('user_id'),
                        'spam_detected': is_spam,
                        'spam_probability': spam_probability,
                        'summary': summary,
                        'entities': entities,
                        'event_extracted': event_extracted,
                        'analysis': {
                            'event_details': event_details or {},
                            'sentiment': 'neutral',  # Placeholder
                            'priority': 'normal' if not is_spam else 'low'
                        },
                        'processed_at': datetime.now().isoformat()
                    }
                    
                    processed_emails.append(processed_email)
                    
                except Exception as e:
                    print(f"Error processing email {email.get('id', 'unknown')}: {e}")
                    continue
            
            return processed_emails
            
        except Exception as e:
            print(f"Error in email processing: {e}")
            return []

# Global instance
email_processor = UnifiedEmailProcessor()
