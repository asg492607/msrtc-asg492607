import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\crew-service\src"

# 1. Repository
crew_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { CrewStatus } from '../enums/crew.enums';

@Injectable()
export class CrewRepository {
  constructor(private prisma: PrismaService) {}

  async createEmployee(data: any) {
    const employeeId = `EMP-${Math.floor(Date.now() / 1000)}`;
    return this.prisma.crew.create({
      data: {
        ...data,
        employeeId,
        status: CrewStatus.AVAILABLE,
      }
    });
  }

  async findById(id: string) {
    return this.prisma.crew.findUnique({ where: { id } });
  }

  async updateStatus(id: string, status: CrewStatus) {
    return this.prisma.crew.update({
      where: { id },
      data: { status }
    });
  }

  async saveAssignment(crewId: string, tripInstanceId: string) {
    return this.prisma.crewAssignment.create({
      data: { crewId, tripInstanceId, assignedAt: new Date() }
    });
  }
}
"""
with open(os.path.join(base_dir, "crew/repository/crew.repository.ts"), "w", encoding="utf-8") as f: f.write(crew_repo)


# 2. Compliance & Availability
compliance_svc = """import { Injectable, BadRequestException } from '@nestjs/common';

@Injectable()
export class ComplianceService {
  /**
   * Verify if the crew member has had mandatory 8 hours of rest
   * and their license/medical certificates are valid.
   */
  async checkAssignmentCompliance(crewRecord: any) {
    if (new Date(crewRecord.licenseExpiry) < new Date()) {
      throw new BadRequestException('License is expired. Cannot assign duty.');
    }
    
    // In real app, check last checked_out time for 8hr rest gap
    const hasAdequateRest = true; 
    if (!hasAdequateRest) {
      throw new BadRequestException('Mandatory rest period not fulfilled.');
    }

    return true;
  }
}
"""
with open(os.path.join(base_dir, "crew/compliance.service.ts"), "w", encoding="utf-8") as f: f.write(compliance_svc)

avail_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
import { CrewStatus } from './enums/crew.enums';

@Injectable()
export class AvailabilityService {
  private allowedTransitions = {
    [CrewStatus.AVAILABLE]: [CrewStatus.ASSIGNED, CrewStatus.ON_LEAVE, CrewStatus.MEDICAL_HOLD],
    [CrewStatus.ASSIGNED]: [CrewStatus.CHECKED_IN, CrewStatus.AVAILABLE], // Can un-assign
    [CrewStatus.CHECKED_IN]: [CrewStatus.ON_DUTY],
    [CrewStatus.ON_DUTY]: [CrewStatus.CHECKED_OUT],
    [CrewStatus.CHECKED_OUT]: [CrewStatus.AVAILABLE],
    [CrewStatus.ON_LEAVE]: [CrewStatus.AVAILABLE],
    [CrewStatus.MEDICAL_HOLD]: [CrewStatus.AVAILABLE],
  };

  validateTransition(currentStatus: CrewStatus, nextStatus: CrewStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Invalid state transition from ${currentStatus} to ${nextStatus}`);
    }
  }
}
"""
with open(os.path.join(base_dir, "crew/availability.service.ts"), "w", encoding="utf-8") as f: f.write(avail_svc)


# 3. Core Operational Services
assignment_svc = """import { Injectable, NotFoundException } from '@nestjs/common';
import { CrewRepository } from './repository/crew.repository';
import { ComplianceService } from './compliance.service';
import { AvailabilityService } from './availability.service';
import { AssignCrewDto } from './dto/crew.dto';
import { CrewStatus } from './enums/crew.enums';

@Injectable()
export class AssignmentService {
  constructor(
    private repository: CrewRepository,
    private compliance: ComplianceService,
    private availability: AvailabilityService
  ) {}

  async assignTrip(crewId: string, dto: AssignCrewDto) {
    const crew = await this.repository.findById(crewId);
    if (!crew) throw new NotFoundException('Crew member not found');

    // 1. Check state machine
    this.availability.validateTransition(crew.status as CrewStatus, CrewStatus.ASSIGNED);

    // 2. Run compliance checks (License, Rest period)
    await this.compliance.checkAssignmentCompliance(crew);

    // 3. Save Assignment
    await this.repository.saveAssignment(crewId, dto.tripInstanceId);
    
    // 4. Update status
    await this.repository.updateStatus(crewId, CrewStatus.ASSIGNED);

    return { success: true, message: 'Crew assigned to trip successfully' };
  }
}
"""
with open(os.path.join(base_dir, "crew/assignment.service.ts"), "w", encoding="utf-8") as f: f.write(assignment_svc)


attendance_svc = """import { Injectable, NotFoundException } from '@nestjs/common';
import { CrewRepository } from './repository/crew.repository';
import { AvailabilityService } from './availability.service';
import { CrewStatus } from './enums/crew.enums';

@Injectable()
export class AttendanceService {
  constructor(
    private repository: CrewRepository,
    private availability: AvailabilityService
  ) {}

  async markCheckIn(crewId: string) {
    const crew = await this.repository.findById(crewId);
    if (!crew) throw new NotFoundException();

    this.availability.validateTransition(crew.status as CrewStatus, CrewStatus.CHECKED_IN);
    await this.repository.updateStatus(crewId, CrewStatus.CHECKED_IN);
    // Fire Kafka event: crew.checked_in (so Depot Dispatch knows they are ready)
    return { success: true, status: CrewStatus.CHECKED_IN };
  }

  async markCheckOut(crewId: string) {
    const crew = await this.repository.findById(crewId);
    if (!crew) throw new NotFoundException();

    this.availability.validateTransition(crew.status as CrewStatus, CrewStatus.CHECKED_OUT);
    await this.repository.updateStatus(crewId, CrewStatus.CHECKED_OUT);
    // Automatic transition back to available after checkout logic
    await this.repository.updateStatus(crewId, CrewStatus.AVAILABLE);
    return { success: true, status: CrewStatus.AVAILABLE };
  }
}
"""
with open(os.path.join(base_dir, "crew/attendance.service.ts"), "w", encoding="utf-8") as f: f.write(attendance_svc)


crew_svc = """import { Injectable, NotFoundException } from '@nestjs/common';
import { CrewRepository } from './repository/crew.repository';
import { CreateEmployeeDto } from './dto/crew.dto';

@Injectable()
export class CrewService {
  constructor(private repository: CrewRepository) {}

  async createProfile(dto: CreateEmployeeDto) {
    return this.repository.createEmployee(dto);
  }

  async getProfile(id: string) {
    const profile = await this.repository.findById(id);
    if (!profile) throw new NotFoundException('Crew not found');
    return profile;
  }
}
"""
with open(os.path.join(base_dir, "crew/crew.service.ts"), "w", encoding="utf-8") as f: f.write(crew_svc)


# 4. Controllers
crew_ctrl = """import { Controller, Get, Param, UseGuards, Request } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "crew/crew.controller.ts"), "w", encoding="utf-8") as f: f.write(crew_ctrl)


admin_ctrl = """import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "crew/admin.controller.ts"), "w", encoding="utf-8") as f: f.write(admin_ctrl)


att_ctrl = """import { Controller, Post, UseGuards, Request } from '@nestjs/common';
import { AttendanceService } from './attendance.service';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Crew Attendance')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('attendance')
export class AttendanceController {
  constructor(private readonly attendanceService: AttendanceService) {}

  @Post('check-in')
  @Roles('Driver', 'Conductor')
  @ApiOperation({ summary: 'Check-in for assigned duty at depot' })
  async checkIn(@Request() req) {
    return this.attendanceService.markCheckIn(req.user.userId);
  }

  @Post('check-out')
  @Roles('Driver', 'Conductor')
  @ApiOperation({ summary: 'Check-out after duty completion' })
  async checkOut(@Request() req) {
    return this.attendanceService.markCheckOut(req.user.userId);
  }
}
"""
with open(os.path.join(base_dir, "crew/attendance.controller.ts"), "w", encoding="utf-8") as f: f.write(att_ctrl)


# 5. Modules
crew_mod = """import { Module } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "crew/crew.module.ts"), "w", encoding="utf-8") as f: f.write(crew_mod)

app_module = """import { Module } from '@nestjs/common';
import { CrewModule } from './crew/crew.module';

@Module({
  imports: [CrewModule],
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
    .setTitle('MSRTC Crew Operations Service')
    .setDescription('Driver/Conductor rosters, assignments, and compliance')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/crew', app, document);

  await app.listen(3014);
  console.log('Crew Service is running on http://localhost:3014');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Crew Service Phase 2 Scaffolded (Compliance, Assignment, Attendance, Controllers)")
