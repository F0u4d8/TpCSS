export interface User {
  id: number;
  email: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  error: string | null;
}

export interface AuthActions {
  setUser: (user: User) => void;
  clearAuth: () => void;
  setError: (error: string | null) => void;
}

export interface AuthStore extends AuthState, AuthActions {}
