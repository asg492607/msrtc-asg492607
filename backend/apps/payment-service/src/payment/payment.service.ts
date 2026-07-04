import { Injectable, BadRequestException } from '@nestjs/common';
import { PaymentRepository } from './repository/payment.repository';
import { RazorpayAdapter } from './razorpay.adapter';
import { CreatePaymentDto, WebhookDto } from './dto/payment.dto';
import { PaymentStatus, PaymentGateway } from './enums/payment.enums';

@Injectable()
export class PaymentService {
  constructor(
    private readonly repository: PaymentRepository,
    private readonly razorpayAdapter: RazorpayAdapter
  ) {}

  async initiatePayment(dto: CreatePaymentDto) {
    let gatewayResponse;
    
    // Gateway Routing
    if (dto.gateway === PaymentGateway.RAZORPAY) {
      gatewayResponse = await this.razorpayAdapter.initiatePayment(dto.amount, dto.currency, dto.bookingId);
    } else {
      throw new BadRequestException('Unsupported gateway');
    }

    // Persist Payment
    const payment = await this.repository.createPaymentTransaction(
      dto.bookingId, 
      dto.amount, 
      dto.gateway, 
      gatewayResponse.id
    );

    return {
      paymentId: payment.id,
      gatewayOrderId: gatewayResponse.id,
      amount: payment.amount,
      status: payment.status
    };
  }

  async processWebhook(dto: WebhookDto, signature: string) {
    // 1. Signature Verification
    const isValid = this.razorpayAdapter.verifySignature(dto.payload, signature, 'MOCK_SECRET');
    if (!isValid) {
      throw new BadRequestException('Invalid webhook signature');
    }

    // 2. Idempotency & State Check (omitted for brevity, but crucial in prod)

    // 3. State Machine Update
    const paymentId = dto.payload.payment.entity.notes.internal_payment_id; // Mock mapping
    const newStatus = dto.event === 'payment.captured' ? PaymentStatus.SUCCESS : PaymentStatus.FAILED;

    const payment = await this.repository.updatePaymentStatus(paymentId, newStatus, dto.payload.payment.entity.id);

    // 4. Kafka Event Publish (Mocked)
    if (newStatus === PaymentStatus.SUCCESS) {
      console.log(`[Kafka] Publishing payment.success for Booking ${payment.bookingId}`);
    }

    return { received: true };
  }
}
