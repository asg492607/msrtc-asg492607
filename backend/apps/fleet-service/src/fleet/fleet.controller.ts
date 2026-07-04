import { Controller, Get } from '@nestjs/common';
import { FleetService } from './fleet.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Fleet')
@Controller()
export class FleetController {
  constructor(private readonly service: FleetService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
