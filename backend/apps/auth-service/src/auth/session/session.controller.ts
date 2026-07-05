import { Controller, Get, Delete, Param, UseGuards, Request } from '@nestjs/common';
import { SessionService } from './session.service';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('IAM Sessions')
@Controller('iam/sessions')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class SessionController {
  constructor(private sessionService: SessionService) {}

  @Get()
  @ApiOperation({ summary: 'Get active sessions for user' })
  async getSessions(@Request() req) {
    return this.sessionService.getActiveSessions(req.user.userId);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Revoke a specific session' })
  async revokeSession(@Param('id') id: string) {
    await this.sessionService.revokeSession(id);
    return { success: true };
  }
}
