import { Controller, Post, Param, Body, UseGuards, Request } from '@nestjs/common';
import { ComplaintService } from './complaint.service';
import { EscalationService } from './escalation.service';
import { ComplaintCommentDto } from './dto/complaint.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Admin Complaint Management')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/complaints')
export class AdminController {
  constructor(
    private readonly complaintService: ComplaintService,
    private readonly escalationService: EscalationService
  ) {}

  @Post(':id/resolve')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Mark a complaint as resolved (Staff only)' })
  async resolve(@Param('id') id: string) {
    return this.complaintService.resolveComplaint(id);
  }

  @Post(':id/escalate')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Manually escalate a complaint (Staff only)' })
  async escalate(@Param('id') id: string) {
    return this.escalationService.escalateComplaint(id);
  }

  @Post(':id/comment')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Add an internal staff comment' })
  async addInternalComment(@Request() req, @Param('id') id: string, @Body() dto: ComplaintCommentDto) {
    return this.complaintService.addComment(id, req.user.userId, dto);
  }
}
