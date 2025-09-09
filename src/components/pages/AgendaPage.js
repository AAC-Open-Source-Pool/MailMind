import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FiArrowLeft } from 'react-icons/fi';
import Agenda from '../Agenda';
import './PageLayout.css';

const AgendaPage = ({ user }) => {
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
          <h1>📋 Email Agenda</h1>
          <p>Non-event emails organized by priority</p>
        </div>
      </div>
      
      <div className="page-content">
        <Agenda user={user} onBack={handleBack} />
      </div>
    </div>
  );
};

export default AgendaPage;
