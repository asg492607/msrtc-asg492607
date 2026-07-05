import { create } from 'zustand';
import { Conductor } from '../types';

interface AuthState {
  conductor: Conductor | null;
  isAuthenticated: boolean;
  login: (conductor: Conductor) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  conductor: null,
  isAuthenticated: false,
  login: (conductor) => set({ conductor, isAuthenticated: true }),
  logout: () => set({ conductor: null, isAuthenticated: false }),
}));
