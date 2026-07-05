import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { ReportConfigDto } from './dto/hq.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Report Generation')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('reports')
export class ReportsController {
  @Post('generate')
  @Roles('Executive', 'HQ_Admin', 'Regional_Admin')
  @ApiOperation({ summary: 'Generate a PDF/CSV historical report' })
  async generateReport(@Body() dto: ReportConfigDto) {
    return { success: true, message: `Report ${dto.reportName} generation started in background.` };
  }
}
