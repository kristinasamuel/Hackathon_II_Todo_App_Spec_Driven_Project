import api from './api';
import logger from '../utils/logger';
import { LoginCredentials, SignupData, User, AuthResponse, LoginResponse } from '../types/auth';


class AuthService {
  /**
   * Login user and store JWT token
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse | null> {
    try {
      logger.info('Attempting user login', { email: credentials.email });

      // Since we're integrating with Better Auth, we'll simulate the login
      // In a real implementation, this would call the actual backend auth endpoint
      const response = await api.post('/auth/login', credentials);

      if (response.data && response.data.token) {
        const { token, refresh_token } = response.data;
        localStorage.setItem('jwt_token', token);
        if (refresh_token) {
          localStorage.setItem('refresh_token', refresh_token);
        }
        logger.info('User login successful', { user_id: response.data.user?.user_id });
        return { user: response.data.user, token };
      }

      logger.warn('Login failed - no token returned', { email: credentials.email });
      return null;
    } catch (error: any) {
      logger.error('Login error', {
        email: credentials.email,
        error: error.response?.data?.message || error.message
      }, error);
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  }

  /**
   * Signup user and store JWT token
   */
  async signup(userData: SignupData): Promise<LoginResponse | null> {
    try {
      logger.info('Attempting user signup', { email: userData.email });

      // In a real implementation, this would call the actual backend signup endpoint
      const response = await api.post('/auth/signup', userData);

      if (response.data && response.data.token) {
        const { token, refresh_token } = response.data;
        localStorage.setItem('jwt_token', token);
        if (refresh_token) {
          localStorage.setItem('refresh_token', refresh_token);
        }
        logger.info('User signup successful', { user_id: response.data.user?.user_id });
        return { user: response.data.user, token };
      }

      logger.warn('Signup failed - no token returned', { email: userData.email });
      return null;
    } catch (error: any) {
      logger.error('Signup error', {
        email: userData.email,
        error: error.response?.data?.message || error.message
      }, error);
      throw new Error(error.response?.data?.message || 'Signup failed');
    }
  }

  /**
   * Logout user and remove JWT token
   */
  logout(): void {
    const token = this.getToken();
    logger.info('User logout initiated', { has_token: !!token });

    localStorage.removeItem('jwt_token');
    localStorage.removeItem('refresh_token');

    // Redirect to login page
    window.location.href = '/login';

    logger.info('User logout completed');
  }

  /**
   * Get current user info
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      const response = await api.get('/auth/me');
      logger.info('Current user info retrieved', { user_id: response.data?.user_id });
      return response.data;
    } catch (error: any) {
      logger.error('Error getting current user info', { error: error.message }, error);
      return null;
    }
  }

  /**
   * Validate JWT token
   */
  async validateToken(): Promise<AuthResponse> {
    try {
      const token = localStorage.getItem('jwt_token');
      if (!token) {
        logger.info('Token validation failed - no token found');
        // Don't redirect here, just return invalid status
        return { valid: false, user_id: '' };
      }

      logger.debug('Validating JWT token');

      // Call the backend validation endpoint
      const response = await api.post('/auth/validate', {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      logger.info('Token validation successful', { user_id: response.data?.user_id });
      return response.data;
    } catch (error: any) {
      logger.error('Token validation error', {
        error: error.message,
        status: error.response?.status
      }, error);

      // Don't redirect here, just return invalid status
      // Individual components can decide whether to redirect based on route
      return { valid: false, user_id: '', error: error.message };
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = localStorage.getItem('jwt_token');
    logger.debug('Authentication check', { is_authenticated: !!token });
    return !!token;
  }

  /**
   * Get JWT token
   */
  getToken(): string | null {
    return localStorage.getItem('jwt_token');
  }

  /**
   * Get refresh token
   */
  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  /**
   * Refresh the JWT token using the refresh token
   */
  async refreshToken(): Promise<string | null> {
    try {
      const refreshToken = this.getRefreshToken();
      logger.info('Attempting token refresh');

      if (!refreshToken) {
        logger.warn('Token refresh failed - no refresh token available');
        return null;
      }

      const response = await api.post('/auth/refresh', {}, {
        headers: {
          Authorization: `Bearer ${refreshToken}`
        }
      });

      if (response.data && response.data.access_token) {
        const newToken = response.data.access_token;
        localStorage.setItem('jwt_token', newToken);
        // Update refresh token if provided in response
        if (response.data.refresh_token) {
          localStorage.setItem('refresh_token', response.data.refresh_token);
        }
        logger.info('Token refresh successful');
        return newToken;
      }

      logger.warn('Token refresh failed - no access token in response');
      return null;
    } catch (error: any) {
      logger.error('Token refresh error', {
        error: error.response?.data?.message || error.message
      }, error);
      // If refresh fails, clear tokens and redirect to login
      this.logout();
      throw new Error(error.response?.data?.message || 'Token refresh failed');
    }
  }
}

export default new AuthService();