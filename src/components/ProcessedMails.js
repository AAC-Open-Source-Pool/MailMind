import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiMail, FiClock, FiUser, FiTag, FiExternalLink, FiFilter, FiSearch, FiEye, FiCalendar, FiShield, FiArrowLeft } from 'react-icons/fi';
import { emailAPI } from '../services/api';
import './ProcessedMails.css';

const ProcessedMails = ({ onBack }) => {
  const [processedMails, setProcessedMails] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // all, events, spam, regular
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('date'); // date, sender, subject, type

  useEffect(() => {
    fetchProcessedMails();
  }, []);

  const fetchProcessedMails = async () => {
    try {
      setIsLoading(true);
      console.log('Fetching processed mails...');
      const response = await emailAPI.getEmailHistory();
      console.log('ProcessedMails API response:', response.data);
      
      if (response.data.success) {
        const mails = response.data.emails.map(email => ({
          id: email.id,
          subject: email.subject,
          sender: email.sender,
          date: email.date,
          summary: email.ai_summary || email.summary || 'No summary available',
          type: email.event_extracted ? 'event' : email.spam_detected ? 'spam' : 'regular',
          priority: email.priority || 'medium',
          category: email.category || 'general',
          tags: email.tags || [],
          eventData: email.event_data || null,
          spamScore: email.spam_score || 0,
          processingTime: email.processing_time || 0,
          originalEmail: email
        }));
        
        setProcessedMails(mails);
      } else {
        setError('Failed to fetch processed mails');
      }
    } catch (error) {
      console.error('Error fetching processed mails:', error);
      setError('Error loading processed mails');
    } finally {
      setIsLoading(false);
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'event': return <FiCalendar />;
      case 'spam': return <FiShield />;
      default: return <FiMail />;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'event': return '#27ae60';
      case 'spam': return '#e74c3c';
      default: return '#3498db';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return '#e74c3c';
      case 'medium': return '#f39c12';
      case 'low': return '#27ae60';
      default: return '#95a5a6';
    }
  };

  const filteredAndSortedMails = processedMails
    .filter(mail => {
      const matchesSearch = mail.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           mail.sender.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           mail.summary.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesFilter = filter === 'all' || mail.type === filter;
      
      return matchesSearch && matchesFilter;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.date) - new Date(a.date);
        case 'sender':
          return a.sender.localeCompare(b.sender);
        case 'subject':
          return a.subject.localeCompare(b.subject);
        case 'type':
          return a.type.localeCompare(b.type);
        default:
          return 0;
      }
    });

  const groupByDate = (mails) => {
    const groups = {};
    mails.forEach(mail => {
      const date = new Date(mail.date).toDateString();
      if (!groups[date]) {
        groups[date] = [];
      }
      groups[date].push(mail);
    });
    return groups;
  };

  const groupedMails = groupByDate(filteredAndSortedMails);

  const getTypeStats = () => {
    const stats = { total: processedMails.length, events: 0, spam: 0, regular: 0 };
    processedMails.forEach(mail => {
      stats[mail.type]++;
    });
    return stats;
  };

  const stats = getTypeStats();

  if (isLoading) {
    return (
      <div className="processed-mails-container">
        <div className="loading-spinner"></div>
        <p>Loading processed mails...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="processed-mails-container">
        <div className="error-message">
          <FiMail className="error-icon" />
          <p>{error}</p>
          <button onClick={fetchProcessedMails} className="btn btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="processed-mails-container">
      <div className="processed-mails-header">
        <div className="processed-mails-title">
          {onBack && (
            <button className="back-button" onClick={onBack}>
              <FiArrowLeft />
              Back to Dashboard
            </button>
          )}
          <div className="title-content">
            <FiMail className="title-icon" />
            <h1>Processed Mails</h1>
            <span className="mail-count">{filteredAndSortedMails.length} mails</span>
          </div>
        </div>
        
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-number">{stats.total}</div>
            <div className="stat-label">Total</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.events}</div>
            <div className="stat-label">Events</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.regular}</div>
            <div className="stat-label">Regular</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.spam}</div>
            <div className="stat-label">Spam</div>
          </div>
        </div>
        
        <div className="processed-mails-controls">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search processed mails..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
          
          <div className="filter-buttons">
            <button
              className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => setFilter('all')}
            >
              All Mails
            </button>
            <button
              className={`filter-btn ${filter === 'events' ? 'active' : ''}`}
              onClick={() => setFilter('events')}
            >
              Events
            </button>
            <button
              className={`filter-btn ${filter === 'regular' ? 'active' : ''}`}
              onClick={() => setFilter('regular')}
            >
              Regular
            </button>
            <button
              className={`filter-btn ${filter === 'spam' ? 'active' : ''}`}
              onClick={() => setFilter('spam')}
            >
              Spam
            </button>
          </div>
          
          <div className="sort-controls">
            <label>Sort by:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="sort-select"
            >
              <option value="date">Date</option>
              <option value="sender">Sender</option>
              <option value="subject">Subject</option>
              <option value="type">Type</option>
            </select>
          </div>
        </div>
      </div>

      <div className="processed-mails-content">
        {Object.keys(groupedMails).length === 0 ? (
          <div className="empty-state">
            <FiMail className="empty-icon" />
            <h3>No processed mails found</h3>
            <p>Process some emails to see them here.</p>
          </div>
        ) : (
          Object.entries(groupedMails).map(([date, dateMails]) => (
            <motion.div
              key={date}
              className="date-group"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="date-header">
                <h2>{date}</h2>
                <span className="date-count">{dateMails.length} mails</span>
              </div>
              
              <div className="mails-list">
                {dateMails.map((mail) => (
                  <motion.div
                    key={mail.id}
                    className={`mail-card mail-${mail.type}`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2 }}
                    whileHover={{ scale: 1.02 }}
                  >
                    <div className="mail-header">
                      <div className="mail-meta">
                        <div className="type-icon" style={{ color: getTypeColor(mail.type) }}>
                          {getTypeIcon(mail.type)}
                        </div>
                        <div className="priority-indicator" style={{ backgroundColor: getPriorityColor(mail.priority) }}></div>
                        <span className="sender">{mail.sender}</span>
                        <span className="time">
                          <FiClock />
                          {new Date(mail.date).toLocaleTimeString()}
                        </span>
                      </div>
                      
                      <div className="mail-badges">
                        <span className="badge badge-type" style={{ backgroundColor: getTypeColor(mail.type) }}>
                          {mail.type}
                        </span>
                        {mail.priority === 'high' && (
                          <span className="badge badge-priority">High Priority</span>
                        )}
                        {mail.type === 'spam' && (
                          <span className="badge badge-spam">Spam Score: {Math.round(mail.spamScore * 100)}%</span>
                        )}
                      </div>
                    </div>
                    
                    <div className="mail-content">
                      <h3 className="mail-subject">{mail.subject}</h3>
                      <p className="mail-summary">{mail.summary}</p>
                      
                      {mail.tags.length > 0 && (
                        <div className="mail-tags">
                          {mail.tags.map((tag, index) => (
                            <span key={index} className="tag">
                              <FiTag />
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                      
                      {mail.eventData && (
                        <div className="event-info">
                          <FiCalendar />
                          <span>Event: {mail.eventData.title}</span>
                          {mail.eventData.start_time && (
                            <span> at {new Date(mail.eventData.start_time).toLocaleString()}</span>
                          )}
                        </div>
                      )}
                      
                      <div className="processing-info">
                        <span>Processing time: {mail.processingTime}ms</span>
                      </div>
                    </div>
                    
                    <div className="mail-actions">
                      <button className="btn btn-sm btn-outline">
                        <FiEye />
                        View Details
                      </button>
                      <button className="btn btn-sm btn-outline">
                        <FiExternalLink />
                        View Original
                      </button>
                      {mail.type === 'event' && (
                        <button className="btn btn-sm btn-primary">
                          <FiCalendar />
                          View Event
                        </button>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
};

export default ProcessedMails;
