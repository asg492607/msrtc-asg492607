import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps"

services = ['booking-service', 'seat-service', 'payment-service', 'ticket-service']

# 1. Update Package.json for dependencies
for svc in services:
    pkg_path = os.path.join(base_dir, svc, "package.json")
    if os.path.exists(pkg_path):
        with open(pkg_path, "r") as f:
            pkg = json.load(f)
        
        # Add workspace packages
        pkg['dependencies']['@msrtc/kafka'] = "workspace:*"
        pkg['dependencies']['@msrtc/redis'] = "workspace:*"
        
        with open(pkg_path, "w") as f:
            json.dump(pkg, f, indent=2)

# 2. Seat Service (Locking)
seat_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
import { LockService, CacheKeys } from '@msrtc/redis';

@Injectable()
export class SeatService {
  constructor(private lockService: LockService) {}

  async lockSeat(tripId: string, seatNo: string) {
    const key = CacheKeys.SEAT_LOCK(tripId, seatNo);
    // 10 minutes TTL
    const lockToken = await this.lockService.acquire(key, 600);
    
    if (!lockToken) {
      throw new BadRequestException(`Seat ${seatNo} on trip ${tripId} is currently locked or booked.`);
    }

    return { success: true, lockToken, expiresId: 600 };
  }

  async releaseSeat(tripId: string, seatNo: string, lockToken: string) {
    const key = CacheKeys.SEAT_LOCK(tripId, seatNo);
    const success = await this.lockService.release(key, lockToken);
    
    if (!success) {
      // Could be expired or invalid token
      return { success: false, message: 'Invalid lock token or lock expired' };
    }
    return { success: true };
  }
}
"""
with open(os.path.join(base_dir, "seat-service/src/seat/seat.service.ts"), "w", encoding="utf-8") as f: f.write(seat_svc)


# 3. Payment Service (Publishing)
payment_svc = """import { Injectable } from '@nestjs/common';
import { EventBusService, Topics } from '@msrtc/kafka';

@Injectable()
export class PaymentService {
  constructor(private eventBus: EventBusService) {}

  async processWebhook(paymentId: string, status: string, bookingId: string) {
    // DB Update logic would go here
    
    if (status === 'SUCCESS') {
      await this.eventBus.publish(Topics.PAYMENT, {
        type: 'payment.success',
        paymentId,
        bookingId,
      });
      return { status: 'CONFIRMED' };
    } else {
      await this.eventBus.publish(Topics.PAYMENT, {
        type: 'payment.failed',
        paymentId,
        bookingId,
      });
      return { status: 'FAILED' };
    }
  }
}
"""
with open(os.path.join(base_dir, "payment-service/src/payment/payment.service.ts"), "w", encoding="utf-8") as f: f.write(payment_svc)


print("E2E Phase 1 Orchestration Scaffolded (Package.json, Seat Lock, Payment Publish)")
