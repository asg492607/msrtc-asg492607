import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
import { WorkshopService } from './workshop.service';
import { CompleteMaintenanceDto } from './dto/maintenance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Workshop Operations')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('workshop/jobs')
export class WorkshopController {
  constructor(private readonly workshopService: WorkshopService) {}

  @Post(':id/start')
  @Roles('Mechanic', 'Foreman')
  @ApiOperation({ summary: 'Start a maintenance job (Notifies Depot to lock bus)' })
  async start(@Param('id') id: string) {
    return this.workshopService.startJob(id);
  }

  @Post(':id/complete')
  @Roles('Foreman')
  @ApiOperation({ summary: 'Complete a job (Notifies Depot to unlock bus)' })
  async complete(@Param('id') id: string, @Body() dto: CompleteMaintenanceDto) {
    return this.workshopService.completeJob(id, dto);
  }
}
