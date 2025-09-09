import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiCalendar, FiClock, FiMapPin, FiExternalLink, FiFilter, FiSearch, FiPlus, FiArrowLeft } from 'react-icons/fi';
import { emailAPI } from '../services/api';
import './CalendarEvents.css';

const CalendarEvents = ({ onBack }) => {
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // all, upcoming, today, this_week
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState('list'); // list, calendar

  useEffect(() => {
    fetchCalendarEvents();
  }, []);

  const fetchCalendarEvents = async () => {
    try {
      setIsLoading(true);
      console.log('Fetching calendar events...');
      const response = await emailAPI.getEmailHistory();
      console.log('CalendarEvents API response:', response.data);
      
      if (response.data.success) {
        // Filter for event emails and transform into calendar events
        const eventEmails = response.data.emails.filter(email => 
          email.event_extracted && !email.spam_detected
        );
        
        const calendarEvents = eventEmails.map(email => {
          const eventData = email.event_data || {};
          
          // Fix date handling - use processed_at if start_time is invalid
          let startTime = eventData.start_time || email.date || email.processed_at;
          let endTime = eventData.end_time || null;
          
          // If startTime is still invalid, use current time
          if (!startTime || new Date(startTime).toString() === 'Invalid Date') {
            startTime = new Date().toISOString();
          }
          
          // If endTime is invalid, set it to 1 hour after startTime
          if (!endTime || new Date(endTime).toString() === 'Invalid Date') {
            endTime = new Date(new Date(startTime).getTime() + 60 * 60 * 1000).toISOString();
          }
          
          return {
            id: email.id,
            title: eventData.title || email.subject || 'Untitled Event',
            description: eventData.description || email.ai_summary || email.summary || 'No description available',
            startTime: startTime,
            endTime: endTime,
            location: eventData.location || null,
            attendees: eventData.attendees || [],
            calendarLink: eventData.calendar_link || null,
            sourceEmail: email,
            status: eventData.status || 'confirmed',
            priority: eventData.priority || 'medium',
            category: eventData.category || 'general'
          };
        });
        
        setEvents(calendarEvents);
      } else {
        setError('Failed to fetch calendar events');
      }
    } catch (error) {
      console.error('Error fetching calendar events:', error);
      setError('Error loading calendar events');
    } finally {
      setIsLoading(false);
    }
  };

  const getEventStatusColor = (status) => {
    switch (status) {
      case 'confirmed': return '#27ae60';
      case 'tentative': return '#f39c12';
      case 'cancelled': return '#e74c3c';
      default: return '#95a5a6';
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

  const isEventToday = (eventDate) => {
    const today = new Date();
    const event = new Date(eventDate);
    return event.toDateString() === today.toDateString();
  };

  const isEventUpcoming = (eventDate) => {
    const now = new Date();
    const event = new Date(eventDate);
    return event > now;
  };

  const isEventThisWeek = (eventDate) => {
    const now = new Date();
    const event = new Date(eventDate);
    const weekFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
    return event >= now && event <= weekFromNow;
  };

  const filteredEvents = events.filter(event => {
    const matchesSearch = event.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         event.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (event.location && event.location.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesFilter = filter === 'all' || 
                         (filter === 'upcoming' && isEventUpcoming(event.startTime)) ||
                         (filter === 'today' && isEventToday(event.startTime)) ||
                         (filter === 'this_week' && isEventThisWeek(event.startTime));
    
    return matchesSearch && matchesFilter;
  });

  const groupByDate = (events) => {
    const groups = {};
    events.forEach(event => {
      try {
        const date = new Date(event.startTime);
        if (date.toString() === 'Invalid Date') {
          console.warn('Invalid date for event:', event);
          return;
        }
        const dateString = date.toDateString();
        if (!groups[dateString]) {
          groups[dateString] = [];
        }
        groups[dateString].push(event);
      } catch (error) {
        console.error('Error processing date for event:', event, error);
      }
    });
    return groups;
  };

  const groupedEvents = groupByDate(filteredEvents);

  const openInCalendar = (event) => {
    if (event.calendarLink) {
      window.open(event.calendarLink, '_blank');
    } else {
      // Create a Google Calendar link
      const startDate = new Date(event.startTime).toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
      const endDate = event.endTime ? 
        new Date(event.endTime).toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z' :
        new Date(new Date(event.startTime).getTime() + 60 * 60 * 1000).toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
      
      const calendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(event.title)}&dates=${startDate}/${endDate}&details=${encodeURIComponent(event.description)}&location=${encodeURIComponent(event.location || '')}`;
      window.open(calendarUrl, '_blank');
    }
  };

  const addToCalendar = async (event) => {
    try {
      // Create event data for the backend
      const eventData = {
        title: event.title,
        description: event.description,
        start_time: event.startTime,
        end_time: event.endTime,
        location: event.location,
        attendees: event.attendees
      };

      // Call the backend API to add the event to Google Calendar
      const response = await fetch('http://localhost:5000/api/calendar/add-event', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ event_details: eventData })
      });

      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          alert('Event added to Google Calendar successfully!');
          // Optionally refresh the events list
          fetchCalendarEvents();
        } else {
          alert('Failed to add event to calendar: ' + (result.error || 'Unknown error'));
        }
      } else {
        alert('Failed to add event to calendar. Please try again.');
      }
    } catch (error) {
      console.error('Error adding event to calendar:', error);
      alert('Error adding event to calendar. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <div className="calendar-events-container">
        <div className="loading-spinner"></div>
        <p>Loading calendar events...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="calendar-events-container">
        <div className="error-message">
          <FiCalendar className="error-icon" />
          <p>{error}</p>
          <button onClick={fetchCalendarEvents} className="btn btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="calendar-events-container">
      <div className="calendar-events-header">
        <div className="calendar-events-title">
          {onBack && (
            <button className="back-button" onClick={onBack}>
              <FiArrowLeft />
              Back to Dashboard
            </button>
          )}
          <div className="title-content">
            <FiCalendar className="title-icon" />
            <h1>Calendar Events</h1>
            <span className="event-count">{filteredEvents.length} events</span>
          </div>
        </div>
        
        <div className="calendar-events-controls">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search events..."
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
              All Events
            </button>
            <button
              className={`filter-btn ${filter === 'today' ? 'active' : ''}`}
              onClick={() => setFilter('today')}
            >
              Today
            </button>
            <button
              className={`filter-btn ${filter === 'this_week' ? 'active' : ''}`}
              onClick={() => setFilter('this_week')}
            >
              This Week
            </button>
            <button
              className={`filter-btn ${filter === 'upcoming' ? 'active' : ''}`}
              onClick={() => setFilter('upcoming')}
            >
              Upcoming
            </button>
          </div>
        </div>
      </div>

      <div className="calendar-events-content">
        {Object.keys(groupedEvents).length === 0 ? (
          <div className="empty-state">
            <FiCalendar className="empty-icon" />
            <h3>No calendar events found</h3>
            <p>Process some emails with events to see your calendar here.</p>
          </div>
        ) : (
          Object.entries(groupedEvents).map(([date, dateEvents]) => (
            <motion.div
              key={date}
              className="date-group"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="date-header">
                <h2>{date}</h2>
                <span className="date-count">{dateEvents.length} events</span>
              </div>
              
              <div className="events-list">
                {dateEvents.map((event) => (
                  <motion.div
                    key={event.id}
                    className="event-card"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2 }}
                    whileHover={{ scale: 1.02 }}
                  >
                    <div className="event-header">
                      <div className="event-meta">
                        <div className="status-indicator" style={{ backgroundColor: getEventStatusColor(event.status) }}></div>
                        <div className="priority-indicator" style={{ backgroundColor: getPriorityColor(event.priority) }}></div>
                        <span className="event-time">
                          <FiClock />
                          {(() => {
                            try {
                              const startDate = new Date(event.startTime);
                              const endDate = event.endTime ? new Date(event.endTime) : null;
                              
                              if (startDate.toString() === 'Invalid Date') {
                                return 'Time TBD';
                              }
                              
                              const startTime = startDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                              const endTime = endDate && endDate.toString() !== 'Invalid Date' 
                                ? endDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                                : null;
                              
                              return endTime ? `${startTime} - ${endTime}` : startTime;
                            } catch (error) {
                              console.error('Error formatting time:', error);
                              return 'Time TBD';
                            }
                          })()}
                        </span>
                      </div>
                      
                      <div className="event-badges">
                        <span className="badge badge-status" style={{ backgroundColor: getEventStatusColor(event.status) }}>
                          {event.status}
                        </span>
                        {event.priority === 'high' && (
                          <span className="badge badge-priority">High Priority</span>
                        )}
                      </div>
                    </div>
                    
                    <div className="event-content">
                      <h3 className="event-title">{event.title}</h3>
                      <p className="event-description">{event.description}</p>
                      
                      {event.location && (
                        <div className="event-location">
                          <FiMapPin />
                          <span>{event.location}</span>
                        </div>
                      )}
                      
                      {event.attendees.length > 0 && (
                        <div className="event-attendees">
                          <span className="attendees-label">Attendees:</span>
                          <span className="attendees-list">{event.attendees.join(', ')}</span>
                        </div>
                      )}
                    </div>
                    
                    <div className="event-actions">
                      <button 
                        className="btn btn-sm btn-outline"
                        onClick={() => openInCalendar(event)}
                      >
                        <FiExternalLink />
                        Open in Calendar
                      </button>
                      <button 
                        className="btn btn-sm btn-primary"
                        onClick={() => addToCalendar(event)}
                      >
                        <FiPlus />
                        Add to Calendar
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

export default CalendarEvents;
