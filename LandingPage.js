import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiMail, FiCalendar, FiClock, FiTrendingUp } from 'react-icons/fi';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      {/* Background gradient overlay */}
      <div className="gradient-overlay"></div>
      
      {/* Navigation */}
      <nav className="landing-nav">
        <div className="nav-brand">
          <FiMail className="brand-icon" />
          <span className="brand-text">Mailmind</span>
        </div>
        <div className="nav-actions">
          <Link to="/signin" className="btn btn-secondary">Sign In</Link>
          <Link to="/signup" className="btn btn-primary">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <motion.div 
          className="hero-content"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="hero-title">
            Intelligent Email Management
            <span className="gradient-text"> Made Simple</span>
          </h1>
          <p className="hero-subtitle">
            Transform your inbox with AI-powered email analysis, smart calendar integration, 
            and automated event management. Save time and stay organized.
          </p>
          <div className="hero-actions">
            <Link to="/signup" className="btn btn-primary btn-large">
              Start Free Trial
            </Link>
            <Link to="/signin" className="btn btn-secondary btn-large">
              Sign In
            </Link>
          </div>
        </motion.div>

        <motion.div 
          className="hero-visual"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <div className="dashboard-preview">
            <div className="preview-header">
              <div className="preview-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            <div className="preview-content">
              <div className="preview-sidebar">
                <div className="preview-nav-item active"></div>
                <div className="preview-nav-item"></div>
                <div className="preview-nav-item"></div>
              </div>
              <div className="preview-main">
                <div className="preview-card"></div>
                <div className="preview-card"></div>
                <div className="preview-card"></div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <motion.div 
          className="features-grid"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <div className="feature-card">
            <div className="feature-icon">
              <FiMail />
            </div>
            <h3>Smart Email Analysis</h3>
            <p>AI-powered email categorization and prioritization to help you focus on what matters most.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">
              <FiCalendar />
            </div>
            <h3>Calendar Integration</h3>
            <p>Seamlessly sync with Google Calendar and automatically create events from your emails.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">
              <FiClock />
            </div>
            <h3>Time Management</h3>
            <p>Track time saved and get insights into your email productivity patterns.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">
              <FiTrendingUp />
            </div>
            <h3>Analytics Dashboard</h3>
            <p>Comprehensive analytics showing emails analyzed, time saved, and productivity trends.</p>
          </div>
        </motion.div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <motion.div 
          className="cta-content"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          <h2>Ready to Transform Your Email Experience?</h2>
          <p>Join thousands of users who have already improved their productivity with Mailmind.</p>
          <Link to="/signup" className="btn btn-primary btn-large">
            Get Started Now
          </Link>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <FiMail className="brand-icon" />
            <span className="brand-text">Mailmind</span>
          </div>
          <div className="footer-links">
            <a href="#privacy">Privacy</a>
            <a href="#terms">Terms</a>
            <a href="#support">Support</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage; 