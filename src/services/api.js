import axios from 'axios';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: '/api',
  withCredentials: true, // Important for session cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth headers if needed
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      localStorage.removeItem('mailmind_user');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
};

// Email API calls
export const emailAPI = {
  fetchEmails: () => api.get('/emails/fetch'),
  getEmailHistory: (limit = 50) => api.get(`/emails/history?limit=${limit}`),
  processEmails: (emails) => api.post('/emails/process', { emails }),
  processEmailsEnhanced: (maxEmails = 5) => api.post('/emails/process-enhanced', { max_emails: maxEmails }),
};

// Calendar API calls
export const calendarAPI = {
  addEvent: (eventDetails) => api.post('/calendar/add-event', { event_details: eventDetails }),
  redirectToEvent: (eventId) => api.get(`/calendar/redirect/${eventId}`),
};

// Analytics API calls
export const analyticsAPI = {
  getSummary: () => api.get('/analytics/summary'),
};

// System API calls
export const systemAPI = {
  healthCheck: () => api.get('/health'),
  getModelsStatus: () => api.get('/models/status'),
};

export default api;
