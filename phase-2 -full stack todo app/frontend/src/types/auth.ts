export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  email: string;
  password: string;
  name: string;
}

export interface User {
  user_id: string;
  email: string;
  created_at: string;
}

export interface AuthResponse {
  valid: boolean;
  user_id: string;
  email?: string;
  expires_at?: string;
  error?: string; // Added to handle error cases
}

export interface LoginResponse {
  user: User;
  token: string;
  refresh_token?: string;
}