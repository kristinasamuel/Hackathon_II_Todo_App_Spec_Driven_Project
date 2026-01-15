import AuthService from '../../src/services/auth';
import api from '../../src/services/api';

// Mock the api module
jest.mock('../../src/services/api', () => ({
  post: jest.fn(),
  get: jest.fn(),
  put: jest.fn(),
  patch: jest.fn(),
  delete: jest.fn(),
}));

// Mock localStorage
const mockLocalStorage = (() => {
  let store: {[key: string]: string} = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

// Mock window.location
const mockWindowLocation: {href: string} = {
  href: '',
};

Object.defineProperty(global, 'localStorage', {
  value: mockLocalStorage,
});

Object.defineProperty(global, 'location', {
  value: mockWindowLocation,
});

describe('AuthService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockLocalStorage.clear();
    mockWindowLocation.href = '';
  });

  describe('login functionality', () => {
    // T018: Test login functionality with valid credentials
    test('T018: should successfully login with valid credentials and store token', async () => {
      const mockCredentials = { email: 'test@example.com', password: 'password123' };
      const mockResponse = {
        data: {
          token: 'mock-jwt-token',
          user: {
            user_id: 'user123',
            email: 'test@example.com',
            created_at: '2023-01-01T00:00:00Z',
          },
        },
      };

      api.post.mockResolvedValue(mockResponse);

      const result = await AuthService.login(mockCredentials);

      expect(api.post).toHaveBeenCalledWith('/auth/login', mockCredentials);
      expect(result).toEqual({
        user: mockResponse.data.user,
        token: mockResponse.data.token,
      });
      expect(mockLocalStorage.getItem('jwt_token')).toBe('mock-jwt-token');
    });

    // T020: Test authentication failure handling with invalid credentials
    test('T020: should handle authentication failure with invalid credentials', async () => {
      const mockCredentials = { email: 'invalid@example.com', password: 'wrongpassword' };
      const mockError = {
        response: {
          data: {
            message: 'Invalid credentials',
          },
        },
      };

      api.post.mockRejectedValue(mockError);

      await expect(AuthService.login(mockCredentials)).rejects.toThrow('Invalid credentials');
      expect(api.post).toHaveBeenCalledWith('/auth/login', mockCredentials);
      expect(mockLocalStorage.getItem('jwt_token')).toBeNull();
    });
  });

  describe('signup functionality', () => {
    // T019: Test signup functionality with valid credentials
    test('T019: should successfully signup with valid credentials and store token', async () => {
      const mockUserData = {
        email: 'newuser@example.com',
        password: 'password123',
        name: 'New User',
      };
      const mockResponse = {
        data: {
          token: 'mock-jwt-token',
          user: {
            user_id: 'newuser123',
            email: 'newuser@example.com',
            created_at: '2023-01-01T00:00:00Z',
          },
        },
      };

      api.post.mockResolvedValue(mockResponse);

      const result = await AuthService.signup(mockUserData);

      expect(api.post).toHaveBeenCalledWith('/auth/signup', mockUserData);
      expect(result).toEqual({
        user: mockResponse.data.user,
        token: mockResponse.data.token,
      });
      expect(mockLocalStorage.getItem('jwt_token')).toBe('mock-jwt-token');
    });

    // T020: Test authentication failure handling with invalid signup data
    test('T020: should handle signup failure with invalid data', async () => {
      const mockUserData = {
        email: 'invalid-email',
        password: 'short',
        name: 'Test User',
      };
      const mockError = {
        response: {
          data: {
            message: 'Invalid signup data',
          },
        },
      };

      api.post.mockRejectedValue(mockError);

      await expect(AuthService.signup(mockUserData)).rejects.toThrow('Invalid signup data');
      expect(api.post).toHaveBeenCalledWith('/auth/signup', mockUserData);
      expect(mockLocalStorage.getItem('jwt_token')).toBeNull();
    });
  });

  describe('authentication state', () => {
    test('should return isAuthenticated as true when token exists', () => {
      mockLocalStorage.setItem('jwt_token', 'mock-jwt-token');
      expect(AuthService.isAuthenticated()).toBe(true);
    });

    test('should return isAuthenticated as false when token does not exist', () => {
      expect(AuthService.isAuthenticated()).toBe(false);
    });

    test('should return token when it exists', () => {
      mockLocalStorage.setItem('jwt_token', 'mock-jwt-token');
      expect(AuthService.getToken()).toBe('mock-jwt-token');
    });

    test('should return null when token does not exist', () => {
      expect(AuthService.getToken()).toBeNull();
    });
  });

  describe('logout functionality', () => {
    test('should remove token and redirect on logout', () => {
      mockLocalStorage.setItem('jwt_token', 'mock-jwt-token');
      AuthService.logout();
      expect(mockLocalStorage.getItem('jwt_token')).toBeNull();
      expect(mockWindowLocation.href).toBe('/login');
    });
  });

  describe('token validation', () => {
    test('should validate existing token', async () => {
      const mockToken = 'mock-jwt-token';
      const mockValidationResponse = {
        data: {
          valid: true,
          user_id: 'user123',
          email: 'test@example.com',
        },
      };

      mockLocalStorage.setItem('jwt_token', mockToken);
      api.post.mockResolvedValue(mockValidationResponse);

      const result = await AuthService.validateToken();

      expect(api.post).toHaveBeenCalledWith('/auth/validate', {}, {
        headers: {
          Authorization: `Bearer ${mockToken}`
        }
      });
      expect(result).toEqual(mockValidationResponse.data);
    });

    test('should return invalid when no token exists', async () => {
      const result = await AuthService.validateToken();
      expect(result).toEqual({ valid: false, user_id: '' });
      expect(api.post).not.toHaveBeenCalled();
    });
  });
});