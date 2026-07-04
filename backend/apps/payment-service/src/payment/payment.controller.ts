import { Controller, Get } from '@nestjs/common';
import { PaymentService } from './payment.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Payment')
@Controller()
export class PaymentController {
  constructor(private readonly service: PaymentService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
