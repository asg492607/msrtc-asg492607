import { Module } from '@nestjs/common';
import { MaintenanceController } from './maintenance.controller';
import { WorkshopController } from './workshop.controller';
import { InspectionController } from './inspection.controller';
import { AdminController } from './admin.controller';
import { MaintenanceService } from './maintenance.service';
import { WorkshopService } from './workshop.service';
import { InspectionService } from './inspection.service';
import { ScheduleService } from './schedule.service';
import { MaintenanceRepository } from './repository/maintenance.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [
    MaintenanceController, WorkshopController, 
    InspectionController, AdminController
  ],
  providers: [
    MaintenanceService, WorkshopService, 
    InspectionService, ScheduleService, MaintenanceRepository
  ],
})
export class MaintenanceModule {}
