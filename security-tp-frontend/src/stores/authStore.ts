import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { User } from '../types/auth.types';

interface AuthStore {
  user: User | null;
  isAuthenticated: boolean;
  error: string | null;
  
  setUser: (user: User) => void;
  clearAuth: () => void;
  setError: (error: string | null) => void;
}

export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      (set) => ({
        // State
        user: null,
        isAuthenticated: false,
        error: null,

        // Actions
        setUser: (user: User) => {
          set({
            user,
            isAuthenticated: true,
            error: null,
          });
        },

        clearAuth: () => {
          set({
            user: null,
            isAuthenticated: false,
            error: null,
          });
        },

        setError: (error: string | null) => {
          set({ error });
        },
      }),
      {
        name: 'auth-storage',
      }
    ),
    { name: 'AuthStore' }
  )
);
