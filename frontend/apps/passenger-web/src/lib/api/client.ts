// Mock implementation of the generated SDK client
export const apiClient = {
  routes: {
    search: async (from: string, to: string, date: string) => {
      // In reality, this calls: fetch('https://api.msrtc.gov.in/v1/routes?from=...')
      console.log('Searching routes', from, to, date);
      return [];
    }
  },
  auth: {
    login: async (phone: string) => {
      console.log('Requesting OTP', phone);
      return { success: true };
    }
  }
};
