import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { DispatchService } from './dispatch.service';
import { PlatformService } from './platform.service';
import { DispatchBusDto, AssignPlatformDto } from './dto/depot.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Yard & Dispatch Operations')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('dispatch')
export class DispatchController {
  constructor(
    private readonly dispatchService: DispatchService,
    private readonly platformService: PlatformService
  ) {}

  @Post('platform')
  @Roles('Dispatcher', 'Depot_Manager')
  @ApiOperation({ summary: 'Assign a bus from the yard to a departure platform' })
  async assignPlatform(@Body() dto: AssignPlatformDto) {
    return this.platformService.assignToPlatform(dto);
  }

  @Post('release')
  @Roles('Dispatcher', 'Depot_Manager')
  @ApiOperation({ summary: 'Officially dispatch a bus from the depot onto a route' })
  async dispatchBus(@Body() dto: DispatchBusDto) {
    return this.dispatchService.dispatchBus(dto);
  }
}
