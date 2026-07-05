import { Controller, Post, Body, UseGuards, Request } from '@nestjs/common';
import { MaintenanceService } from './maintenance.service';
import { BreakdownReportDto } from './dto/maintenance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Fleet Reporting')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('maintenance')
export class MaintenanceController {
  constructor(private readonly maintenanceService: MaintenanceService) {}

  @Post('breakdown')
  @Roles('Driver', 'Conductor')
  @ApiOperation({ summary: 'Report a breakdown on the road (locks vehicle)' })
  async reportBreakdown(@Request() req, @Body() dto: BreakdownReportDto) {
    return this.maintenanceService.reportBreakdown(dto, req.user.userId);
  }
}
