import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';
import SignUp from './components/SignUp';
import SignIn from './components/SignIn';
import OAuthCallback from './components/OAuthCallback';
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
            <Dashboard user={user} /> : 
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