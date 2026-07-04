import { Controller, Get } from '@nestjs/common';
import { SeatService } from './seat.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Seat')
@Controller()
export class SeatController {
  constructor(private readonly service: SeatService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
