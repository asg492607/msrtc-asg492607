import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
import { InspectionService } from './inspection.service';
import { InspectionDto } from './dto/maintenance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Quality & Inspection')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('inspections')
export class InspectionController {
  constructor(private readonly inspectionService: InspectionService) {}

  @Post('job/:jobId')
  @Roles('Foreman', 'Inspector')
  @ApiOperation({ summary: 'Log a Quality Check for an in-progress job' })
  async performInspection(@Param('jobId') jobId: string, @Body() dto: InspectionDto) {
    return this.inspectionService.performInspection(jobId, dto);
  }
}
