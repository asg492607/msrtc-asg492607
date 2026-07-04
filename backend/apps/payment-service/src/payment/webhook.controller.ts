import { Controller, Post, Body, Headers } from '@nestjs/common';
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
