'use client';

import { useState, useEffect } from 'react';
import { authService } from '@/services/auth';
import { User } from '@/services/auth';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticatedState, setIsAuthenticatedState] = useState<boolean>(false);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        setLoading(true);
        const authStatus = authService.isAuthenticated();
        setIsAuthenticatedState(authStatus);

        if (authStatus) {
          const currentUser = authService.getCurrentUser();
          setUser(currentUser);
        } else {
          setUser(null);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Authentication error');
        setUser(null);
        setIsAuthenticatedState(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setError(null);
      // Clear any existing user state before login
      setUser(null);
      setIsAuthenticatedState(false);
      const { user: userData } = await authService.login({ email, password });
      setUser(userData);
      setIsAuthenticatedState(true);
      // Force a state update to ensure UI re-renders
      setLoading(false);
      return { success: true, user: userData };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const register = async (email: string, password: string, name?: string) => {
    try {
      setError(null);
      // Clear any existing user state before registration/login
      setUser(null);
      setIsAuthenticatedState(false);
      const { user: userData } = await authService.register({ email, password, name });
      setUser(userData);
      setIsAuthenticatedState(true);
      // Force a state update to ensure UI re-renders
      setLoading(false);
      return { success: true, user: userData };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Registration failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticatedState(false);
    // Clear any stored conversation ID to prevent cross-user data leakage
    if (typeof window !== 'undefined') {
      localStorage.removeItem('chat_conversation_id');
    }
    // Trigger a re-render by updating loading state
    setLoading(false);
  };

  const isAuthenticated = () => {
    return isAuthenticatedState;
  };

  return {
    user,
    loading,
    error,
    isAuthenticated, // Use the state-based function
    login,
    register,
    logout,
  };
};