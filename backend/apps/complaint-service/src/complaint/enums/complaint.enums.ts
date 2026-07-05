export enum ComplaintStatus {
  OPEN = 'OPEN',
  ASSIGNED = 'ASSIGNED',
  IN_PROGRESS = 'IN_PROGRESS',
  ESCALATED = 'ESCALATED',
  RESOLVED = 'RESOLVED',
  CLOSED = 'CLOSED',
}

export enum ComplaintPriority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL',
}

export enum ComplaintCategory {
  STAFF_BEHAVIOR = 'STAFF_BEHAVIOR',
  BUS_CLEANLINESS = 'BUS_CLEANLINESS',
  DELAY = 'DELAY',
  TICKET_ISSUE = 'TICKET_ISSUE',
  OTHER = 'OTHER',
}
