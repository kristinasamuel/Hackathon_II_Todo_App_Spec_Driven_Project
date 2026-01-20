import api from './api';
import { jwtDecode } from 'jwt-decode';

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterCredentials {
  email: string;
  password: string;
  name?: string;
}

interface User {
  id: string;
  email: string;
  name?: string;
}

// Safe storage helper to handle SSR
const safeLocalStorage = {
  getItem: (key: string): string | null => {
    if (typeof window !== 'undefined' && window.localStorage) {
      return window.localStorage.getItem(key);
    }
    return null;
  },
  setItem: (key: string, value: string): void => {
    if (typeof window !== 'undefined' && window.localStorage) {
      window.localStorage.setItem(key, value);
    }
  },
  removeItem: (key: string): void => {
    if (typeof window !== 'undefined' && window.localStorage) {
      window.localStorage.removeItem(key);
    }
  }
};

class AuthService {
  async login(credentials: LoginCredentials): Promise<{ user: User; token: string }> {
    try {
      const response = await api.post('/auth/login', credentials);
      const { token } = response.data;

      if (token) {
        safeLocalStorage.setItem('jwt_token', token);
      }

      const decodedUser = jwtDecode(token) as any;
      const user: User = {
        id: decodedUser.user_id || decodedUser.sub,
        email: decodedUser.email,
        name: decodedUser.name || decodedUser.email.split('@')[0],
      };

      return { user, token };
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  }

  async register(credentials: RegisterCredentials): Promise<{ user: User; token: string }> {
    try {
      const response = await api.post('/auth/signup', credentials);
      const { token } = response.data;

      if (token) {
        safeLocalStorage.setItem('jwt_token', token);
      }

      const decodedUser = jwtDecode(token) as any;
      const user: User = {
        id: decodedUser.user_id || decodedUser.sub,
        email: decodedUser.email,
        name: decodedUser.name || decodedUser.email.split('@')[0],
      };

      return { user, token };
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  }

  logout(): void {
    safeLocalStorage.removeItem('jwt_token');
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) {
      return false;
    }

    try {
      const decoded = jwtDecode(token) as any;
      const currentTime = Date.now() / 1000;
      return decoded.exp > currentTime;
    } catch (error) {
      return false;
    }
  }

  getToken(): string | null {
    return safeLocalStorage.getItem('jwt_token');
  }

  getCurrentUser(): User | null {
    const token = this.getToken();
    if (!token || !this.isAuthenticated()) {
      return null;
    }

    try {
      const decoded = jwtDecode(token) as any;
      return {
        id: decoded.user_id || decoded.sub,
        email: decoded.email,
        name: decoded.name || decoded.email.split('@')[0],
      };
    } catch (error) {
      return null;
    }
  }
}

export const authService = new AuthService();
export default authService;