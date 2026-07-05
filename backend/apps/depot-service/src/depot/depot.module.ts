import { Module } from '@nestjs/common';
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
