# MailMind API Requirements & Setup Guide

## 🎯 Complete API Requirements

### **1. Google Cloud Platform APIs**

#### **Required APIs:**
1. **Gmail API** - For email fetching and processing
2. **Google Calendar API** - For event creation and management
3. **Google Generative AI API** - For advanced text processing and summarization

#### **Setup Steps:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable APIs:
   - Navigate to "APIs & Services" → "Library"
   - Search and enable each API:
     - Gmail API
     - Google Calendar API
     - Generative AI API
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client IDs"
   - Application type: Desktop application
   - Download JSON file and rename to `credentials.json`
   - Place in project root directory

### **2. Google Generative AI API**

#### **Method 1: Google AI Studio (Recommended)**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key
5. Add to your `.env` file as `GOOGLE_GENAI_API_KEY`

#### **Method 2: Google Cloud Console**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" → "Library"
3. Search for "Generative AI API"
4. Click "Enable"
5. Go to "APIs & Services" → "Credentials"
6. Click "Create Credentials" → "API Key"
7. Copy the API key and add to `.env` file

### **3. Firebase Project**

#### **Setup Steps:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Enable Authentication:
   - Go to "Authentication" → "Sign-in method"
   - Enable "Email/Password"
4. Enable Firestore Database:
   - Go to "Firestore Database"
   - Click "Create database"
   - Choose "Start in test mode" (for development)
5. Create Service Account:
   - Go to "Project Settings" → "Service accounts"
   - Click "Generate new private key"
   - Download JSON file and rename to `firebase-credentials.json`
   - Place in project root directory

### **4. Ollama (Optional - Local LLM)**

#### **Setup Steps:**
1. Download from [Ollama.ai](https://ollama.ai/)
2. Install and run: `ollama serve`
3. Pull model: `ollama pull mistral`

## 📋 Required Files

### **1. credentials.json (Google OAuth)**
```json
{
  "installed": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your-client-secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

### **2. firebase-credentials.json (Firebase Service Account)**
```json
{
  "type": "service_account",
  "project_id": "your-firebase-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project.iam.gserviceaccount.com"
}
```

### **3. .env file**
```env
# Google API Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Firebase Configuration
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project.iam.gserviceaccount.com

# Google Generative AI
GOOGLE_GENAI_API_KEY=your_google_genai_api_key_here

# Ollama Configuration (Optional)
OLLAMA_BASE_URL=http://localhost:11434

# Application Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

## 🚀 Quick Setup Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 2. Update scikit-learn (fix version warnings)
pip install --upgrade scikit-learn

# 3. Test setup
python test_setup.py
```

## 📊 API Quotas and Limits

### **Google APIs:**
- **Gmail API**: 1 billion queries/day
- **Calendar API**: 1 billion queries/day
- **Generative AI**: 15 requests/minute (free tier)

### **Firebase:**
- **Firestore**: 50,000 reads/day, 20,000 writes/day (free tier)
- **Authentication**: 10,000 users (free tier)

## 🔒 Security Best Practices

1. **Never commit credentials files to version control**
2. **Use environment variables for sensitive data**
3. **Regularly rotate API keys**
4. **Monitor API usage in Google Cloud Console**
5. **Use least privilege principle for API permissions**
6. **Enable Firebase Security Rules for production**

## 🧪 Testing Each Component

### **Test Firebase Connection:**
```bash
python -c "
from firebase_service import firebase_service
print('✅ Firebase connected successfully' if firebase_service.db else '❌ Firebase connection failed')
"
```

### **Test Google Authentication:**
```bash
python -c "
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
print('✅ Google authentication successful')
"
```

### **Test Google Gen AI:**
```bash
python -c "
import google.generativeai as genai
from config import Config
config = Config()
genai.configure(api_key=config.GOOGLE_GENAI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content('Hello, world!')
print('✅ Google Gen AI working:', response.text[:50])
"
```

### **Test AI Models:**
```bash
python -c "
from models.unified_model import email_processor
print('✅ AI models loaded successfully')
"
```

## 🚨 Common Issues & Solutions

### **1. "No such file or directory: 'credentials.json'"**
- Download credentials.json from Google Cloud Console
- Place in project root directory

### **2. "Firebase initialization error"**
- Check firebase-credentials.json file
- Verify Firebase project ID and credentials
- Ensure Firestore is enabled in Firebase Console

### **3. "Google Gen AI API key error"**
- Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Add to .env file as GOOGLE_GENAI_API_KEY
- Ensure Generative AI API is enabled in Google Cloud Console

### **4. "scikit-learn version warnings"**
- Run: `pip install --upgrade scikit-learn`

### **5. "spaCy model not found"**
- Run: `python -m spacy download en_core_web_sm`

## 📞 Support Resources

- **Google Cloud Console**: https://console.cloud.google.com/
- **Firebase Console**: https://console.firebase.google.com/
- **Google AI Studio**: https://makersuite.google.com/app/apikey
- **Google Cloud APIs**: https://developers.google.com/apis-explorer
- **Firebase Documentation**: https://firebase.google.com/docs

## 🔄 Migration Summary

This version has been successfully migrated from MongoDB to Firebase:
- ✅ User authentication via Firebase Auth
- ✅ Data storage via Firestore
- ✅ Token management via Firebase
- ✅ Analytics storage via Firestore
- ❌ MongoDB dependencies removed
- ❌ MongoDB connection strings removed
