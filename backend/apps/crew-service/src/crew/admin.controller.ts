import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
import { CrewService } from './crew.service';
import { AssignmentService } from './assignment.service';
import { CreateEmployeeDto, AssignCrewDto } from './dto/crew.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Admin / Depot Operations')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/crew')
export class AdminController {
  constructor(
    private readonly crewService: CrewService,
    private readonly assignmentService: AssignmentService
  ) {}

  @Post()
  @Roles('HQ_Admin')
  @ApiOperation({ summary: 'Onboard a new Driver or Conductor' })
  async createEmployee(@Body() dto: CreateEmployeeDto) {
    return this.crewService.createProfile(dto);
  }

  @Post(':id/assign')
  @Roles('Depot_Manager')
  @ApiOperation({ summary: 'Assign a crew member to a specific Trip Instance' })
  async assignTrip(@Param('id') id: string, @Body() dto: AssignCrewDto) {
    return this.assignmentService.assignTrip(id, dto);
  }
}
