import React from 'react';
import Navigation from './Navigation';
import './Layout.css';

const Layout = ({ children, user }) => {
  return (
    <div className="app-layout">
      <Navigation user={user} />
      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

export default Layout;
