import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Don't auto-login from localStorage - require proper authentication
    // This ensures users go through the landing page -> sign in flow
    setIsLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials);
      
      if (response.data.success) {
        const userData = {
          id: response.data.user_id,
          email: credentials.email,
          fullName: credentials.email.split('@')[0], // Fallback name
          // Add more user data as needed
        };
        
        setUser(userData);
        setIsAuthenticated(true);
        localStorage.setItem('mailmind_user', JSON.stringify(userData));
        
        return { success: true, user: userData };
      } else {
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed. Please try again.' 
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      
      if (response.data.success) {
        const newUser = {
          id: response.data.user_id,
          email: userData.email,
          fullName: userData.name || userData.email.split('@')[0],
          // Add more user data as needed
        };
        
        setUser(newUser);
        setIsAuthenticated(true);
        localStorage.setItem('mailmind_user', JSON.stringify(newUser));
        
        return { success: true, user: newUser };
      } else {
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || 'Registration failed. Please try again.' 
      };
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setIsAuthenticated(false);
      localStorage.removeItem('mailmind_user');
      localStorage.removeItem('auth_token');
    }
  };

  const setOAuthUser = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
    localStorage.setItem('mailmind_user', JSON.stringify(userData));
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    setOAuthUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
