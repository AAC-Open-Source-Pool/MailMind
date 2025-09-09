import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { FiCheckCircle, FiXCircle, FiLoader } from 'react-icons/fi';
import './Auth.css';

const OAuthCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { setOAuthUser } = useAuth();
  const [status, setStatus] = useState('loading'); // 'loading', 'success', 'error'
  const [message, setMessage] = useState('Processing authentication...');

  useEffect(() => {
    const handleOAuthCallback = async () => {
      try {
        // Check if this is a redirect from successful OAuth
        const urlParams = new URLSearchParams(location.search);
        const auth = urlParams.get('auth');
        const userId = urlParams.get('user_id');
        const email = urlParams.get('email');
        const name = urlParams.get('name');

        if (auth === 'success' && userId && email) {
          setStatus('success');
          setMessage('Authentication successful! Redirecting to dashboard...');
          
          // Update the auth context with the user data
          const userData = {
            id: userId,
            email: decodeURIComponent(email),
            fullName: name ? decodeURIComponent(name) : email.split('@')[0]
          };
          
          console.log('OAuth success - setting user data:', userData);
          
          // Set the user in the auth context
          setOAuthUser(userData);
          
          // Redirect to dashboard after a short delay
          setTimeout(() => navigate('/dashboard'), 2000);
          return;
        }

        // If not a success redirect, check for error
        const error = urlParams.get('error');
        if (error) {
          setStatus('error');
          setMessage('Authentication was cancelled or failed.');
          setTimeout(() => navigate('/signin'), 3000);
          return;
        }

        // If no success or error, this might be a direct access
        setStatus('error');
        setMessage('Invalid OAuth callback. Please try signing in again.');
        setTimeout(() => navigate('/signin'), 3000);
        
      } catch (error) {
        console.error('OAuth callback error:', error);
        setStatus('error');
        setMessage('An unexpected error occurred.');
        setTimeout(() => navigate('/signin'), 3000);
      }
    };

    handleOAuthCallback();
  }, [location, navigate, setOAuthUser]);

  const getStatusIcon = () => {
    switch (status) {
      case 'loading':
        return <FiLoader className="status-icon loading" />;
      case 'success':
        return <FiCheckCircle className="status-icon success" />;
      case 'error':
        return <FiXCircle className="status-icon error" />;
      default:
        return <FiLoader className="status-icon loading" />;
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-background">
        <div className="gradient-overlay"></div>
      </div>
      
      <motion.div 
        className="auth-card"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="auth-header">
          <div className="auth-brand">
            <span className="brand-text">Mailmind</span>
          </div>
        </div>

        <div className="auth-content">
          <div className="oauth-callback">
            {getStatusIcon()}
            <h2>Google Authentication</h2>
            <p>{message}</p>
            
            {status === 'loading' && (
              <div className="loading-spinner"></div>
            )}
            
            {status === 'error' && (
              <button 
                className="btn btn-primary"
                onClick={() => navigate('/signin')}
              >
                Back to Sign In
              </button>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default OAuthCallback;
