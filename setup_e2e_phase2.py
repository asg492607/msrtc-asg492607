import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps"

# 1. Booking Service (Consume Payment, Publish Confirmed)
booking_svc = """import { Injectable, OnModuleInit } from '@nestjs/common';
import { EventBusService, ConsumerService, Topics, EventEnvelope } from '@msrtc/kafka';
import { LockService, CacheKeys } from '@msrtc/redis';

@Injectable()
export class BookingService implements OnModuleInit {
  constructor(
    private eventBus: EventBusService,
    private consumer: ConsumerService,
    private lockService: LockService
  ) {}

  onModuleInit() {
    // Consume Payment Events
    this.consumer.handleEvent(Topics.PAYMENT, null as any, async (envelope: EventEnvelope) => {
      const payload = envelope.payload;
      
      if (payload.type === 'payment.success') {
        await this.handlePaymentSuccess(payload.bookingId);
      } else if (payload.type === 'payment.failed') {
        await this.handlePaymentFailure(payload.bookingId);
      }
    });
  }

  async handlePaymentSuccess(bookingId: string) {
    // 1. Update DB to CONFIRMED
    console.log(`Booking ${bookingId} confirmed.`);
    
    // 2. Publish Booking Confirmed Event
    await this.eventBus.publish(Topics.BOOKING, {
      type: 'booking.confirmed',
      bookingId,
      // mock data
      tripId: 'TRIP-123',
      seatNo: '4A',
      passenger: 'John Doe',
      lockToken: 'tok-abc' 
    });

    // 3. Release Redis Seat Lock Explicitly
    const key = CacheKeys.SEAT_LOCK('TRIP-123', '4A');
    await this.lockService.release(key, 'tok-abc');
  }

  async handlePaymentFailure(bookingId: string) {
    // 1. Update DB to CANCELLED
    console.log(`Booking ${bookingId} cancelled due to payment failure.`);
    
    // 2. Release Redis Seat Lock Explicitly
    const key = CacheKeys.SEAT_LOCK('TRIP-123', '4A'); // mock
    await this.lockService.release(key, 'tok-abc');
  }
}
"""
with open(os.path.join(base_dir, "booking-service/src/booking/booking.service.ts"), "w", encoding="utf-8") as f: f.write(booking_svc)


# 2. Ticket Service (Consume Booking Confirmed)
ticket_svc = """import { Injectable, OnModuleInit } from '@nestjs/common';
import { EventBusService, ConsumerService, Topics, EventEnvelope } from '@msrtc/kafka';

@Injectable()
export class TicketService implements OnModuleInit {
  constructor(
    private eventBus: EventBusService,
    private consumer: ConsumerService
  ) {}

  onModuleInit() {
    this.consumer.handleEvent(Topics.BOOKING, null as any, async (envelope: EventEnvelope) => {
      if (envelope.payload.type === 'booking.confirmed') {
        await this.generateTicket(envelope.payload);
      }
    });
  }

  async generateTicket(bookingData: any) {
    console.log(`Generating QR and Ticket for Booking: ${bookingData.bookingId}`);
    
    // Publish Ticket Generated Event
    await this.eventBus.publish(Topics.TICKET, {
      type: 'ticket.generated',
      ticketId: 'TKT-' + bookingData.bookingId,
      passenger: bookingData.passenger,
      // ...
    });
  }
}
"""
with open(os.path.join(base_dir, "ticket-service/src/ticket/ticket.service.ts"), "w", encoding="utf-8") as f: f.write(ticket_svc)

print("E2E Phase 2 Orchestration Scaffolded (Booking Consumer, Ticket Consumer)")
