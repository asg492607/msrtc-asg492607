import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\payment-service\src"

# 1. Gateway Abstraction (Razorpay Adapter)
gateway_adapter = """import { Injectable, NotImplementedException } from '@nestjs/common';
import { IPaymentGateway } from '../interfaces/gateway.interface';

@Injectable()
export class RazorpayAdapter implements IPaymentGateway {
  // In a real app, inject Razorpay SDK here

  async initiatePayment(amount: number, currency: string, receiptId: string): Promise<any> {
    // Mock Razorpay Order Creation
    return {
      id: `order_${Date.now()}`,
      amount: amount * 100, // Razorpay expects paise
      currency,
      receipt: receiptId,
      status: 'created'
    };
  }

  verifySignature(payload: any, signature: string, secret: string): boolean {
    // Mock signature verification (Normally uses crypto.createHmac)
    return true; 
  }

  async processRefund(paymentId: string, amount: number): Promise<any> {
    throw new NotImplementedException('Refunds not mocked yet');
  }
}
"""
with open(os.path.join(base_dir, "payment/razorpay.adapter.ts"), "w") as f: f.write(gateway_adapter)


# 2. Payment Repository
payment_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { PaymentStatus } from '../enums/payment.enums';

@Injectable()
export class PaymentRepository {
  constructor(private prisma: PrismaService) {}

  async createPaymentTransaction(bookingId: string, amount: number, gateway: string, transactionId: string) {
    // Interactive Transaction to create payment and its initial log
    return this.prisma.$transaction(async (tx) => {
      const payment = await tx.payment.create({
        data: {
          bookingId,
          amount,
          status: PaymentStatus.CREATED,
          transactionId,
          gateway,
        }
      });

      await tx.paymentLog.create({
        data: {
          paymentId: payment.id,
          status: PaymentStatus.CREATED,
          message: `Payment initiated via ${gateway}`
        }
      });

      return payment;
    });
  }

  async updatePaymentStatus(paymentId: string, status: PaymentStatus, transactionId?: string) {
    return this.prisma.$transaction(async (tx) => {
      const payment = await tx.payment.update({
        where: { id: paymentId },
        data: { status, transactionId }
      });

      await tx.paymentLog.create({
        data: {
          paymentId,
          status,
          message: `Status updated to ${status}`
        }
      });

      return payment;
    });
  }

  async findPaymentById(id: string) {
    return this.prisma.payment.findUnique({ where: { id } });
  }
}
"""
with open(os.path.join(base_dir, "payment/repository/payment.repository.ts"), "w") as f: f.write(payment_repo)


# 3. Payment Service
payment_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "payment/payment.service.ts"), "w") as f: f.write(payment_svc)


# 4. Controllers
payment_ctrl = """import { Controller, Post, Body, UseGuards, Request } from '@nestjs/common';
import { PaymentService } from './payment.service';
import { CreatePaymentDto } from './dto/payment.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Payments')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('payments')
export class PaymentController {
  constructor(private readonly paymentService: PaymentService) {}

  @Post('initiate')
  @ApiOperation({ summary: 'Initiate a new payment transaction with a gateway' })
  async initiatePayment(@Request() req, @Body() dto: CreatePaymentDto) {
    return this.paymentService.initiatePayment(dto);
  }
}
"""
with open(os.path.join(base_dir, "payment/payment.controller.ts"), "w") as f: f.write(payment_ctrl)

webhook_ctrl = """import { Controller, Post, Body, Headers } from '@nestjs/common';
import { PaymentService } from './payment.service';
import { WebhookDto } from './dto/payment.dto';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Webhooks')
@Controller('webhooks')
export class WebhookController {
  constructor(private readonly paymentService: PaymentService) {}

  @Post('razorpay')
  @ApiOperation({ summary: 'Receive callbacks from Razorpay' })
  async handleRazorpayWebhook(
    @Headers('x-razorpay-signature') signature: string,
    @Body() dto: WebhookDto
  ) {
    return this.paymentService.processWebhook(dto, signature);
  }
}
"""
with open(os.path.join(base_dir, "payment/webhook.controller.ts"), "w") as f: f.write(webhook_ctrl)


# 5. Payment Module
payment_mod = """import { Module } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "payment/payment.module.ts"), "w") as f: f.write(payment_mod)


# 6. Main.ts update
main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AllExceptionsFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.useGlobalFilters(new AllExceptionsFilter());
  
  app.setGlobalPrefix('api/v1');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Payment Service')
    .setDescription('Core Gateway Abstraction and Financial API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/payment', app, document);

  await app.listen(3007);
  console.log('Payment Service is running on http://localhost:3007');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w") as f: f.write(main_ts)

app_module = """import { Module } from '@nestjs/common';
import { PaymentModule } from './payment/payment.module';

@Module({
  imports: [PaymentModule],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w") as f: f.write(app_module)


print("Payment Service Phase 2 Scaffolded (Gateway, Repo, Services, Controllers)")
