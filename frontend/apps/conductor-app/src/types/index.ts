export interface Conductor {
  id: string;
  employeeId: string;
  name: string;
  phone: string;
  depotId: string;
  roles: string[];
  token: string;
}

export interface DutyRoster {
  dutyId: string;
  date: string;
  shift: 'MORNING' | 'AFTERNOON' | 'NIGHT';
  busNumber: string;
  routeId: string;
  source: string;
  destination: string;
  departureTime: string;
  status: 'UPCOMING' | 'ACTIVE' | 'COMPLETED';
}

export interface ValidationResult {
  valid: boolean;
  pnr?: string;
  passengerName?: string;
  seatNumber?: string;
  message: string;
}
