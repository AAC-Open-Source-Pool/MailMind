import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FiMenu, 
  FiX, 
  FiMail, 
  FiCalendar, 
  FiList, 
  FiInbox, 
  FiTrendingUp,
  FiHome,
  FiLogOut
} from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import './Navigation.css';

const Navigation = ({ user }) => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: FiHome,
      path: '/dashboard',
      description: 'Main dashboard with analytics'
    },
    {
      id: 'agenda',
      label: 'Agenda',
      icon: FiList,
      path: '/agenda',
      description: 'Non-event emails organized by priority'
    },
    {
      id: 'calendar-events',
      label: 'Calendar Events',
      icon: FiCalendar,
      path: '/calendar-events',
      description: 'View and manage your calendar events'
    },
    {
      id: 'processed-mails',
      label: 'Processed Mails',
      icon: FiInbox,
      path: '/processed-mails',
      description: 'View all processed emails with AI analysis'
    }
  ];

  const handleNavigation = (path) => {
    navigate(path);
    setIsOpen(false);
  };

  const handleLogout = () => {
    logout();
    setIsOpen(false);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <>
      {/* Hamburger Menu Button */}
      <button 
        className="hamburger-button"
        onClick={() => setIsOpen(true)}
        aria-label="Open navigation menu"
      >
        <FiMenu />
      </button>

      {/* Mobile Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            className="mobile-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Navigation Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.nav 
            className="navigation-menu"
            initial={{ x: -320 }}
            animate={{ x: 0 }}
            exit={{ x: -320 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          >
            {/* Header */}
            <div className="nav-header">
              <div className="brand">
                <FiMail className="brand-icon" />
                <span className="brand-text">MailMind</span>
              </div>
              <button 
                className="close-button"
                onClick={() => setIsOpen(false)}
                aria-label="Close navigation menu"
              >
                <FiX />
              </button>
            </div>

            {/* User Profile */}
            <div className="user-profile">
              <div className="user-avatar">
                <FiMail />
              </div>
              <div className="user-info">
                <h3>{user?.fullName || 'User'}</h3>
                <p>{user?.email || 'user@example.com'}</p>
              </div>
            </div>

            {/* Navigation Items */}
            <div className="nav-items">
              {navigationItems.map((item) => (
                <button
                  key={item.id}
                  className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
                  onClick={() => handleNavigation(item.path)}
                >
                  <div className="nav-item-icon">
                    <item.icon />
                  </div>
                  <div className="nav-item-content">
                    <span className="nav-item-label">{item.label}</span>
                    <span className="nav-item-description">{item.description}</span>
                  </div>
                </button>
              ))}
            </div>

            {/* Logout Button */}
            <div className="nav-footer">
              <button className="logout-button" onClick={handleLogout}>
                <FiLogOut />
                <span>Sign Out</span>
              </button>
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </>
  );
};

export default Navigation;
