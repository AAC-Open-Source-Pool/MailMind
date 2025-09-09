import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FiArrowLeft } from 'react-icons/fi';
import CalendarEvents from '../CalendarEvents';
import './PageLayout.css';

const CalendarEventsPage = ({ user }) => {
  const navigate = useNavigate();

  const handleBack = () => {
    navigate('/dashboard');
  };

  return (
    <div className="page-layout">
      <div className="page-header">
        <button className="back-button" onClick={handleBack}>
          <FiArrowLeft />
          Back to Dashboard
        </button>
        <div className="page-title">
          <h1>📅 Calendar Events</h1>
          <p>View and manage your calendar events</p>
        </div>
      </div>
      
      <div className="page-content">
        <CalendarEvents user={user} onBack={handleBack} />
      </div>
    </div>
  );
};

export default CalendarEventsPage;
