import { Controller, Get } from '@nestjs/common';
import { PassengerService } from './passenger.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Passenger')
@Controller()
export class PassengerController {
  constructor(private readonly service: PassengerService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
