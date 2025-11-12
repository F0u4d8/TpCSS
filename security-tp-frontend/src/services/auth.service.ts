const API_BASE_URL = 'http://localhost:3000/api/auth';

export interface RegisterData {
  username : string ;
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export class AuthService {
  static async register(data: RegisterData) {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Registration failed');
    }

    return response.json();
  }

  static async login(data: LoginData) {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Login failed');
    }

    return response.json();
  }

  /**
   * Get user profile
   * ⚠️ Phase 1: Backend can't verify this request
   */
  static async getProfile(userId: number) {
    const response = await fetch(`${API_BASE_URL}/profile/${userId}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to get profile');
    }

    return response.json();
  }

  /**
   * Get all users (mock admin endpoint)
   * ⚠️ Phase 1: No authorization check
   */
  static async getAllUsers() {
    const response = await fetch(`${API_BASE_URL}/users`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to get users');
    }

    return response.json();
  }
}
