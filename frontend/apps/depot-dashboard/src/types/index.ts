export interface Bus {
  id: string; busNumber: string; type: string;
  status: 'OPERATIONAL' | 'IN_MAINTENANCE' | 'BREAKDOWN' | 'IDLE';
  driver?: string; conductor?: string; route?: string;
  lastService: string; nextServiceDue: string; kmToday: number;
  fuelLevel: number;
}

export interface TripEntry {
  tripId: string; route: string; busNumber: string;
  departure: string; arrival: string;
  status: 'ON_TIME' | 'DELAYED' | 'DEPARTED' | 'ARRIVED' | 'CANCELLED';
  passengerCount: number; capacity: number;
}

export interface CrewMember {
  id: string; name: string; role: 'DRIVER' | 'CONDUCTOR';
  employeeId: string; phone: string; shift: string;
  status: 'ON_DUTY' | 'OFF_DUTY' | 'LEAVE' | 'AVAILABLE';
  assignedBus?: string; assignedRoute?: string;
}

export interface MaintenanceJob {
  id: string; busNumber: string; type: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  status: 'OPEN' | 'IN_PROGRESS' | 'COMPLETED';
  mechanic?: string; openedAt: string; estimatedCompletion: string;
}

export interface SparePart {
  id: string; name: string; partNumber: string;
  stock: number; minStock: number; unit: string; unitPrice: number;
}
