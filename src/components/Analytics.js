import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiClock, FiMail, FiCalendar, FiTrendingUp, FiTrendingDown, FiActivity } from 'react-icons/fi';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { analyticsAPI } from '../services/api';
import './Analytics.css';

const Analytics = ({ user }) => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  // Fetch analytics data from API
  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setIsLoading(true);
        const response = await analyticsAPI.getSummary();
        if (response.data.success) {
          setAnalyticsData(response.data.summary);
        } else {
          setError('Failed to fetch analytics data');
        }
      } catch (error) {
        console.error('Error fetching analytics:', error);
        setError('Failed to load analytics data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  // Use API data or fallback to user data
  const analytics = analyticsData || user?.analytics || {
    total_emails_processed: 127,
    spam_detected: 15,
    events_extracted: 8,
    average_urgency: 3,
    processing_time: 45
  };

  // Sample data for charts
  const weeklyData = [
    { day: 'Mon', emails: 23, timeSaved: 8, events: 2 },
    { day: 'Tue', emails: 31, timeSaved: 12, events: 1 },
    { day: 'Wed', emails: 28, timeSaved: 10, events: 3 },
    { day: 'Thu', emails: 35, timeSaved: 15, events: 2 },
    { day: 'Fri', emails: 42, timeSaved: 18, events: 4 },
    { day: 'Sat', emails: 15, timeSaved: 6, events: 1 },
    { day: 'Sun', emails: 12, timeSaved: 5, events: 0 }
  ];

  const emailCategories = [
    { name: 'Important', value: 35, color: '#4a7c59' },
    { name: 'Work', value: 28, color: '#5a8c69' },
    { name: 'Personal', value: 22, color: '#6a9c79' },
    { name: 'Spam', value: 15, color: '#ff6b6b' }
  ];

  const productivityTrends = [
    { month: 'Jan', score: 75 },
    { month: 'Feb', score: 82 },
    { month: 'Mar', score: 79 },
    { month: 'Apr', score: 87 },
    { month: 'May', score: 91 },
    { month: 'Jun', score: 88 }
  ];

  const metricCards = [
    {
      title: 'Emails Processed',
      value: analytics.total_emails_processed?.toLocaleString() || '0',
      change: '+12%',
      trend: 'up',
      icon: FiMail,
      color: '#4a7c59'
    },
    {
      title: 'Spam Detected',
      value: analytics.spam_detected || '0',
      change: '+8%',
      trend: 'up',
      icon: FiMail,
      color: '#5a8c69'
    },
    {
      title: 'Events Extracted',
      value: analytics.events_extracted || '0',
      change: '+25%',
      trend: 'up',
      icon: FiCalendar,
      color: '#6a9c79'
    },
    {
      title: 'Processing Time',
      value: `${analytics.processing_time || 0}s`,
      change: '+5%',
      trend: 'up',
      icon: FiActivity,
      color: '#8bc34a'
    }
  ];

  if (isLoading) {
    return (
      <div className="analytics">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics">
        <div className="error-container">
          <h3>Error Loading Analytics</h3>
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="btn btn-primary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="analytics">
      {/* Welcome Section */}
      <motion.div 
        className="welcome-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h2>Welcome back, {user?.fullName || 'User'}! 👋</h2>
        <p>Here's your productivity overview for this week</p>
      </motion.div>

      {/* Metrics Cards */}
      <div className="metrics-grid">
        {metricCards.map((metric, index) => (
          <motion.div
            key={metric.title}
            className="metric-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: index * 0.1 }}
          >
            <div className="metric-header">
              <div className="metric-icon" style={{ backgroundColor: metric.color }}>
                <metric.icon />
              </div>
              <div className="metric-trend">
                <span className={`trend-indicator ${metric.trend}`}>
                  {metric.trend === 'up' ? <FiTrendingUp /> : <FiTrendingDown />}
                  {metric.change}
                </span>
              </div>
            </div>
            <div className="metric-content">
              <h3 className="metric-value">{metric.value}</h3>
              <p className="metric-title">{metric.title}</p>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        {/* Weekly Overview Chart */}
        <motion.div 
          className="chart-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div className="chart-header">
            <h3>Weekly Overview</h3>
            <p>Email activity and time saved this week</p>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
                <XAxis 
                  dataKey="day" 
                  stroke="rgba(255, 255, 255, 0.7)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="rgba(255, 255, 255, 0.7)"
                  fontSize={12}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px',
                    color: 'white'
                  }}
                />
                <Area 
                  type="monotone" 
                  dataKey="emails" 
                  stackId="1"
                  stroke="#4a7c59" 
                  fill="#4a7c59" 
                  fillOpacity={0.3}
                />
                <Area 
                  type="monotone" 
                  dataKey="timeSaved" 
                  stackId="2"
                  stroke="#5a8c69" 
                  fill="#5a8c69" 
                  fillOpacity={0.3}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Email Categories Chart */}
        <motion.div 
          className="chart-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <div className="chart-header">
            <h3>Email Categories</h3>
            <p>Distribution of your emails by category</p>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={emailCategories}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {emailCategories.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px',
                    color: 'white'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="chart-legend">
              {emailCategories.map((category, index) => (
                <div key={index} className="legend-item">
                  <div className="legend-color" style={{ backgroundColor: category.color }}></div>
                  <span>{category.name}</span>
                  <span className="legend-value">{category.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Productivity Trends */}
        <motion.div 
          className="chart-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <div className="chart-header">
            <h3>Productivity Trends</h3>
            <p>Your productivity score over the last 6 months</p>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={productivityTrends}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
                <XAxis 
                  dataKey="month" 
                  stroke="rgba(255, 255, 255, 0.7)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="rgba(255, 255, 255, 0.7)"
                  fontSize={12}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px',
                    color: 'white'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="score" 
                  stroke="#8bc34a" 
                  strokeWidth={3}
                  dot={{ fill: '#8bc34a', strokeWidth: 2, r: 6 }}
                  activeDot={{ r: 8, stroke: '#8bc34a', strokeWidth: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* Insights Section */}
      <motion.div 
        className="insights-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.7 }}
      >
        <h3>Key Insights</h3>
        <div className="insights-grid">
          <div className="insight-card">
            <div className="insight-icon positive">
              <FiTrendingUp />
            </div>
            <div className="insight-content">
              <h4>Productivity Boost</h4>
              <p>Your productivity score has increased by 15% this month compared to last month.</p>
            </div>
          </div>
          <div className="insight-card">
            <div className="insight-icon positive">
              <FiClock />
            </div>
            <div className="insight-content">
              <h4>Time Efficiency</h4>
              <p>You've saved an average of 2.5 hours per day through automated email processing.</p>
            </div>
          </div>
          <div className="insight-card">
            <div className="insight-icon neutral">
              <FiMail />
            </div>
            <div className="insight-content">
              <h4>Email Management</h4>
              <p>75% of your emails are now automatically categorized and prioritized.</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Analytics; 