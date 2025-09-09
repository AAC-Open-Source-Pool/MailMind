import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiMail, FiClock, FiUser, FiTag, FiExternalLink, FiCalendar, FiFilter, FiArrowLeft, FiAlertCircle, FiCheckCircle, FiStar } from 'react-icons/fi';
import { emailAPI } from '../services/api';
import './Agenda.css';

const Agenda = ({ onBack }) => {
  const [agendaItems, setAgendaItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // all, important, action_required, follow_up
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchAgendaItems();
  }, []);

  const fetchAgendaItems = async () => {
    try {
      setIsLoading(true);
      console.log('Fetching agenda items...');
      const response = await emailAPI.getEmailHistory();
      console.log('Agenda API response:', response.data);
      
      if (response.data.success) {
        // Filter for non-event emails (emails that are not events)
        const nonEventEmails = response.data.emails.filter(email => 
          !email.event_extracted && !email.spam_detected
        );
        
        // Transform into agenda items
        const agendaData = nonEventEmails.map(email => ({
          id: email.id,
          subject: email.subject,
          sender: email.sender,
          date: email.date,
          summary: email.ai_summary || email.summary || 'No summary available',
          priority: email.priority || 'medium',
          category: email.category || 'general',
          actionRequired: email.action_required || false,
          followUp: email.follow_up || false,
          tags: email.tags || [],
          originalEmail: email
        }));
        
        setAgendaItems(agendaData);
      } else {
        setError('Failed to fetch agenda items');
      }
    } catch (error) {
      console.error('Error fetching agenda items:', error);
      setError('Error loading agenda items');
    } finally {
      setIsLoading(false);
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

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'work': return <FiCalendar />;
      case 'personal': return <FiUser />;
      case 'finance': return <FiTag />;
      default: return <FiMail />;
    }
  };

  const filteredItems = agendaItems.filter(item => {
    const matchesSearch = item.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.sender.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.summary.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = filter === 'all' || 
                         (filter === 'important' && item.priority === 'high') ||
                         (filter === 'action_required' && item.actionRequired) ||
                         (filter === 'follow_up' && item.followUp);
    
    return matchesSearch && matchesFilter;
  });

  const groupByDate = (items) => {
    const groups = {};
    items.forEach(item => {
      const date = new Date(item.date).toDateString();
      if (!groups[date]) {
        groups[date] = [];
      }
      groups[date].push(item);
    });
    return groups;
  };

  const groupedItems = groupByDate(filteredItems);

  if (isLoading) {
    return (
      <div className="agenda-container">
        <div className="loading-spinner"></div>
        <p>Loading agenda items...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="agenda-container">
        <div className="error-message">
          <FiMail className="error-icon" />
          <p>{error}</p>
          <button onClick={fetchAgendaItems} className="btn btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="agenda-container">
      <div className="agenda-header">
        <div className="agenda-title">
          {onBack && (
            <button className="back-button" onClick={onBack}>
              <FiArrowLeft />
              Back to Dashboard
            </button>
          )}
          <div className="title-content">
            <FiMail className="title-icon" />
            <h1>Email Agenda</h1>
            <span className="item-count">{filteredItems.length} items</span>
          </div>
        </div>
        
        <div className="agenda-controls">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search agenda items..."
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
              All
            </button>
            <button
              className={`filter-btn ${filter === 'important' ? 'active' : ''}`}
              onClick={() => setFilter('important')}
            >
              Important
            </button>
            <button
              className={`filter-btn ${filter === 'action_required' ? 'active' : ''}`}
              onClick={() => setFilter('action_required')}
            >
              Action Required
            </button>
            <button
              className={`filter-btn ${filter === 'follow_up' ? 'active' : ''}`}
              onClick={() => setFilter('follow_up')}
            >
              Follow Up
            </button>
          </div>
        </div>
      </div>

      <div className="agenda-content">
        {Object.keys(groupedItems).length === 0 ? (
          <div className="empty-state">
            <FiMail className="empty-icon" />
            <h3>No agenda items found</h3>
            <p>Process some emails to see your agenda items here.</p>
          </div>
        ) : (
          Object.entries(groupedItems).map(([date, items]) => (
            <motion.div
              key={date}
              className="date-group"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="date-header">
                <h2>{date}</h2>
                <span className="date-count">{items.length} items</span>
              </div>
              
              <div className="agenda-items">
                {items.map((item) => (
                  <motion.div
                    key={item.id}
                    className="agenda-item"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2 }}
                    whileHover={{ scale: 1.02 }}
                  >
                    <div className="item-header">
                      <div className="item-meta">
                        <div className="priority-indicator" style={{ backgroundColor: getPriorityColor(item.priority) }}></div>
                        <div className="category-icon">{getCategoryIcon(item.category)}</div>
                        <span className="sender">{item.sender}</span>
                        <span className="time">
                          <FiClock />
                          {new Date(item.date).toLocaleTimeString()}
                        </span>
                      </div>
                      
                      <div className="item-badges">
                        {item.actionRequired && (
                          <span className="badge badge-action">Action Required</span>
                        )}
                        {item.followUp && (
                          <span className="badge badge-follow">Follow Up</span>
                        )}
                        {item.priority === 'high' && (
                          <span className="badge badge-important">Important</span>
                        )}
                      </div>
                    </div>
                    
                    <div className="item-content">
                      <h3 className="item-subject">{item.subject}</h3>
                      <p className="item-summary">{item.summary}</p>
                      
                      {item.tags.length > 0 && (
                        <div className="item-tags">
                          {item.tags.map((tag, index) => (
                            <span key={index} className="tag">
                              <FiTag />
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <div className="item-actions">
                      <button className="btn btn-sm btn-outline">
                        <FiExternalLink />
                        View Original
                      </button>
                      <button className="btn btn-sm btn-primary">
                        <FiMail />
                        Reply
                      </button>
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

export default Agenda;
