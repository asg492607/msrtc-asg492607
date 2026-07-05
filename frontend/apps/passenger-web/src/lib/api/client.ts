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
  

  seats: {
    getLayout: async (tripId: string) => {
      console.log('Fetching layout for', tripId);
      await new Promise(r => setTimeout(r, 500));
      // Generate a mock 2x2 layout (4 columns: [Seat, Seat, Aisle, Seat, Seat])
      // We will model the aisle as empty space in the component, so columns 1,2 and 4,5
      const mockSeats = [];
      let seatCounter = 1;
      for(let r=1; r<=10; r++) {
         for(let c of [1,2, 4,5]) {
            let status = 'AVAILABLE';
            if(r === 1 && c === 1) status = 'BOOKED';
            if(r === 2 && c === 4) status = 'LOCKED';
            if(r === 3 && c === 1) status = 'LADIES_ONLY';
            
            mockSeats.push({
              id: `S-${r}-${c}`,
              row: r, col: c,
              status,
              fare: 500,
              number: `${seatCounter++}`
            });
         }
      }
      return { tripId, rows: 10, cols: 5, seats: mockSeats };
    },
    lockSeats: async (tripId: string, seatIds: string[]) => {
      console.log('Attempting Redis Lock for', seatIds);
      await new Promise(r => setTimeout(r, 800));
      // Simulate 10% chance of 409 Conflict (someone else locked it)
      if (Math.random() > 0.9) {
         throw new Error("409_CONFLICT: One or more seats are no longer available.");
      }
      return { success: true, expiresAt: Date.now() + 10 * 60 * 1000 };
    }
  },

  booking: {
    createBooking: async (data: any) => {
      console.log('Creating pending booking', data);
      await new Promise(r => setTimeout(r, 1000));
      // Simulate backend validation or success
      return { success: true, bookingId: `BKG-${Math.floor(Math.random() * 1000000)}` };
    }
  },

  payment: {
    initiate: async (bookingId: string, method: string) => {
      console.log('Initiating payment for', bookingId, method);
      await new Promise(r => setTimeout(r, 500));
      return { paymentIntentId: `PI-${Date.now()}` };
    },
    // Simulating webhook polling
    getStatus: async (bookingId: string) => {
      console.log('Polling payment status for', bookingId);
      // In a real app, this queries the backend which listens to razorpay webhooks
      // For this demo, we use localStorage to mock backend state changes made by the simulator
      const status = localStorage.getItem(`mock_payment_${bookingId}`);
      if (status === 'SUCCESS') return { status: 'CONFIRMED', pnr: `PNR${Math.floor(Math.random()*100000)}` };
      if (status === 'FAILED') return { status: 'FAILED' };
      return { status: 'PENDING' };
    }
  },
  ticket: {
    get: async (pnr: string) => {
      console.log('Fetching ticket', pnr);
      await new Promise(r => setTimeout(r, 500));
      return {
        pnr,
        status: 'CONFIRMED',
        source: 'Mumbai', destination: 'Pune',
        departureTime: '2026-07-10T08:00:00Z',
        busType: 'Shivneri',
        seats: ['1', '2'],
        passengers: [{ name: 'John Doe', age: 30, gender: 'MALE' }]
      };
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
