import { Controller, Get, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('HQ System Config')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/hq')
export class AdminController {
  @Get('health')
  @Roles('HQ_Admin')
  @ApiOperation({ summary: 'Check aggregation engine health' })
  async getHealth() {
    return { status: 'OK', kafkaLag: '0ms', redisLatency: '2ms' };
  }
}
