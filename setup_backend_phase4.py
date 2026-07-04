import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend"

directories = [
    "apps/crew-service",
    "apps/depot-service",
    "apps/maintenance-service",
    "apps/finance-service",
    "apps/hq-service"
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

schema_path = os.path.join(base_dir, "packages", "database", "prisma", "schema.prisma")

new_models = """

// ==========================================
// TASK 16: Driver & Crew Management
// ==========================================

model Employee {
  id             String   @id @default(uuid())
  userId         String   @unique
  employeeCode   String   @unique
  designation    String   // DRIVER, CONDUCTOR, INSPECTOR, MECHANIC
  depotId        String?
  status         String   // ACTIVE, ON_LEAVE, SUSPENDED
  joiningDate    DateTime
  createdAt      DateTime @default(now())
  
  user           User     @relation(fields: [userId], references: [id])
  depot          Depot?   @relation(fields: [depotId], references: [id])
  
  driverLicense  DriverLicense?
  attendance     Attendance[]
  leaveRequests  LeaveRequest[]
  dutyRosters    DutyRoster[]
}

model DriverLicense {
  id             String   @id @default(uuid())
  employeeId     String   @unique
  licenseNumber  String   @unique
  vehicleClasses String   // HMV, LMV
  expiryDate     DateTime
  issuedState    String
  
  employee       Employee @relation(fields: [employeeId], references: [id])
}

model DutyRoster {
  id             String   @id @default(uuid())
  employeeId     String
  tripInstanceId String
  dutyDate       DateTime
  status         String   // ASSIGNED, COMPLETED, CANCELLED
  
  employee       Employee @relation(fields: [employeeId], references: [id])
  trip           TripInstance @relation(fields: [tripInstanceId], references: [id])
}

model Attendance {
  id             String   @id @default(uuid())
  employeeId     String
  date           DateTime
  checkInTime    DateTime?
  checkOutTime   DateTime?
  status         String   // PRESENT, ABSENT, HALF_DAY
  
  employee       Employee @relation(fields: [employeeId], references: [id])
}

model LeaveRequest {
  id             String   @id @default(uuid())
  employeeId     String
  leaveType      String   // SICK, CASUAL, EARNED
  startDate      DateTime
  endDate        DateTime
  status         String   // PENDING, APPROVED, REJECTED
  reason         String?
  
  employee       Employee @relation(fields: [employeeId], references: [id])
}

// ==========================================
// TASK 17: Depot Operations
// ==========================================

model Platform {
  id             String   @id @default(uuid())
  depotId        String
  platformNumber String
  status         String   // AVAILABLE, OCCUPIED, MAINTENANCE
  
  depot          Depot    @relation(fields: [depotId], references: [id])
}

model DispatchLog {
  id             String   @id @default(uuid())
  tripInstanceId String   @unique
  depotId        String
  dispatchedAt   DateTime @default(now())
  platformId     String?
  authorizedBy   String   // User ID of depot manager
  
  trip           TripInstance @relation(fields: [tripInstanceId], references: [id])
  depot          Depot    @relation(fields: [depotId], references: [id])
}

model ArrivalLog {
  id             String   @id @default(uuid())
  tripInstanceId String   @unique
  depotId        String
  arrivedAt      DateTime @default(now())
  platformId     String?
  
  trip           TripInstance @relation(fields: [tripInstanceId], references: [id])
  depot          Depot    @relation(fields: [depotId], references: [id])
}

model DailyOperation {
  id             String   @id @default(uuid())
  depotId        String
  date           DateTime
  totalDispatches Int     @default(0)
  totalArrivals   Int     @default(0)
  counterRevenue  Float   @default(0.0)
  status         String   // OPEN, CLOSED
  
  depot          Depot    @relation(fields: [depotId], references: [id])
  @@unique([depotId, date])
}

// ==========================================
// TASK 18: Fleet Maintenance & Workshop
// ==========================================

model Maintenance {
  id             String   @id @default(uuid())
  busId          String
  type           String   // PREVENTIVE, BREAKDOWN
  status         String   // SCHEDULED, IN_PROGRESS, COMPLETED
  scheduledDate  DateTime
  completedDate  DateTime?
  description    String?
  
  bus            Bus      @relation(fields: [busId], references: [id])
  jobCards       JobCard[]
}

model JobCard {
  id             String   @id @default(uuid())
  maintenanceId  String
  mechanicId     String   // Employee ID
  task           String
  status         String   // PENDING, COMPLETED
  partsCost      Float    @default(0.0)
  laborCost      Float    @default(0.0)
  
  maintenance    Maintenance @relation(fields: [maintenanceId], references: [id])
}

model Breakdown {
  id             String   @id @default(uuid())
  busId          String
  tripInstanceId String?
  location       String
  reportedAt     DateTime @default(now())
  resolvedAt     DateTime?
  status         String   // REPORTED, ATTENDING, RESOLVED
  description    String
  
  bus            Bus      @relation(fields: [busId], references: [id])
  trip           TripInstance? @relation(fields: [tripInstanceId], references: [id])
}

model Inventory {
  id             String   @id @default(uuid())
  partName       String   @unique
  partNumber     String   @unique
  category       String
  quantity       Int      @default(0)
  unitPrice      Float
  reorderLevel   Int
  depotId        String
  
  depot          Depot    @relation(fields: [depotId], references: [id])
}

// ==========================================
// TASK 19: Revenue, Finance & Accounting
// ==========================================

model Revenue {
  id             String   @id @default(uuid())
  source         String   // BOOKING, PARCEL, PASS, COUNTER
  amount         Float
  referenceId    String   // e.g. Booking ID
  date           DateTime @default(now())
  depotId        String?
  
  depot          Depot?   @relation(fields: [depotId], references: [id])
}

model Expense {
  id             String   @id @default(uuid())
  category       String   // FUEL, MAINTENANCE, SALARY
  amount         Float
  description    String?
  date           DateTime @default(now())
  depotId        String?
  
  depot          Depot?   @relation(fields: [depotId], references: [id])
}

model Ledger {
  id             String   @id @default(uuid())
  accountId      String
  accountName    String
  type           String   // ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
  balance        Float    @default(0.0)
  
  journals       Journal[]
}

model Journal {
  id             String   @id @default(uuid())
  ledgerId       String
  type           String   // DEBIT, CREDIT
  amount         Float
  date           DateTime @default(now())
  referenceId    String?
  
  ledger         Ledger   @relation(fields: [ledgerId], references: [id])
}

// ==========================================
// TASK 20: HQ Command Center & Analytics
// ==========================================

model DashboardCache {
  id             String   @id @default(uuid())
  kpiName        String   @unique
  value          String   // JSON payload of the KPI data
  lastUpdated    DateTime @default(now())
}

model ExecutiveReport {
  id             String   @id @default(uuid())
  reportType     String   // REVENUE, OPERATIONS, MAINTENANCE
  reportDate     DateTime
  s3Url          String?
  generatedAt    DateTime @default(now())
}

model AlertHistory {
  id             String   @id @default(uuid())
  alertType      String   // CRITICAL_DELAY, BREAKDOWN, REVENUE_DROP
  severity       String   // HIGH, MEDIUM, LOW
  message        String
  isAcknowledged Boolean  @default(false)
  timestamp      DateTime @default(now())
}
"""

with open(schema_path, "a") as f:
    f.write(new_models)

print("Backend Phase 4 structure and schema appended successfully.")
