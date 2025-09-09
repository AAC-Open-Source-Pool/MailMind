import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';
import SignUp from './components/SignUp';
import SignIn from './components/SignIn';
import OAuthCallback from './components/OAuthCallback';
import Layout from './components/Layout';
import AgendaPage from './components/pages/AgendaPage';
import CalendarEventsPage from './components/pages/CalendarEventsPage';
import ProcessedMailsPage from './components/pages/ProcessedMailsPage';
import './App.css';

function AppRoutes() {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <Routes>
        <Route 
          path="/" 
          element={
            isAuthenticated ? 
            <Navigate to="/dashboard" replace /> : 
            <LandingPage />
          } 
        />
        <Route 
          path="/signup" 
          element={
            isAuthenticated ? 
            <Navigate to="/dashboard" replace /> : 
            <SignUp />
          } 
        />
        <Route 
          path="/signin" 
          element={
            isAuthenticated ? 
            <Navigate to="/dashboard" replace /> : 
            <SignIn />
          } 
        />
        <Route 
          path="/api/auth/google/callback" 
          element={<OAuthCallback />} 
        />
        <Route 
          path="/dashboard" 
          element={
            isAuthenticated ? 
            <Layout user={user}>
              <Dashboard user={user} />
            </Layout> : 
            <Navigate to="/" replace />
          } 
        />
        <Route 
          path="/agenda" 
          element={
            isAuthenticated ? 
            <Layout user={user}>
              <AgendaPage user={user} />
            </Layout> : 
            <Navigate to="/" replace />
          } 
        />
        <Route 
          path="/calendar-events" 
          element={
            isAuthenticated ? 
            <Layout user={user}>
              <CalendarEventsPage user={user} />
            </Layout> : 
            <Navigate to="/" replace />
          } 
        />
        <Route 
          path="/processed-mails" 
          element={
            isAuthenticated ? 
            <Layout user={user}>
              <ProcessedMailsPage user={user} />
            </Layout> : 
            <Navigate to="/" replace />
          } 
        />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App; 