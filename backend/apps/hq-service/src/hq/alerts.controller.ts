import { Controller, Get, UseGuards } from '@nestjs/common';
import { AlertService } from './alert.service';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Operational Alerts')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('alerts')
export class AlertsController {
  constructor(private readonly alertService: AlertService) {}

  @Get()
  @Roles('Executive', 'HQ_Admin')
  @ApiOperation({ summary: 'Get recent operational anomalies' })
  async getAlerts() {
    return { alerts: [] }; // Mock
  }
}
