import { Module } from '@nestjs/common';
import { CrewController } from './crew.controller';
import { AdminController } from './admin.controller';
import { AttendanceController } from './attendance.controller';
import { CrewService } from './crew.service';
import { AssignmentService } from './assignment.service';
import { AttendanceService } from './attendance.service';
import { ComplianceService } from './compliance.service';
import { AvailabilityService } from './availability.service';
import { CrewRepository } from './repository/crew.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [CrewController, AdminController, AttendanceController],
  providers: [
    CrewService, AssignmentService, AttendanceService,
    ComplianceService, AvailabilityService, CrewRepository
  ],
})
export class CrewModule {}
