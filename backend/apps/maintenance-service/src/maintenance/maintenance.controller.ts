import { Controller, Get } from '@nestjs/common';
import { MaintenanceService } from './maintenance.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Maintenance')
@Controller()
export class MaintenanceController {
  constructor(private readonly service: MaintenanceService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
