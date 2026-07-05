import { Injectable } from '@nestjs/common';
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
