import { useAuthStore } from '../../store/useAuthStore';

// Mock implementation of the generated SDK client with Auth Injection
export const apiClient = {
  getHeaders: () => {
    const token = useAuthStore.getState().token;
    return {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    };
  },

  routes: {
    search: async (from: string, to: string, date: string) => {
      console.log('Searching routes', from, to, date, 'Headers:', apiClient.getHeaders());
      return [];
    }
  },
  
  auth: {
    login: async (phone: string, otp: string) => {
      console.log('Verifying OTP', phone, otp);
      // Simulate backend response
      if (otp === '1234') {
         return {
           token: 'mock-jwt-token-xyz',
           user: { id: 'u1', phone, roles: ['PASSENGER'] }
         };
      }
      throw new Error("Invalid OTP");
    }
  }
};
