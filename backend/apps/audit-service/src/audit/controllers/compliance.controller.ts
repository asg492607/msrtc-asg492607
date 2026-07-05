import { Controller, Post, Body, Request } from '@nestjs/common';
import { ComplianceService } from '../services/compliance.service';

@Controller('compliance')
export class ComplianceController {
  constructor(private complianceService: ComplianceService) {}

  @Post('data-export')
  async exportData(@Body('targetUserId') targetUserId: string, @Request() req: any) {
    const requestedBy = 'compliance-officer'; // mocked
    return this.complianceService.requestDataExport(targetUserId, requestedBy);
  }

  @Post('data-deletion')
  async deleteData(@Body('targetUserId') targetUserId: string, @Request() req: any) {
    const requestedBy = 'compliance-officer'; // mocked
    return this.complianceService.executeRightToErasure(targetUserId, requestedBy);
  }
}
