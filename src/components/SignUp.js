import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiMail, FiUser, FiPhone, FiCalendar, FiArrowLeft, FiEye, FiEyeOff } from 'react-icons/fi';
import './Auth.css';

const SignUp = ({ onLogin }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    dateOfBirth: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required';
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    }

    if (!formData.dateOfBirth) {
      newErrors.dateOfBirth = 'Date of birth is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    // Simulate API call
    setTimeout(() => {
      const userData = {
        id: Date.now(),
        firstName: formData.firstName,
        lastName: formData.lastName,
        email: formData.email,
        phone: formData.phone,
        dateOfBirth: formData.dateOfBirth,
        fullName: `${formData.firstName} ${formData.lastName}`,
        joinedDate: new Date().toISOString(),
        analytics: {
          timeSaved: 0,
          emailsAnalyzed: 0,
          eventsCreated: 0,
          productivityScore: 0
        }
      };

      onLogin(userData);
      navigate('/dashboard');
    }, 1500);
  };

  const handleGoogleSignUp = () => {
    setIsLoading(true);
    
    // Simulate Google OAuth
    setTimeout(() => {
      const userData = {
        id: Date.now(),
        firstName: 'Google',
        lastName: 'User',
        email: 'googleuser@example.com',
        phone: '+1234567890',
        dateOfBirth: '1990-01-01',
        fullName: 'Google User',
        joinedDate: new Date().toISOString(),
        analytics: {
          timeSaved: 0,
          emailsAnalyzed: 0,
          eventsCreated: 0,
          productivityScore: 0
        }
      };

      onLogin(userData);
      navigate('/dashboard');
    }, 1500);
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
          <Link to="/" className="back-button">
            <FiArrowLeft />
            Back to Home
          </Link>
          <div className="auth-brand">
            <FiMail className="brand-icon" />
            <span className="brand-text">Mailmind</span>
          </div>
        </div>

        <div className="auth-content">
          <h1>Create Your Account</h1>
          <p>Join Mailmind to transform your email experience</p>

          <button 
            className="btn btn-google"
            onClick={handleGoogleSignUp}
            disabled={isLoading}
          >
            <svg width="20" height="20" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Continue with Google
          </button>

          <div className="divider">
            <span>or</span>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="firstName">First Name *</label>
                <div className="input-wrapper">
                  <FiUser className="input-icon" />
                  <input
                    type="text"
                    id="firstName"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    className={`input ${errors.firstName ? 'error' : ''}`}
                    placeholder="Enter your first name"
                  />
                </div>
                {errors.firstName && <span className="error-message">{errors.firstName}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="lastName">Last Name *</label>
                <div className="input-wrapper">
                  <FiUser className="input-icon" />
                  <input
                    type="text"
                    id="lastName"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    className={`input ${errors.lastName ? 'error' : ''}`}
                    placeholder="Enter your last name"
                  />
                </div>
                {errors.lastName && <span className="error-message">{errors.lastName}</span>}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="email">Email Address *</label>
              <div className="input-wrapper">
                <FiMail className="input-icon" />
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className={`input ${errors.email ? 'error' : ''}`}
                  placeholder="Enter your email address"
                />
              </div>
              {errors.email && <span className="error-message">{errors.email}</span>}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="phone">Phone Number *</label>
                <div className="input-wrapper">
                  <FiPhone className="input-icon" />
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className={`input ${errors.phone ? 'error' : ''}`}
                    placeholder="Enter your phone number"
                  />
                </div>
                {errors.phone && <span className="error-message">{errors.phone}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="dateOfBirth">Date of Birth *</label>
                <div className="input-wrapper">
                  <FiCalendar className="input-icon" />
                  <input
                    type="date"
                    id="dateOfBirth"
                    name="dateOfBirth"
                    value={formData.dateOfBirth}
                    onChange={handleInputChange}
                    className={`input ${errors.dateOfBirth ? 'error' : ''}`}
                  />
                </div>
                {errors.dateOfBirth && <span className="error-message">{errors.dateOfBirth}</span>}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="password">Password *</label>
              <div className="input-wrapper">
                {showPassword ? <FiEyeOff className="input-icon clickable" onClick={() => setShowPassword(false)} /> : <FiEye className="input-icon clickable" onClick={() => setShowPassword(true)} />}
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  className={`input ${errors.password ? 'error' : ''}`}
                  placeholder="Create a password"
                />
              </div>
              {errors.password && <span className="error-message">{errors.password}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password *</label>
              <div className="input-wrapper">
                {showConfirmPassword ? <FiEyeOff className="input-icon clickable" onClick={() => setShowConfirmPassword(false)} /> : <FiEye className="input-icon clickable" onClick={() => setShowConfirmPassword(true)} />}
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  className={`input ${errors.confirmPassword ? 'error' : ''}`}
                  placeholder="Confirm your password"
                />
              </div>
              {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
            </div>

            <button 
              type="submit" 
              className="btn btn-primary btn-full"
              disabled={isLoading}
            >
              {isLoading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          <div className="auth-footer">
            <p>
              Already have an account? <Link to="/signin">Sign In</Link>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default SignUp; 