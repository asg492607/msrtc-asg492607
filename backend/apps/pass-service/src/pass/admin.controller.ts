import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
import { PassService } from './pass.service';
import { RejectPassDto } from './dto/pass.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Admin Pass Review')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/passes')
export class AdminController {
  constructor(private readonly passService: PassService) {}

  @Post(':id/approve')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Approve a submitted pass application' })
  async approve(@Param('id') id: string) {
    return this.passService.approvePass(id);
  }

  @Post(':id/reject')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Reject a pass application with reason' })
  async reject(@Param('id') id: string, @Body() dto: RejectPassDto) {
    return this.passService.rejectPass(id, dto);
  }
}
