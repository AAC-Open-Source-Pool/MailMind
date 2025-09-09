# Mailmind - React + Flask Integration

This project integrates a React frontend with a Flask backend for an AI-powered email processing system.

## Project Structure

```
25AACR13/
├── src/                    # React frontend
│   ├── components/         # React components
│   ├── context/           # React context (AuthContext)
│   ├── services/          # API service layer
│   └── App.js             # Main React app
├── app.py                 # Flask backend API
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies
└── README.md             # Original project README
```

## Features Integrated

### Frontend (React)
- **Authentication**: Login/Register with real API calls
- **Dashboard**: Analytics, Email Gist, and Calendar views
- **Real-time Data**: Fetches data from Flask backend
- **Error Handling**: Proper loading and error states
- **Responsive Design**: Modern UI with animations

### Backend (Flask)
- **REST API**: Complete API endpoints for all features
- **Authentication**: User registration and login
- **Email Processing**: AI-powered email analysis
- **Calendar Integration**: Google Calendar events
- **Analytics**: User productivity metrics

## Setup Instructions

### 1. Install Dependencies

**Backend (Python)**
```bash
cd 25AACR13
pip install -r requirements.txt
```

**Frontend (Node.js)**
```bash
cd 25AACR13
npm install
```

### 2. Configure Backend

1. Set up Firebase credentials (see `firebase-credentials-template.json`)
2. Configure Google API credentials for email/calendar access
3. Set environment variables in `config.py`

### 3. Run the Application

**Start Flask Backend**
```bash
cd 25AACR13
python app.py
```
Backend will run on: http://localhost:5000

**Start React Frontend**
```bash
cd 25AACR13
npm start
```
Frontend will run on: http://localhost:3000

The React app is configured with a proxy to automatically forward API calls to the Flask backend.

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Email Processing
- `GET /api/emails/fetch` - Fetch unread emails
- `GET /api/emails/history` - Get email history
- `POST /api/emails/process` - Process emails with AI
- `POST /api/emails/process-enhanced` - Enhanced processing with calendar

### Analytics
- `GET /api/analytics/summary` - Get user analytics

### Calendar
- `POST /api/calendar/add-event` - Add calendar event
- `GET /api/calendar/redirect/{event_id}` - Redirect to calendar event

### System
- `GET /api/health` - Health check
- `GET /api/models/status` - AI models status

## Key Integration Features

### 1. Authentication Context
- Centralized auth state management
- Automatic token handling
- Session persistence

### 2. API Service Layer
- Centralized API calls
- Error handling and interceptors
- Automatic authentication headers

### 3. Real-time Data Fetching
- Analytics data from backend
- Email history and processing
- Calendar events integration

### 4. Error Handling
- Loading states for all components
- Error boundaries and fallbacks
- User-friendly error messages

## Development Notes

### Proxy Configuration
The React app uses a proxy configuration in `package.json` to forward API calls to the Flask backend during development.

### CORS Configuration
The Flask backend is configured with CORS to allow requests from the React frontend.

### Session Management
Uses Flask sessions for backend authentication and localStorage for frontend state persistence.

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure Flask CORS is properly configured
2. **Proxy Issues**: Check that proxy is set to `http://localhost:5000` in package.json
3. **Authentication**: Verify Firebase credentials are properly set up
4. **API Errors**: Check Flask logs for backend errors

### Debug Mode
Both frontend and backend support debug mode for development:
- React: `npm start` (development mode)
- Flask: Set `FLASK_ENV=development` in config

## Next Steps

1. **Google OAuth**: Implement real Google OAuth integration
2. **Real-time Updates**: Add WebSocket support for live updates
3. **Email Processing**: Enhance AI models and processing capabilities
4. **Mobile App**: Consider React Native for mobile support
5. **Deployment**: Set up production deployment pipeline
