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
    search: async (from: string, to: string, date: string): Promise<any[]> => {
      console.log('Searching routes', from, to, date, 'Headers:', apiClient.getHeaders());
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 800));
      return [
        {
          id: 'TRIP-101', routeId: 'R-MUM-PUN', source: from, destination: to,
          departureTime: '2026-07-10T08:00:00Z', arrivalTime: '2026-07-10T11:30:00Z', durationMinutes: 210,
          busType: 'Shivneri', availableSeats: 12, baseFare: 550, liveStatus: 'ON_TIME'
        },
        {
          id: 'TRIP-102', routeId: 'R-MUM-PUN', source: from, destination: to,
          departureTime: '2026-07-10T09:15:00Z', arrivalTime: '2026-07-10T13:00:00Z', durationMinutes: 225,
          busType: 'Shivshahi', availableSeats: 30, baseFare: 350, liveStatus: 'DELAYED'
        }
      ];
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
