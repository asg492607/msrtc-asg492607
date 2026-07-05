import { Controller, Post, Get, Body, Param, UseGuards, Request } from '@nestjs/common';
import { ComplaintService } from './complaint.service';
import { CreateComplaintDto, ComplaintCommentDto } from './dto/complaint.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Passenger Complaints')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('complaints')
export class ComplaintController {
  constructor(private readonly complaintService: ComplaintService) {}

  @Post()
  @ApiOperation({ summary: 'Register a new grievance' })
  async register(@Request() req, @Body() dto: CreateComplaintDto) {
    return this.complaintService.registerComplaint(req.user.userId, dto);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get details of a specific complaint (Passenger view)' })
  async getDetails(@Request() req, @Param('id') id: string) {
    return this.complaintService.getComplaintForPassenger(id, req.user.userId);
  }

  @Post(':id/comment')
  @ApiOperation({ summary: 'Add a comment to an open complaint' })
  async addComment(@Request() req, @Param('id') id: string, @Body() dto: ComplaintCommentDto) {
    // Force isInternal to false for passenger submissions
    dto.isInternal = false; 
    return this.complaintService.addComment(id, req.user.userId, dto);
  }
}
