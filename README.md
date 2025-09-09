# MailMind - Intelligent Email Processing System

A comprehensive email processing system that uses AI to classify emails, extract events, and manage your inbox intelligently.

## 🏗️ Project Architecture

### Frontend (React)
- **Location**: `src/` directory
- **Purpose**: User interface for email management and analytics
- **Key Components**:
  - Dashboard: Main email processing interface
  - Analytics: Processing statistics and insights
  - Calendar: Event management
  - Authentication: User login/signup

### Backend (Python Flask)
- **Location**: `app.py`
- **Purpose**: API server connecting frontend with AI models
- **Key Features**:
  - RESTful API endpoints
  - Email processing pipeline
  - Google Calendar integration
  - User authentication

### AI Models (Unified System)
- **Location**: `models/unified_model.py`
- **Purpose**: Consolidated email processing with multiple AI models
- **Models Included**:
  - **Spam Detection**: Naive Bayes classifier
  - **Event Extraction**: spaCy NLP for named entity recognition
  - **Text Summarization**: Transformers pipeline
  - **Advanced Analysis**: Ollama integration for complex reasoning

### Email Fetching
- **Location**: `MAILFETCHING/fetch.py`
- **Purpose**: Gmail API integration for email retrieval
- **Features**:
  - OAuth2 authentication
  - MongoDB token storage
  - HTML email cleaning
  - Unread email processing

## 🔄 System Flow

1. **Authentication**: User logs in via React frontend
2. **Email Fetching**: Backend fetches unread emails from Gmail
3. **AI Processing**: Unified model processes emails through multiple AI systems:
   - Spam detection (Naive Bayes)
   - Event extraction (spaCy NLP)
   - Text summarization (Transformers)
   - Advanced analysis (Ollama)
4. **Event Management**: Extracted events are added to Google Calendar
5. **Analytics**: Processing results are stored and displayed in dashboard

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB Atlas account
- Google Cloud Platform account
- Ollama (optional, for local LLM)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Install Node.js Dependencies
```bash
npm install
```

### 3. Environment Configuration
Create a `.env` file with:
```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
MONGODB_URI=your_mongodb_connection_string
GOOGLE_GENAI_API_KEY=your_google_genai_key
FLASK_SECRET_KEY=your_secret_key
```

### 4. Google API Setup
1. Create a Google Cloud Project
2. Enable Gmail and Calendar APIs
3. Create OAuth2 credentials
4. Download `credentials.json` to project root

### 5. Run the Application

**Backend (Flask API)**:
```bash
python app.py
```

**Frontend (React)**:
```bash
npm start
```

**Direct Email Processing**:
```bash
python main.py
```

## 📁 File Structure

```
25AACR13/
├── app.py                 # Flask API server
├── main.py               # Direct email processing script
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
├── models/
│   └── unified_model.py  # Consolidated AI models
├── MAILFETCHING/
│   └── fetch.py          # Gmail integration
├── src/                  # React frontend
│   ├── App.js           # Main React component
│   └── components/      # React components
├── public/              # Static assets
├── spam_classifier_model.pkl  # Pre-trained spam model
├── vectorizer.pkl       # TF-IDF vectorizer
└── nlp_model.pkl        # spaCy NLP model
```

## 🔧 Model Conflicts Resolution

### Issues Fixed:
1. **Multiple Model Implementations**: Consolidated into `unified_model.py`
2. **Inconsistent File Paths**: Centralized in `config.py`
3. **API Key Exposure**: Moved to environment variables
4. **Missing Dependencies**: Created comprehensive `requirements.txt`
5. **Frontend-Backend Disconnect**: Added Flask API bridge
6. **Unnecessary Files**: Removed legacy models and large datasets

### Unified Model Features:
- **Fallback System**: Multiple AI models with graceful degradation
- **Error Handling**: Comprehensive error handling and logging
- **Configuration Management**: Centralized settings
- **Modular Design**: Easy to extend and maintain

## 🧪 Testing

### Test Email Processing:
```bash
python main.py
```

### Test API Endpoints:
```bash
curl http://localhost:5000/api/health
```

### Test Frontend:
```bash
npm start
# Open http://localhost:3000
```

## 📊 Analytics & Monitoring

The system provides:
- Email processing statistics
- Spam detection rates
- Event extraction accuracy
- Model performance metrics
- Processing time analytics

## 🔒 Security Features

- OAuth2 authentication
- Environment variable configuration
- Session management
- CORS protection
- Input validation

## 🚨 Troubleshooting

### Common Issues:
1. **Model Loading Errors**: Check if spaCy model is installed
2. **API Authentication**: Verify Google credentials
3. **MongoDB Connection**: Check connection string
4. **Ollama Integration**: Ensure Ollama is running locally

### Debug Mode:
Set `FLASK_ENV=development` in `.env` for detailed error messages.

## 📈 Performance Optimization

- Model caching with pickle files
- Batch email processing
- Async API endpoints
- Efficient text preprocessing
- Memory-optimized NLP models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.