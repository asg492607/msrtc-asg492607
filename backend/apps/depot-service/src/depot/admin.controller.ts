import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { InventoryService } from './inventory.service';
import { CreateDepotDto, AddBusDto } from './dto/depot.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Depot Administration (HQ)')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/depots')
export class AdminController {
  constructor(private readonly inventoryService: InventoryService) {}

  @Post()
  @Roles('HQ_Admin')
  @ApiOperation({ summary: 'Register a new MSRTC Depot' })
  async createDepot(@Body() dto: CreateDepotDto) {
    return this.inventoryService.createDepot(dto);
  }

  @Post('inventory')
  @Roles('HQ_Admin')
  @ApiOperation({ summary: 'Add a new bus to a specific depot inventory' })
  async addBus(@Body() dto: AddBusDto) {
    return this.inventoryService.addBusToDepot(dto);
  }
}
