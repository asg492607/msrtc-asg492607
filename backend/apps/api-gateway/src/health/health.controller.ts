import { Controller, Get } from '@nestjs/common';
import { HealthService } from './health.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('System Diagnostics')
@Controller('system/health')
export class HealthController {
  constructor(private readonly healthService: HealthService) {}

  @Get()
  @ApiOperation({ summary: 'Aggregate health checks across all microservices' })
  async getSystemHealth() {
    return this.healthService.aggregateHealth();
  }
}
