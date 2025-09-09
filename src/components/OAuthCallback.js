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
        // Get the authorization code from URL parameters
        const urlParams = new URLSearchParams(location.search);
        const code = urlParams.get('code');
        const state = urlParams.get('state');
        const error = urlParams.get('error');

        if (error) {
          setStatus('error');
          setMessage('Authentication was cancelled or failed.');
          setTimeout(() => navigate('/signin'), 3000);
          return;
        }

        if (!code) {
          setStatus('error');
          setMessage('No authorization code received.');
          setTimeout(() => navigate('/signin'), 3000);
          return;
        }

        // Call the backend to exchange code for tokens
        const response = await fetch(`/api/auth/google/callback?code=${code}&state=${state}`, {
          method: 'GET',
          credentials: 'include'
        });

        const data = await response.json();

        if (data.success) {
          setStatus('success');
          setMessage('Authentication successful! Redirecting to dashboard...');
          
          // Update the auth context with the user data
          const userData = {
            id: data.user.id,
            email: data.user.email,
            fullName: data.user.name
          };
          
          // Set the user in the auth context
          setOAuthUser(userData);
          
          // Redirect to dashboard after a short delay
          setTimeout(() => navigate('/dashboard'), 2000);
        } else {
          setStatus('error');
          setMessage(data.error || 'Authentication failed.');
          setTimeout(() => navigate('/signin'), 3000);
        }
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
