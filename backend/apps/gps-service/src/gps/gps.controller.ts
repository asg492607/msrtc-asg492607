import { Controller, Get } from '@nestjs/common';
import { GpsService } from './gps.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Gps')
@Controller()
export class GpsController {
  constructor(private readonly service: GpsService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
