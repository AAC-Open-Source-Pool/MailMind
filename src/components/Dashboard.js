import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FiMail, FiCalendar, FiClock, FiTrendingUp, FiUser, FiLogOut, FiMenu, FiX, FiExternalLink } from 'react-icons/fi';
import Analytics from './Analytics';
import Calendar from './Calendar';
import EmailGist from './EmailGist';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('analytics');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigationItems = [
    {
      id: 'analytics',
      label: 'Analytics',
      icon: FiTrendingUp,
      description: 'View your productivity insights'
    },
    {
      id: 'calendar',
      label: 'Calendar',
      icon: FiCalendar,
      description: 'Review your events and agenda'
    },
    {
      id: 'emails',
      label: 'Email Gist',
      icon: FiMail,
      description: 'Non-event email summaries'
    }
  ];

  const externalLinks = [
    {
      label: 'Gmail',
      url: 'https://mail.google.com',
      icon: FiMail
    },
    {
      label: 'Google Calendar',
      url: 'https://calendar.google.com',
      icon: FiCalendar
    }
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'analytics':
        return <Analytics user={user} />;
      case 'calendar':
        return <Calendar user={user} />;
      case 'emails':
        return <EmailGist user={user} />;
      default:
        return <Analytics user={user} />;
    }
  };

  const handleLogout = () => {
    onLogout();
  };

  return (
    <div className="dashboard">
      {/* Mobile Menu Overlay */}
      {sidebarOpen && (
        <div 
          className="mobile-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <motion.aside 
        className={`sidebar ${sidebarOpen ? 'open' : ''}`}
        initial={{ x: -300 }}
        animate={{ x: sidebarOpen ? 0 : -300 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      >
        <div className="sidebar-header">
          <div className="brand">
            <FiMail className="brand-icon" />
            <span className="brand-text">Mailmind</span>
          </div>
          <button 
            className="close-sidebar"
            onClick={() => setSidebarOpen(false)}
          >
            <FiX />
          </button>
        </div>

        <div className="user-profile">
          <div className="user-avatar">
            <FiUser />
          </div>
          <div className="user-info">
            <h3>{user?.fullName || 'User'}</h3>
            <p>{user?.email || 'user@example.com'}</p>
          </div>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-section">
            <h4>Main Navigation</h4>
            <ul>
              {navigationItems.map((item) => (
                <li key={item.id}>
                  <button
                    className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                    onClick={() => {
                      setActiveTab(item.id);
                      setSidebarOpen(false);
                    }}
                  >
                    <item.icon />
                    <span>{item.label}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>

          <div className="nav-section">
            <h4>External Links</h4>
            <ul>
              {externalLinks.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="nav-item external"
                  >
                    <link.icon />
                    <span>{link.label}</span>
                    <FiExternalLink className="external-icon" />
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </nav>

        <div className="sidebar-footer">
          <button className="logout-btn" onClick={handleLogout}>
            <FiLogOut />
            <span>Sign Out</span>
          </button>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Top Header */}
        <header className="top-header">
          <div className="header-left">
            <button 
              className="menu-toggle"
              onClick={() => setSidebarOpen(true)}
            >
              <FiMenu />
            </button>
            <div className="page-title">
              <h1>{navigationItems.find(item => item.id === activeTab)?.label}</h1>
              <p>{navigationItems.find(item => item.id === activeTab)?.description}</p>
            </div>
          </div>
          
          <div className="header-right">
            <div className="user-menu">
              <div className="user-avatar-small">
                <FiUser />
              </div>
              <div className="user-details">
                <span className="user-name">{user?.fullName || 'User'}</span>
                <span className="user-email">{user?.email || 'user@example.com'}</span>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="page-content">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            {renderContent()}
          </motion.div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard; 