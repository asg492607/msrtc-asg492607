export interface Trip {
  id: string;
  routeId: string;
  source: string;
  destination: string;
  departureTime: string; // ISO String
  arrivalTime: string;   // ISO String
  durationMinutes: number;
  busType: 'Shivneri' | 'Shivshahi' | 'Ordinary' | 'Hirkani';
  availableSeats: number;
  baseFare: number;
  liveStatus: 'ON_TIME' | 'DELAYED';
}
