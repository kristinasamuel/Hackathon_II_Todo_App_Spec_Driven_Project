import axios, { AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import logger from '../utils/logger';

// Create an axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});


// Request interceptor to add JWT token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    logger.error('API request error', { error: error.message }, error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration and network issues
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    // Log the error with context
    logger.error('API response error', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      statusText: error.response?.statusText,
      message: error.message
    }, error);

    // Handle network connectivity issues
    if (!error.response) {
      logger.warn('Network connectivity issue detected', { message: error.message || 'Network error' });
      // Could implement retry mechanism here if needed
      return Promise.reject(error);
    }

    // Handle token expiration (401 Unauthorized)
    if (error.response.status === 401 && !originalRequest._retry) {
      logger.warn('Token expired or invalid, removing tokens');
      // Token is invalid/expired, remove tokens
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('refresh_token');

      // Only redirect to login if the user is on a protected route
      // We can check the URL to determine if it's a protected route
      const currentPath = window.location.pathname;
      const protectedPaths = ['/dashboard', '/tasks', '/profile'];

      if (protectedPaths.some(path => currentPath.startsWith(path))) {
        // If on a protected route, redirect to login
        window.location.href = '/login';
      }

      return Promise.reject(error);
    }

    // Handle temporarily unavailable backend API (5xx errors)
    if (error.response.status >= 500) {
      logger.error('Backend API unavailable', {
        status: error.response.status,
        statusText: error.response.statusText,
        url: error.config?.url
      });
      // Could implement retry mechanism with exponential backoff here
    }

    // Handle unauthorized resource access attempts (403 Forbidden)
    if (error.response.status === 403) {
      logger.warn('Unauthorized access attempt', {
        status: error.response.status,
        url: error.config?.url,
        data: error.response.data
      });
      // Redirect to login or show unauthorized page
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

export default api;