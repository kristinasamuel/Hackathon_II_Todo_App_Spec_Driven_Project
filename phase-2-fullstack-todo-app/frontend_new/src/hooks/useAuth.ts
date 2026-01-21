'use client';

import { useState, useEffect } from 'react';
import { authService } from '@/services/auth';
import { User } from '@/services/auth';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        setLoading(true);
        if (authService.isAuthenticated()) {
          const currentUser = authService.getCurrentUser();
          setUser(currentUser);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Authentication error');
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setError(null);
      const { user: userData } = await authService.login({ email, password });
      setUser(userData);
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
      const { user: userData } = await authService.register({ email, password, name });
      setUser(userData);
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
  };

  const isAuthenticated = () => {
    return authService.isAuthenticated() && !!user;
  };

  return {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated,
  };
};