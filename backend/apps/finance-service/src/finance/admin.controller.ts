import { Controller, Get, UseGuards } from '@nestjs/common';
import { GstService } from './gst.service';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Financial Reporting')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/finance')
export class AdminController {
  constructor(private readonly gstService: GstService) {}

  @Get('gst-report')
  @Roles('HQ_Admin', 'Auditor')
  @ApiOperation({ summary: 'Generate monthly GST liability report' })
  async getGstReport() {
    return this.gstService.generateMonthlyReport();
  }
}
