import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend"

directories = [
    "apps/gps-service",
    "apps/notification-service",
    "apps/complaint-service",
    "apps/pass-service",
    "apps/parcel-service"
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

schema_path = os.path.join(base_dir, "packages", "database", "prisma", "schema.prisma")

new_models = """

// ==========================================
// TASK 11: GPS Tracking & Live Operations
// ==========================================

model GpsLog {
  id             String   @id @default(uuid())
  busId          String
  tripInstanceId String?
  latitude       Float
  longitude      Float
  speed          Float
  heading        Float?
  accuracy       Float?
  timestamp      DateTime @default(now())
  
  bus            Bus      @relation(fields: [busId], references: [id])
}

model TripTracking {
  id             String   @id @default(uuid())
  tripInstanceId String   @unique
  currentStopId  String?
  nextStopId     String?
  distanceCovered Float
  status         String   // ON_TIME, MINOR_DELAY, MAJOR_DELAY, CRITICAL
  delayMinutes   Int      @default(0)
  updatedAt      DateTime @updatedAt
  
  trip           TripInstance @relation(fields: [tripInstanceId], references: [id])
}

model TripEta {
  id             String   @id @default(uuid())
  tripInstanceId String
  stopId         String
  estimatedTime  DateTime
  updatedAt      DateTime @updatedAt
  
  trip           TripInstance @relation(fields: [tripInstanceId], references: [id])
}

model GeofenceEvent {
  id             String   @id @default(uuid())
  busId          String
  geofenceType   String   // DEPOT, TERMINAL, STOP
  locationId     String
  eventType      String   // ENTRY, EXIT
  timestamp      DateTime @default(now())
  
  bus            Bus      @relation(fields: [busId], references: [id])
}

// ==========================================
// TASK 12: Notification Service
// ==========================================

model Notification {
  id             String   @id @default(uuid())
  userId         String
  type           String   // SMS, EMAIL, PUSH, WHATSAPP, IN_APP
  category       String   // BOOKING, COMPLAINT, ALERT
  title          String?
  content        String
  status         String   // PENDING, SENT, FAILED, DELIVERED, READ
  scheduledFor   DateTime?
  createdAt      DateTime @default(now())
  
  user           User     @relation(fields: [userId], references: [id])
  logs           NotificationLog[]
}

model NotificationLog {
  id             String   @id @default(uuid())
  notificationId String
  status         String
  providerRes    String?
  timestamp      DateTime @default(now())
  
  notification   Notification @relation(fields: [notificationId], references: [id])
}

model Template {
  id             String   @id @default(uuid())
  name           String   @unique
  type           String   // SMS, EMAIL
  content        String
  variables      String   // JSON string of required variables
  isActive       Boolean  @default(true)
}

// ==========================================
// TASK 13: Complaint & Grievance Management
// ==========================================

model Complaint {
  id             String   @id @default(uuid())
  userId         String
  category       String   // DELAY, STAFF, REFUND, BUS_CONDITION
  description    String
  tripInstanceId String?
  status         String   // OPEN, ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED
  assignedTo     String?  // Admin User ID
  escalationLevel Int     @default(0)
  createdAt      DateTime @default(now())
  updatedAt      DateTime @updatedAt
  
  user           User     @relation(fields: [userId], references: [id])
  comments       ComplaintComment[]
  sla            ComplaintSla?
}

model ComplaintComment {
  id             String   @id @default(uuid())
  complaintId    String
  userId         String
  comment        String
  timestamp      DateTime @default(now())
  
  complaint      Complaint @relation(fields: [complaintId], references: [id])
}

model ComplaintSla {
  id             String   @id @default(uuid())
  complaintId    String   @unique
  priority       String   // LOW, MEDIUM, HIGH, CRITICAL
  dueDate        DateTime
  isBreached     Boolean  @default(false)
  
  complaint      Complaint @relation(fields: [complaintId], references: [id])
}

// ==========================================
// TASK 14: Bus Pass Management
// ==========================================

model PassType {
  id             String   @id @default(uuid())
  name           String   // STUDENT, SENIOR, MONTHLY
  validityDays   Int
  price          Float
  isActive       Boolean  @default(true)
  passes         Pass[]
}

model Pass {
  id             String   @id @default(uuid())
  userId         String
  passTypeId     String
  status         String   // PENDING, APPROVED, ACTIVE, EXPIRED, REJECTED
  validFrom      DateTime?
  validTo        DateTime?
  qrCodeUrl      String?
  createdAt      DateTime @default(now())
  
  user           User     @relation(fields: [userId], references: [id])
  passType       PassType @relation(fields: [passTypeId], references: [id])
  documents      PassDocument[]
  history        PassHistory[]
}

model PassDocument {
  id             String   @id @default(uuid())
  passId         String
  documentType   String   // ID_PROOF, PHOTO, CERTIFICATE
  documentUrl    String
  
  pass           Pass     @relation(fields: [passId], references: [id])
}

model PassHistory {
  id             String   @id @default(uuid())
  passId         String
  action         String   // APPLIED, APPROVED, RENEWED
  timestamp      DateTime @default(now())
  
  pass           Pass     @relation(fields: [passId], references: [id])
}

// ==========================================
// TASK 15: Parcel & Cargo Management
// ==========================================

model Parcel {
  id             String   @id @default(uuid())
  pnr            String   @unique
  senderId       String
  receiverName   String
  receiverPhone  String
  weight         Float
  distance       Float
  totalFare      Float
  status         String   // BOOKED, DISPATCHED, IN_TRANSIT, ARRIVED, DELIVERED
  tripInstanceId String?
  createdAt      DateTime @default(now())
  updatedAt      DateTime @updatedAt
  
  sender         User     @relation(fields: [senderId], references: [id])
  trip           TripInstance? @relation(fields: [tripInstanceId], references: [id])
  tracking       ParcelTracking[]
  payments       ParcelPayment[]
}

model ParcelTracking {
  id             String   @id @default(uuid())
  parcelId       String
  status         String
  location       String
  timestamp      DateTime @default(now())
  
  parcel         Parcel   @relation(fields: [parcelId], references: [id])
}

model ParcelPayment {
  id             String   @id @default(uuid())
  parcelId       String
  amount         Float
  status         String   // PENDING, SUCCESS, FAILED
  transactionId  String?
  createdAt      DateTime @default(now())
  
  parcel         Parcel   @relation(fields: [parcelId], references: [id])
}
"""

with open(schema_path, "a") as f:
    f.write(new_models)

print("Backend Phase 3 structure and schema appended successfully.")
