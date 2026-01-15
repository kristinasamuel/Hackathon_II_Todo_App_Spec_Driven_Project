/**
 * JWT Utilities for frontend
 */

interface DecodedToken {
  user_id: string;
  exp: number;
  iat: number;
  email?: string;
}

/**
 * Decode a JWT token without verifying signature (client-side only)
 */
export function decodeToken(token: string): DecodedToken | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid token format');
    }

    const payload = parts[1];
    // Add padding if needed
    const paddedPayload = payload + '='.repeat((4 - (payload.length % 4)) % 4);
    const decodedPayload = atob(paddedPayload);
    return JSON.parse(decodedPayload);
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
}

/**
 * Check if token is expired
 */
export function isTokenExpired(token: string): boolean {
  const decoded = decodeToken(token);
  if (!decoded || !decoded.exp) {
    return true; // Consider invalid tokens as expired
  }

  const currentTime = Math.floor(Date.now() / 1000);
  return decoded.exp < currentTime;
}

/**
 * Get token expiration time
 */
export function getTokenExpiration(token: string): Date | null {
  const decoded = decodeToken(token);
  if (!decoded || !decoded.exp) {
    return null;
  }

  return new Date(decoded.exp * 1000);
}

/**
 * Get user ID from token
 */
export function getUserIdFromToken(token: string): string | null {
  const decoded = decodeToken(token);
  return decoded ? decoded.user_id : null;
}

/**
 * Check if token will expire soon (within 5 minutes)
 */
export function isTokenExpiringSoon(token: string): boolean {
  const decoded = decodeToken(token);
  if (!decoded || !decoded.exp) {
    return true; // Consider invalid tokens as expiring soon
  }

  const currentTime = Math.floor(Date.now() / 1000);
  const fiveMinutes = 5 * 60; // 5 minutes in seconds
  return decoded.exp - currentTime < fiveMinutes;
}

/**
 * Store token in local storage
 */
export function storeToken(token: string): void {
  localStorage.setItem('jwt_token', token);
}

/**
 * Get token from local storage
 */
export function getToken(): string | null {
  return localStorage.getItem('jwt_token');
}

/**
 * Remove token from local storage
 */
export function removeToken(): void {
  localStorage.removeItem('jwt_token');
}