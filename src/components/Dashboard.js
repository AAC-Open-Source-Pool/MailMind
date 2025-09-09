import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { FiMail, FiCalendar, FiClock, FiTrendingUp, FiLoader, FiList, FiInbox, FiArrowRight } from 'react-icons/fi';
import { emailAPI, systemAPI, analyticsAPI } from '../services/api';
import Analytics from './Analytics';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  const navigate = useNavigate();
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState(null);
  const [processingResults, setProcessingResults] = useState(null);
  const [systemStatus, setSystemStatus] = useState(null);
  const [dashboardStats, setDashboardStats] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Fetch dashboard stats
  const fetchDashboardStats = async () => {
    try {
      const response = await analyticsAPI.getSummary();
      setDashboardStats(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error);
      setDashboardStats({
        total_emails: 0,
        events_created: 0,
        spam_detected: 0,
        processing_time: 0,
        daily_stats: []
      });
    }
  };

  // Check system status and fetch stats on component mount
  useEffect(() => {
    const checkSystemStatus = async () => {
      try {
        const response = await systemAPI.healthCheck();
        if (response.data.status === 'healthy') {
          setSystemStatus(response.data);
        }
      } catch (error) {
        console.error('Failed to check system status:', error);
      }
    };

    checkSystemStatus();
    fetchDashboardStats();
  }, [refreshTrigger]);

  const quickActions = [
    {
      id: 'agenda',
      label: 'Email Agenda',
      icon: FiList,
      description: 'Non-event emails organized by priority',
      path: '/agenda'
    },
    {
      id: 'calendar-events',
      label: 'Calendar Events',
      icon: FiCalendar,
      description: 'View and manage your calendar events',
      path: '/calendar-events'
    },
    {
      id: 'processed-mails',
      label: 'Processed Mails',
      icon: FiInbox,
      description: 'View all processed emails with AI analysis',
      path: '/processed-mails'
    }
  ];

  const clearProcessingResults = () => {
    setProcessingResults(null);
    setProcessingStatus(null);
  };

  const navigateToPage = (path) => {
    console.log('Navigating to:', path);
    navigate(path);
  };

  return (
    <div className="dashboard-page">
      {/* Main Content */}
      <div className="dashboard-content">
        {/* Header */}
        <div className="dashboard-header">
          <h1>📊 Dashboard</h1>
          <p>Welcome back, {user?.fullName || 'User'}! Here's your email management overview.</p>
        </div>

        {/* Quick Actions */}
        <motion.div
          className="quick-actions-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <h2>🚀 Quick Actions</h2>
          <div className="quick-actions-grid">
            {quickActions.map((action) => (
              <motion.button
                key={action.id}
                className="quick-action-card"
                onClick={() => navigateToPage(action.path)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <div className="action-icon">
                  <action.icon />
                </div>
                <div className="action-content">
                  <h3>{action.label}</h3>
                  <p>{action.description}</p>
                </div>
                <div className="action-arrow">
                  <FiArrowRight />
                </div>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Email Processing */}
        <motion.div
          className="email-processing-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <h2>📧 Process New Emails</h2>
          <button 
            className="process-emails-btn"
            disabled={isProcessing}
            onClick={async () => {
              try {
                setIsProcessing(true);
                setProcessingStatus('Starting email processing...');
                
                const response = await emailAPI.processEmailsEnhanced(5);
                
                if (response.data.success) {
                  setProcessingStatus(`✅ Successfully processed ${response.data.processed_count} emails!`);
                  
                  // Store processing results for navigation
                  setProcessingResults({
                    processed_count: response.data.processed_count,
                    summary: response.data.summary,
                    calendar_events: response.data.calendar_events || [],
                    emails_processed: response.data.emails_processed || []
                  });
                  
                  // Refresh dashboard stats
                  setRefreshTrigger(prev => prev + 1);
                } else {
                  setProcessingStatus('❌ Email processing failed: ' + response.data.error);
                  setProcessingResults(null);
                }
              } catch (error) {
                const errorMessage = error.response?.data?.error || error.message;
                setProcessingStatus('❌ Error: ' + errorMessage);
                setProcessingResults(null);
              } finally {
                setIsProcessing(false);
              }
            }}
          >
            {isProcessing ? <FiLoader className="spinning" /> : <FiMail />}
            {isProcessing ? 'Processing...' : 'Process New Emails'}
          </button>
          
          {/* Processing Status */}
          {processingStatus && (
            <motion.div 
              className="processing-status"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <p>{processingStatus}</p>
            </motion.div>
          )}

          {/* Processing Results */}
          {processingResults && (
            <motion.div 
              className="processing-results"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="results-header">
                <h3>📧 Email Processing Complete!</h3>
                <button 
                  className="btn-close"
                  onClick={clearProcessingResults}
                >
                  ×
                </button>
              </div>
              
              <div className="results-summary">
                <div className="summary-stats">
                  <div className="stat-item">
                    <span className="stat-number">{processingResults.processed_count}</span>
                    <span className="stat-label">Emails Processed</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-number">{processingResults.summary?.events_extracted || 0}</span>
                    <span className="stat-label">Events Found</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-number">{processingResults.summary?.spam_detected || 0}</span>
                    <span className="stat-label">Spam Detected</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-number">{processingResults.calendar_events.length}</span>
                    <span className="stat-label">Calendar Events</span>
                  </div>
                </div>
              </div>

              <div className="results-actions">
                <h4>View Your Processed Emails:</h4>
                <div className="action-buttons">
                  <button 
                    className="btn btn-primary"
                    onClick={() => navigateToPage('/processed-mails')}
                  >
                    <FiInbox />
                    View All Processed Mails
                  </button>
                  
                  {processingResults.summary?.events_extracted > 0 && (
                    <button 
                      className="btn btn-secondary"
                      onClick={() => navigateToPage('/calendar-events')}
                    >
                      <FiCalendar />
                      View Calendar Events
                    </button>
                  )}
                  
                  <button 
                    className="btn btn-secondary"
                    onClick={() => navigateToPage('/agenda')}
                  >
                    <FiList />
                    View Email Agenda
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>

        {/* Dashboard Stats */}
        {dashboardStats && (
          <motion.div 
            className="dashboard-stats-section"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <h2>📊 Your Email Analytics</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">
                  <FiMail />
                </div>
                <div className="stat-content">
                  <span className="stat-number">{dashboardStats.total_emails || 0}</span>
                  <span className="stat-label">Total Emails</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">
                  <FiCalendar />
                </div>
                <div className="stat-content">
                  <span className="stat-number">{dashboardStats.events_created || 0}</span>
                  <span className="stat-label">Events Created</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">
                  <FiTrendingUp />
                </div>
                <div className="stat-content">
                  <span className="stat-number">{dashboardStats.spam_detected || 0}</span>
                  <span className="stat-label">Spam Detected</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">
                  <FiClock />
                </div>
                <div className="stat-content">
                  <span className="stat-number">{Math.round(dashboardStats.processing_time || 0)}s</span>
                  <span className="stat-label">Avg Processing</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Analytics Component */}
        <motion.div
          className="analytics-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.3 }}
        >
          <Analytics user={user} />
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;