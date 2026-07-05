import { Controller, Post, Get, Param, Body, Request } from '@nestjs/common';
import { ReportService } from '../services/report.service';

@Controller('reports')
export class ReportController {
  constructor(private reportService: ReportService) {}

  @Post('generate')
  async requestReport(@Body() body: { type: string, parameters: any }, @Request() req: any) {
    const userId = 'sys-admin'; // mock req.user.userId
    return this.reportService.queueReport(body.type, userId, body.parameters);
  }

  @Get(':id')
  async getReportStatus(@Param('id') id: string) {
    return this.reportService.getJobStatus(id);
  }
}
