import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend"

directories = [
    "apps/booking-service",
    "apps/seat-service",
    "apps/payment-service",
    "apps/ticket-service",
    "apps/passenger-service"
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

schema_path = os.path.join(base_dir, "packages", "database", "prisma", "schema.prisma")

new_models = """

// ==========================================
// TASK 6: Booking Service
// ==========================================

model Booking {
  id              String   @id @default(uuid())
  pnr             String   @unique
  userId          String
  tripInstanceId  String
  status          String   // PENDING, SEAT_LOCKED, PAYMENT_PENDING, CONFIRMED, CANCELLED, REFUNDED
  totalFare       Float
  discount        Float    @default(0.0)
  netAmount       Float
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  user            User           @relation(fields: [userId], references: [id])
  trip            TripInstance   @relation(fields: [tripInstanceId], references: [id])
  
  passengers      BookingPassenger[]
  payments        PaymentTransaction[]
  refunds         BookingRefund[]
  logs            BookingLog[]
  ticket          Ticket?
}

model BookingPassenger {
  id        String   @id @default(uuid())
  bookingId String
  name      String
  age       Int
  gender    String
  seatNo    String
  status    String   // CONFIRMED, CANCELLED
  fare      Float
  
  booking   Booking  @relation(fields: [bookingId], references: [id])
}

model BookingLog {
  id        String   @id @default(uuid())
  bookingId String
  action    String   // e.g. "SEAT_LOCKED", "PAYMENT_SUCCESS"
  timestamp DateTime @default(now())
  
  booking   Booking  @relation(fields: [bookingId], references: [id])
}

model BookingRefund {
  id            String   @id @default(uuid())
  bookingId     String
  refundAmount  Float
  status        String   // INITIATED, SUCCESS, FAILED
  processedAt   DateTime?
  
  booking       Booking  @relation(fields: [bookingId], references: [id])
}

// ==========================================
// TASK 7: Seat Inventory & Locking
// ==========================================
// Note: Real-time locking (5-min window) is handled in Redis.
// This table stores the final confirmed state.

model SeatStatus {
  id             String   @id @default(uuid())
  tripInstanceId String
  seatNo         String
  status         String   // BOOKED, LADIES, SENIOR, MAINTENANCE
  bookingId      String?
  updatedAt      DateTime @updatedAt
  
  trip           TripInstance @relation(fields: [tripInstanceId], references: [id])
  @@unique([tripInstanceId, seatNo])
}

// ==========================================
// TASK 8: Payment Service
// ==========================================

model PaymentTransaction {
  id             String   @id @default(uuid())
  bookingId      String
  gateway        String   // RAZORPAY, PAYU
  gatewayTxnId   String?  @unique
  amount         Float
  currency       String   @default("INR")
  status         String   // INITIATED, PENDING, SUCCESS, FAILED
  paymentMethod  String?  // UPI, CARD, NETBANKING
  createdAt      DateTime @default(now())
  updatedAt      DateTime @updatedAt
  
  booking        Booking  @relation(fields: [bookingId], references: [id])
}

model PromoCode {
  id            String   @id @default(uuid())
  code          String   @unique
  discountPct   Float
  maxDiscount   Float
  validUntil    DateTime
  isActive      Boolean  @default(true)
}

// ==========================================
// TASK 9: Ticket & Document Service
// ==========================================

model Ticket {
  id         String   @id @default(uuid())
  bookingId  String   @unique
  qrCodeUrl  String?
  pdfUrl     String?
  issuedAt   DateTime @default(now())
  
  booking    Booking  @relation(fields: [bookingId], references: [id])
}

// ==========================================
// TASK 10: Passenger Service (Profiles)
// ==========================================

model SavedPassenger {
  id        String   @id @default(uuid())
  userId    String
  name      String
  age       Int
  gender    String
  relation  String?
  
  user      User     @relation(fields: [userId], references: [id])
}

model EmergencyContact {
  id        String   @id @default(uuid())
  userId    String
  name      String
  phone     String
  relation  String
  
  user      User     @relation(fields: [userId], references: [id])
}

model FavouriteRoute {
  id           String   @id @default(uuid())
  userId       String
  origin       String
  destination  String
  
  user         User     @relation(fields: [userId], references: [id])
}

model UserPreference {
  id           String   @id @default(uuid())
  userId       String   @unique
  language     String   @default("en")
  theme        String   @default("light")
  emailAlerts  Boolean  @default(true)
  smsAlerts    Boolean  @default(true)
  
  user         User     @relation(fields: [userId], references: [id])
}
"""

with open(schema_path, "a") as f:
    f.write(new_models)

print("Backend Phase 2 structure and schema appended successfully.")
