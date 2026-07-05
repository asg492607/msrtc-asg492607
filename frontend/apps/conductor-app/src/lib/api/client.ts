import { useAuthStore } from '../store/useAuthStore';

export const conductorApi = {
  getHeaders: () => {
    const token = useAuthStore.getState().conductor?.token;
    return {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    };
  },

  auth: {
    requestOtp: async (employeeId: string, phone: string) => {
      await new Promise(r => setTimeout(r, 600));
      console.log(`OTP sent to ${phone} for employee ${employeeId}`);
      return { success: true };
    },
    verifyOtp: async (employeeId: string, otp: string) => {
      await new Promise(r => setTimeout(r, 800));
      if (otp === '1234') {
        return {
          id: 'C-001',
          employeeId,
          name: 'Rajesh Kumar',
          phone: '9876543210',
          depotId: 'DEPOT-MUM-01',
          roles: ['CONDUCTOR'],
          token: 'mock-conductor-jwt-token'
        };
      }
      throw new Error('Invalid OTP');
    }
  },

  duty: {
    getTodaysRoster: async () => {
      await new Promise(r => setTimeout(r, 500));
      return [
        {
          dutyId: 'DUTY-001',
          date: new Date().toISOString().split('T')[0],
          shift: 'MORNING',
          busNumber: 'MH-01-AB-1234',
          routeId: 'R-MUM-PUN',
          source: 'Mumbai',
          destination: 'Pune',
          departureTime: '07:30',
          status: 'ACTIVE'
        },
        {
          dutyId: 'DUTY-002',
          date: new Date().toISOString().split('T')[0],
          shift: 'AFTERNOON',
          busNumber: 'MH-01-CD-5678',
          routeId: 'R-PUN-NAS',
          source: 'Pune',
          destination: 'Nashik',
          departureTime: '14:00',
          status: 'UPCOMING'
        }
      ];
    }
  },

  validate: {
    pass: async (passId: string) => {
      await new Promise(r => setTimeout(r, 500));
      if (passId.startsWith('PASS')) {
        return {
          valid: true,
          passId,
          passengerName: 'Suresh Pawar',
          validUntil: '2026-07-31',
          message: 'Monthly Pass valid — Board allowed'
        };
      }
      return { valid: false, message: 'Invalid or expired pass' };
    },

    ticket: async (qrData: string) => {
      await new Promise(r => setTimeout(r, 600));
      // Simulate validation — any valid-looking PNR succeeds
      if (qrData.startsWith('PNR')) {
        return {
          valid: true,
          pnr: qrData,
          passengerName: 'Amit Desai',
          seatNumber: '14',
          message: 'Ticket valid — Board allowed'
        };
      }
      return { valid: false, message: 'Invalid or expired ticket' };
    }
  },

  gps: {
    pushLocation: async (lat: number, lng: number, tripId: string) => {
      console.log(`GPS Update: ${lat}, ${lng} for trip ${tripId}`);
      return { success: true };
    }
  }
};
