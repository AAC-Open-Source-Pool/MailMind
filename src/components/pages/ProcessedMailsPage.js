import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FiArrowLeft } from 'react-icons/fi';
import ProcessedMails from '../ProcessedMails';
import './PageLayout.css';

const ProcessedMailsPage = ({ user }) => {
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
          <h1>📧 Processed Mails</h1>
          <p>View all processed emails with AI analysis</p>
        </div>
      </div>
      
      <div className="page-content">
        <ProcessedMails user={user} onBack={handleBack} />
      </div>
    </div>
  );
};

export default ProcessedMailsPage;
