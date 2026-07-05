import { Controller, Post, UseGuards, Request } from '@nestjs/common';
import { AttendanceService } from './attendance.service';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Crew Attendance')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('attendance')
export class AttendanceController {
  constructor(private readonly attendanceService: AttendanceService) {}

  @Post('check-in')
  @Roles('Driver', 'Conductor')
  @ApiOperation({ summary: 'Check-in for assigned duty at depot' })
  async checkIn(@Request() req) {
    return this.attendanceService.markCheckIn(req.user.userId);
  }

  @Post('check-out')
  @Roles('Driver', 'Conductor')
  @ApiOperation({ summary: 'Check-out after duty completion' })
  async checkOut(@Request() req) {
    return this.attendanceService.markCheckOut(req.user.userId);
  }
}
