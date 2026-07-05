import { Controller, Get, Param, UseGuards, Request } from '@nestjs/common';
import { CrewService } from './crew.service';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Crew Profile (Self)')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('crew')
export class CrewController {
  constructor(private readonly crewService: CrewService) {}

  @Get('me')
  @ApiOperation({ summary: 'Get own profile details' })
  async getMyProfile(@Request() req) {
    return this.crewService.getProfile(req.user.userId);
  }
}
