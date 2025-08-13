import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FiMail, FiSearch, FiFilter, FiClock, FiUser, FiTag, FiEye, FiArchive, FiTrash2, FiStar } from 'react-icons/fi';
import './EmailGist.css';

const EmailGist = ({ user }) => {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedEmail, setSelectedEmail] = useState(null);

  // Sample email data
  const emails = [
    {
      id: 1,
      subject: 'Project Update - Q4 Milestones',
      sender: 'manager@company.com',
      senderName: 'Sarah Johnson',
      summary: 'Updated project timeline with new milestones for Q4. Key deliverables include user interface redesign and backend optimization.',
      category: 'work',
      priority: 'high',
      date: '2024-01-15T10:30:00',
      read: false,
      starred: true,
      tags: ['project', 'milestone', 'timeline']
    },
    {
      id: 2,
      subject: 'Weekly Newsletter - Tech Updates',
      sender: 'newsletter@techdaily.com',
      senderName: 'Tech Daily',
      summary: 'Latest updates in AI and machine learning. New developments in natural language processing and computer vision technologies.',
      category: 'newsletter',
      priority: 'low',
      date: '2024-01-15T09:15:00',
      read: true,
      starred: false,
      tags: ['AI', 'technology', 'newsletter']
    },
    {
      id: 3,
      subject: 'Invoice #INV-2024-001',
      sender: 'billing@serviceprovider.com',
      senderName: 'Service Provider Inc.',
      summary: 'Invoice for cloud services and hosting fees for December 2023. Total amount: $1,250.00. Due date: January 30, 2024.',
      category: 'billing',
      priority: 'medium',
      date: '2024-01-15T08:45:00',
      read: false,
      starred: false,
      tags: ['invoice', 'billing', 'payment']
    },
    {
      id: 4,
      subject: 'Team Lunch Invitation',
      sender: 'hr@company.com',
      senderName: 'HR Department',
      summary: 'Monthly team lunch this Friday at 12:30 PM. Location: Downtown Bistro. Please RSVP by Wednesday.',
      category: 'personal',
      priority: 'medium',
      date: '2024-01-14T16:20:00',
      read: true,
      starred: false,
      tags: ['team', 'lunch', 'social']
    },
    {
      id: 5,
      subject: 'Security Alert - Password Reset',
      sender: 'security@company.com',
      senderName: 'IT Security',
      summary: 'Your account password has been reset. If you did not request this change, please contact IT support immediately.',
      category: 'security',
      priority: 'high',
      date: '2024-01-14T14:10:00',
      read: false,
      starred: true,
      tags: ['security', 'password', 'alert']
    },
    {
      id: 6,
      subject: 'Conference Registration Confirmation',
      sender: 'events@techconf.com',
      senderName: 'Tech Conference 2024',
      summary: 'Your registration for Tech Conference 2024 has been confirmed. Event details and schedule attached.',
      category: 'event',
      priority: 'medium',
      date: '2024-01-14T11:30:00',
      read: true,
      starred: false,
      tags: ['conference', 'registration', 'event']
    }
  ];

  const categories = [
    { id: 'all', label: 'All Emails', color: '#4a7c59' },
    { id: 'work', label: 'Work', color: '#5a8c69' },
    { id: 'personal', label: 'Personal', color: '#6a9c79' },
    { id: 'newsletter', label: 'Newsletters', color: '#8bc34a' },
    { id: 'billing', label: 'Billing', color: '#ffa726' },
    { id: 'security', label: 'Security', color: '#ff6b6b' }
  ];

  const priorities = {
    high: { label: 'High', color: '#ff6b6b' },
    medium: { label: 'Medium', color: '#ffa726' },
    low: { label: 'Low', color: '#66bb6a' }
  };

  const filteredEmails = emails.filter(email => {
    const matchesFilter = filter === 'all' || email.category === filter;
    const matchesSearch = email.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         email.summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         email.senderName.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) {
      return 'Just now';
    } else if (diffInHours < 24) {
      return `${diffInHours}h ago`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays}d ago`;
    }
  };

  const handleEmailClick = (email) => {
    setSelectedEmail(email);
  };

  const closeEmailDetail = () => {
    setSelectedEmail(null);
  };

  return (
    <div className="email-gist">
      {/* Header */}
      <motion.div 
        className="email-header"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="header-left">
          <h2>Email Gist</h2>
          <p>AI-powered summaries of your non-event emails</p>
        </div>
        <div className="header-stats">
          <div className="stat-item">
            <span className="stat-number">{emails.length}</span>
            <span className="stat-label">Total Emails</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{emails.filter(e => !e.read).length}</span>
            <span className="stat-label">Unread</span>
          </div>
        </div>
      </motion.div>

      {/* Controls */}
      <motion.div 
        className="email-controls"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
      >
        <div className="search-box">
          <FiSearch className="search-icon" />
          <input
            type="text"
            placeholder="Search emails..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filter-buttons">
          {categories.map((category) => (
            <button
              key={category.id}
              className={`filter-btn ${filter === category.id ? 'active' : ''}`}
              onClick={() => setFilter(category.id)}
              style={{ '--category-color': category.color }}
            >
              <FiFilter />
              {category.label}
            </button>
          ))}
        </div>
      </motion.div>

      {/* Email List */}
      <div className="emails-container">
        {filteredEmails.length === 0 ? (
          <motion.div 
            className="no-emails"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <FiMail className="no-emails-icon" />
            <h3>No emails found</h3>
            <p>Try adjusting your filters or search terms</p>
          </motion.div>
        ) : (
          <div className="emails-list">
            {filteredEmails.map((email, index) => (
              <motion.div
                key={email.id}
                className={`email-card ${!email.read ? 'unread' : ''}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 + index * 0.05 }}
                whileHover={{ scale: 1.02 }}
                onClick={() => handleEmailClick(email)}
              >
                <div className="email-header-row">
                  <div className="email-sender">
                    <div className="sender-avatar">
                      {email.senderName.charAt(0).toUpperCase()}
                    </div>
                    <div className="sender-info">
                      <h4>{email.senderName}</h4>
                      <span className="sender-email">{email.sender}</span>
                    </div>
                  </div>
                  <div className="email-meta">
                    <span className="email-time">{formatDate(email.date)}</span>
                    <div className="email-actions">
                      <button className="action-btn" onClick={(e) => { e.stopPropagation(); }}>
                        <FiStar className={email.starred ? 'starred' : ''} />
                      </button>
                      <button className="action-btn" onClick={(e) => { e.stopPropagation(); }}>
                        <FiArchive />
                      </button>
                    </div>
                  </div>
                </div>

                <div className="email-content">
                  <h3 className="email-subject">{email.subject}</h3>
                  <p className="email-summary">{email.summary}</p>
                </div>

                <div className="email-footer">
                  <div className="email-tags">
                    {email.tags.slice(0, 3).map((tag, idx) => (
                      <span key={idx} className="tag">
                        <FiTag />
                        {tag}
                      </span>
                    ))}
                    {email.tags.length > 3 && (
                      <span className="more-tags">+{email.tags.length - 3}</span>
                    )}
                  </div>
                  <div className="email-priority">
                    <span className={`priority-badge ${email.priority}`}>
                      {priorities[email.priority].label}
                    </span>
                  </div>
                </div>

                {!email.read && <div className="unread-indicator"></div>}
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Email Detail Modal */}
      {selectedEmail && (
        <motion.div 
          className="email-modal-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={closeEmailDetail}
        >
          <motion.div 
            className="email-modal"
            initial={{ opacity: 0, scale: 0.9, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-header">
              <h3>Email Details</h3>
              <button className="close-modal" onClick={closeEmailDetail}>
                ×
              </button>
            </div>

            <div className="modal-content">
              <div className="email-detail-header">
                <div className="detail-sender">
                  <div className="sender-avatar-large">
                    {selectedEmail.senderName.charAt(0).toUpperCase()}
                  </div>
                  <div className="sender-details">
                    <h4>{selectedEmail.senderName}</h4>
                    <span>{selectedEmail.sender}</span>
                    <span className="detail-time">{formatDate(selectedEmail.date)}</span>
                  </div>
                </div>
                <div className="detail-priority">
                  <span className={`priority-badge ${selectedEmail.priority}`}>
                    {priorities[selectedEmail.priority].label}
                  </span>
                </div>
              </div>

              <div className="email-detail-content">
                <h2>{selectedEmail.subject}</h2>
                <p className="detail-summary">{selectedEmail.summary}</p>
              </div>

              <div className="email-detail-tags">
                <h5>Tags:</h5>
                <div className="tags-list">
                  {selectedEmail.tags.map((tag, idx) => (
                    <span key={idx} className="tag">
                      <FiTag />
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              <div className="email-detail-actions">
                <button className="btn btn-primary">
                  <FiEye />
                  View Original Email
                </button>
                <button className="btn btn-secondary">
                  <FiArchive />
                  Archive
                </button>
                <button className="btn btn-secondary">
                  <FiTrash2 />
                  Delete
                </button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
};

export default EmailGist; 