import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { MaintenanceService } from './maintenance.service';
import { CreateMaintenanceJobDto } from './dto/maintenance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Maintenance Administration')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/maintenance')
export class AdminController {
  constructor(private readonly maintenanceService: MaintenanceService) {}

  @Post('jobs')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Create a new Scheduled/Preventive Job' })
  async createJob(@Body() dto: CreateMaintenanceJobDto) {
    return this.maintenanceService.createJob(dto);
  }
}
