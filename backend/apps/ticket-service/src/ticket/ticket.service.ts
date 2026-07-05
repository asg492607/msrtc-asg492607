import { Injectable, OnModuleInit } from '@nestjs/common';
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
