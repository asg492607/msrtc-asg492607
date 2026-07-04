import { Controller, Get } from '@nestjs/common';
import { BookingService } from './booking.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Booking')
@Controller()
export class BookingController {
  constructor(private readonly service: BookingService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
