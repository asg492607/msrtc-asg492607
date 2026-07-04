import { Module } from '@nestjs/common';
import { PaymentController } from './payment.controller';
import { WebhookController } from './webhook.controller';
import { PaymentService } from './payment.service';
import { PaymentRepository } from './repository/payment.repository';
import { RazorpayAdapter } from './razorpay.adapter';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [PaymentController, WebhookController],
  providers: [PaymentService, PaymentRepository, RazorpayAdapter],
})
export class PaymentModule {}
