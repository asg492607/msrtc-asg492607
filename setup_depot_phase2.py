import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\depot-service\src"

# 1. Repository
depot_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { VehicleStatus } from '../enums/depot.enums';

@Injectable()
export class DepotRepository {
  constructor(private prisma: PrismaService) {}

  async createDepot(data: any) {
    return this.prisma.depot.create({ data });
  }

  async addBus(data: any) {
    return this.prisma.vehicleInventory.create({
      data: {
        ...data,
        status: VehicleStatus.AVAILABLE
      }
    });
  }

  async findBusById(id: string) {
    return this.prisma.vehicleInventory.findUnique({ where: { id } });
  }

  async updateBusStatus(id: string, status: VehicleStatus) {
    return this.prisma.vehicleInventory.update({
      where: { id },
      data: { status }
    });
  }

  async logDispatch(busId: string, tripInstanceId: string) {
    return this.prisma.dispatchLog.create({
      data: { busId, tripInstanceId, dispatchedAt: new Date() }
    });
  }
}
"""
with open(os.path.join(base_dir, "depot/repository/depot.repository.ts"), "w", encoding="utf-8") as f: f.write(depot_repo)


# 2. State Machine & Platforms
avail_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
import { VehicleStatus } from './enums/depot.enums';

@Injectable()
export class AvailabilityService {
  private allowedTransitions = {
    [VehicleStatus.AVAILABLE]: [VehicleStatus.CREW_ASSIGNED, VehicleStatus.UNDER_MAINTENANCE],
    [VehicleStatus.CREW_ASSIGNED]: [VehicleStatus.PLATFORM_ASSIGNED, VehicleStatus.AVAILABLE],
    [VehicleStatus.PLATFORM_ASSIGNED]: [VehicleStatus.READY_FOR_DISPATCH, VehicleStatus.AVAILABLE],
    [VehicleStatus.READY_FOR_DISPATCH]: [VehicleStatus.DISPATCHED, VehicleStatus.AVAILABLE],
    [VehicleStatus.DISPATCHED]: [VehicleStatus.RUNNING],
    [VehicleStatus.RUNNING]: [VehicleStatus.ARRIVED],
    [VehicleStatus.ARRIVED]: [VehicleStatus.PARKED],
    [VehicleStatus.PARKED]: [VehicleStatus.AVAILABLE, VehicleStatus.UNDER_MAINTENANCE],
    [VehicleStatus.UNDER_MAINTENANCE]: [VehicleStatus.AVAILABLE],
  };

  validateTransition(currentStatus: VehicleStatus, nextStatus: VehicleStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Bus cannot transition from ${currentStatus} to ${nextStatus}`);
    }
  }
}
"""
with open(os.path.join(base_dir, "depot/availability.service.ts"), "w", encoding="utf-8") as f: f.write(avail_svc)

platform_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
import { DepotRepository } from './repository/depot.repository';
import { AvailabilityService } from './availability.service';
import { AssignPlatformDto } from './dto/depot.dto';
import { VehicleStatus } from './enums/depot.enums';

@Injectable()
export class PlatformService {
  constructor(
    private repository: DepotRepository,
    private availability: AvailabilityService
  ) {}

  async assignToPlatform(dto: AssignPlatformDto) {
    const bus = await this.repository.findBusById(dto.busId);
    if (!bus) throw new BadRequestException('Bus not found');

    this.availability.validateTransition(bus.status as VehicleStatus, VehicleStatus.PLATFORM_ASSIGNED);
    
    // In real app, check if platformNumber is currently OCCUPIED
    
    await this.repository.updateBusStatus(dto.busId, VehicleStatus.PLATFORM_ASSIGNED);
    return { success: true, platformNumber: dto.platformNumber };
  }
}
"""
with open(os.path.join(base_dir, "depot/platform.service.ts"), "w", encoding="utf-8") as f: f.write(platform_svc)


# 3. Dispatch & Inventory
dispatch_svc = """import { Injectable, BadRequestException, NotFoundException } from '@nestjs/common';
import { DepotRepository } from './repository/depot.repository';
import { AvailabilityService } from './availability.service';
import { DispatchBusDto } from './dto/depot.dto';
import { VehicleStatus } from './enums/depot.enums';

@Injectable()
export class DispatchService {
  constructor(
    private repository: DepotRepository,
    private availability: AvailabilityService
  ) {}

  /**
   * Extremely critical cross-domain validation engine
   */
  async dispatchBus(dto: DispatchBusDto) {
    const bus = await this.repository.findBusById(dto.busId);
    if (!bus) throw new NotFoundException('Bus not found');

    // 1. Check if bus is mechanically available and on a platform
    this.availability.validateTransition(bus.status as VehicleStatus, VehicleStatus.DISPATCHED);

    // 2. Validate Crew Check-In (Mocking inter-service call to Crew Service)
    const isCrewCheckedIn = true; 
    if (!isCrewCheckedIn) {
      throw new BadRequestException('Cannot dispatch: Assigned crew has not checked in.');
    }

    // 3. Dispatch
    await this.repository.logDispatch(dto.busId, dto.tripInstanceId);
    await this.repository.updateBusStatus(dto.busId, VehicleStatus.DISPATCHED);
    
    // Fire Kafka Event: bus.dispatched
    return { success: true, message: 'Bus officially dispatched from Depot' };
  }
}
"""
with open(os.path.join(base_dir, "depot/dispatch.service.ts"), "w", encoding="utf-8") as f: f.write(dispatch_svc)

inv_svc = """import { Injectable } from '@nestjs/common';
import { DepotRepository } from './repository/depot.repository';
import { CreateDepotDto, AddBusDto } from './dto/depot.dto';

@Injectable()
export class InventoryService {
  constructor(private repository: DepotRepository) {}

  async createDepot(dto: CreateDepotDto) {
    return this.repository.createDepot(dto);
  }

  async addBusToDepot(dto: AddBusDto) {
    return this.repository.addBus(dto);
  }
}
"""
with open(os.path.join(base_dir, "depot/inventory.service.ts"), "w", encoding="utf-8") as f: f.write(inv_svc)


# 4. Controllers
dispatch_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "depot/dispatch.controller.ts"), "w", encoding="utf-8") as f: f.write(dispatch_ctrl)


admin_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "depot/admin.controller.ts"), "w", encoding="utf-8") as f: f.write(admin_ctrl)


# 5. Modules
depot_mod = """import { Module } from '@nestjs/common';
import { DispatchController } from './dispatch.controller';
import { AdminController } from './admin.controller';
import { DispatchService } from './dispatch.service';
import { PlatformService } from './platform.service';
import { InventoryService } from './inventory.service';
import { AvailabilityService } from './availability.service';
import { DepotRepository } from './repository/depot.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [DispatchController, AdminController],
  providers: [
    DispatchService, PlatformService, InventoryService,
    AvailabilityService, DepotRepository
  ],
})
export class DepotModule {}
"""
with open(os.path.join(base_dir, "depot/depot.module.ts"), "w", encoding="utf-8") as f: f.write(depot_mod)

app_module = """import { Module } from '@nestjs/common';
import { DepotModule } from './depot/depot.module';

@Module({
  imports: [DepotModule],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(app_module)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AllExceptionsFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.useGlobalFilters(new AllExceptionsFilter());
  
  app.setGlobalPrefix('api/v1');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Depot & Dispatch Service')
    .setDescription('Yard management, Bus Inventory, and Dispatch Control')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/depot', app, document);

  await app.listen(3015);
  console.log('Depot Service is running on http://localhost:3015');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Depot Service Phase 2 Scaffolded (Dispatch, Inventory, Controllers)")
