import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiCalendar, FiClock, FiMapPin, FiUser, FiPlus, FiFilter, FiSearch, FiExternalLink } from 'react-icons/fi';
import { emailAPI } from '../services/api';
import './Calendar.css';

const Calendar = ({ user }) => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch calendar events from backend
  useEffect(() => {
    const fetchCalendarEvents = async () => {
      try {
        setIsLoading(true);
        // For now, we'll use the email history to get events
        // In a full implementation, you'd have a dedicated calendar events endpoint
        const response = await emailAPI.getEmailHistory(100);
        if (response.data.success) {
          // Filter for event-based emails and convert to calendar events
          const eventEmails = response.data.emails?.filter(email => 
            email.event_extracted || email.analysis?.event_details
          ) || [];
          
          const calendarEvents = eventEmails.map((email, index) => ({
            id: email.id || index,
            title: email.analysis?.event_details?.title || email.subject,
            description: email.summary || email.analysis?.event_details?.description || '',
            date: email.analysis?.event_details?.start_time?.split('T')[0] || new Date().toISOString().split('T')[0],
            time: email.analysis?.event_details?.start_time ? 
              new Date(email.analysis.event_details.start_time).toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit',
                hour12: true 
              }) : 'All Day',
            location: email.analysis?.event_details?.location || '',
            attendees: email.attendees || [],
            category: email.category || 'work',
            priority: email.priority || 'medium',
            source: 'email',
            calendar_link: email.analysis?.event_details?.calendar_link || '',
            email_id: email.id
          }));
          
          setEvents(calendarEvents);
        } else {
          setError('Failed to fetch calendar events');
        }
      } catch (error) {
        console.error('Error fetching calendar events:', error);
        setError('Failed to load calendar events');
        // Fallback to sample data
        setEvents([
          {
            id: 1,
            title: 'Team Meeting - Q4 Planning',
            description: 'Quarterly planning session with the development team',
            date: '2024-01-15',
            time: '10:00 AM - 11:30 AM',
            location: 'Conference Room A',
            attendees: ['john@company.com', 'sarah@company.com', 'mike@company.com'],
            category: 'work',
            priority: 'high',
            source: 'email'
          }
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCalendarEvents();
  }, []);

  // Sample events data (fallback)
  const sampleEvents = [
    {
      id: 1,
      title: 'Team Meeting - Q4 Planning',
      description: 'Quarterly planning session with the development team',
      date: '2024-01-15',
      time: '10:00 AM - 11:30 AM',
      location: 'Conference Room A',
      attendees: ['john@company.com', 'sarah@company.com', 'mike@company.com'],
      category: 'work',
      priority: 'high',
      source: 'email'
    },
    {
      id: 2,
      title: 'Client Presentation',
      description: 'Present quarterly results to key client',
      date: '2024-01-16',
      time: '2:00 PM - 3:00 PM',
      location: 'Virtual Meeting',
      attendees: ['client@example.com', 'manager@company.com'],
      category: 'work',
      priority: 'high',
      source: 'email'
    },
    {
      id: 3,
      title: 'Dentist Appointment',
      description: 'Regular dental checkup',
      date: '2024-01-17',
      time: '9:00 AM - 10:00 AM',
      location: 'Dental Clinic',
      attendees: [],
      category: 'personal',
      priority: 'medium',
      source: 'email'
    },
    {
      id: 4,
      title: 'Project Deadline',
      description: 'Submit final project deliverables',
      date: '2024-01-18',
      time: '5:00 PM',
      location: 'Office',
      attendees: ['team@company.com'],
      category: 'work',
      priority: 'high',
      source: 'email'
    },
    {
      id: 5,
      title: 'Lunch with Colleague',
      description: 'Catch up over lunch',
      date: '2024-01-19',
      time: '12:00 PM - 1:00 PM',
      location: 'Local Restaurant',
      attendees: ['colleague@company.com'],
      category: 'personal',
      priority: 'low',
      source: 'email'
    }
  ];

  const categories = [
    { id: 'all', label: 'All Events', color: '#4a7c59' },
    { id: 'work', label: 'Work', color: '#5a8c69' },
    { id: 'personal', label: 'Personal', color: '#6a9c79' },
    { id: 'meeting', label: 'Meetings', color: '#8bc34a' }
  ];

  const priorities = {
    high: { label: 'High', color: '#ff6b6b' },
    medium: { label: 'Medium', color: '#ffa726' },
    low: { label: 'Low', color: '#66bb6a' }
  };

  const filteredEvents = events.filter(event => {
    const matchesFilter = filter === 'all' || event.category === filter;
    const matchesSearch = event.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         event.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const groupedEvents = filteredEvents.reduce((groups, event) => {
    const date = event.date;
    if (!groups[date]) {
      groups[date] = [];
    }
    groups[date].push(event);
    return groups;
  }, {});

  const sortedDates = Object.keys(groupedEvents).sort();

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return 'Tomorrow';
    } else {
      return date.toLocaleDateString('en-US', { 
        weekday: 'long', 
        month: 'short', 
        day: 'numeric' 
      });
    }
  };

  if (isLoading) {
    return (
      <div className="calendar">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading calendar events...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="calendar">
        <div className="error-container">
          <h3>Error Loading Calendar</h3>
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="btn btn-primary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="calendar">
      {/* Header */}
      <motion.div 
        className="calendar-header"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="header-left">
          <h2>Calendar & Events</h2>
          <p>Events created from your emails and calendar integration</p>
        </div>
        <button className="btn btn-primary">
          <FiPlus />
          Add Event
        </button>
      </motion.div>

      {/* Filters and Search */}
      <motion.div 
        className="calendar-controls"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
      >
        <div className="search-box">
          <FiSearch className="search-icon" />
          <input
            type="text"
            placeholder="Search events..."
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

      {/* Events List */}
      <div className="events-container">
        {sortedDates.length === 0 ? (
          <motion.div 
            className="no-events"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <FiCalendar className="no-events-icon" />
            <h3>No events found</h3>
            <p>Try adjusting your filters or search terms</p>
          </motion.div>
        ) : (
          sortedDates.map((date, index) => (
            <motion.div
              key={date}
              className="date-group"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 + index * 0.1 }}
            >
              <div className="date-header">
                <h3>{formatDate(date)}</h3>
                <span className="event-count">{groupedEvents[date].length} event{groupedEvents[date].length !== 1 ? 's' : ''}</span>
              </div>

              <div className="events-list">
                {groupedEvents[date].map((event) => (
                  <motion.div
                    key={event.id}
                    className="event-card"
                    whileHover={{ scale: 1.02 }}
                    transition={{ type: 'spring', stiffness: 300 }}
                  >
                    <div className="event-header">
                      <div className="event-title-section">
                        <h4>{event.title}</h4>
                        <span className={`priority-badge ${event.priority}`}>
                          {priorities[event.priority].label}
                        </span>
                      </div>
                      <div className="event-source">
                        <span className="source-badge">From Email</span>
                      </div>
                    </div>

                    <p className="event-description">{event.description}</p>

                    <div className="event-details">
                      <div className="detail-item">
                        <FiClock className="detail-icon" />
                        <span>{event.time}</span>
                      </div>
                      
                      {event.location && (
                        <div className="detail-item">
                          <FiMapPin className="detail-icon" />
                          <span>{event.location}</span>
                        </div>
                      )}

                      {event.attendees.length > 0 && (
                        <div className="detail-item">
                          <FiUser className="detail-icon" />
                          <span>{event.attendees.length} attendee{event.attendees.length !== 1 ? 's' : ''}</span>
                        </div>
                      )}
                    </div>

                    {event.attendees.length > 0 && (
                      <div className="attendees-list">
                        {event.attendees.slice(0, 3).map((attendee, idx) => (
                          <div key={idx} className="attendee">
                            <div className="attendee-avatar">
                              {attendee.charAt(0).toUpperCase()}
                            </div>
                            <span className="attendee-email">{attendee}</span>
                          </div>
                        ))}
                        {event.attendees.length > 3 && (
                          <div className="more-attendees">
                            +{event.attendees.length - 3} more
                          </div>
                        )}
                      </div>
                    )}

                    <div className="event-actions">
                      {event.calendar_link && (
                        <button 
                          className="btn btn-primary btn-sm"
                          onClick={() => window.open(event.calendar_link, '_blank')}
                        >
                          <FiExternalLink />
                          Open in Calendar
                        </button>
                      )}
                      <button className="btn btn-secondary btn-sm">Edit</button>
                      <button className="btn btn-secondary btn-sm">View Email</button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          ))
        )}
      </div>

      {/* Summary Stats */}
      <motion.div 
        className="calendar-stats"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
      >
        <div className="stat-card">
          <div className="stat-icon">
            <FiCalendar />
          </div>
          <div className="stat-content">
            <h3>{events.length}</h3>
            <p>Total Events</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">
            <FiUser />
          </div>
          <div className="stat-content">
            <h3>{events.filter(e => e.attendees.length > 0).length}</h3>
            <p>Events with Attendees</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">
            <FiClock />
          </div>
          <div className="stat-content">
            <h3>{events.filter(e => e.priority === 'high').length}</h3>
            <p>High Priority</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Calendar; 