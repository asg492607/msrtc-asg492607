import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\maintenance-service\src"

# 1. Repository
maint_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { MaintenanceStatus } from '../enums/maintenance.enums';

@Injectable()
export class MaintenanceRepository {
  constructor(private prisma: PrismaService) {}

  async createJob(data: any) {
    const jobNumber = `JOB-${Math.floor(Date.now() / 1000)}`;
    return this.prisma.maintenanceJob.create({
      data: {
        ...data,
        jobNumber,
        status: MaintenanceStatus.SCHEDULED,
      }
    });
  }

  async findById(id: string) {
    return this.prisma.maintenanceJob.findUnique({ where: { id } });
  }

  async updateStatus(id: string, status: MaintenanceStatus) {
    return this.prisma.maintenanceJob.update({
      where: { id },
      data: { status }
    });
  }

  async logInspection(jobId: string, comments: string, passed: boolean) {
    return this.prisma.inspectionLog.create({
      data: { jobId, comments, passed, inspectedAt: new Date() }
    });
  }

  async logBreakdown(data: any) {
    return this.prisma.breakdownReport.create({ data });
  }

  async hasPassedInspection(jobId: string): Promise<boolean> {
    const logs = await this.prisma.inspectionLog.findMany({
      where: { jobId },
      orderBy: { inspectedAt: 'desc' },
      take: 1
    });
    return logs.length > 0 && logs[0].passed;
  }
}
"""
with open(os.path.join(base_dir, "maintenance/repository/maintenance.repository.ts"), "w", encoding="utf-8") as f: f.write(maint_repo)


# 2. State Machine & Inspection
workshop_svc = """import { Injectable, BadRequestException, NotFoundException } from '@nestjs/common';
import { MaintenanceRepository } from './repository/maintenance.repository';
import { CompleteMaintenanceDto } from './dto/maintenance.dto';
import { MaintenanceStatus } from './enums/maintenance.enums';

@Injectable()
export class WorkshopService {
  constructor(private repository: MaintenanceRepository) {}

  private allowedTransitions = {
    [MaintenanceStatus.SCHEDULED]: [MaintenanceStatus.ASSIGNED, MaintenanceStatus.CANCELLED],
    [MaintenanceStatus.ASSIGNED]: [MaintenanceStatus.IN_PROGRESS],
    [MaintenanceStatus.IN_PROGRESS]: [MaintenanceStatus.QUALITY_CHECK],
    [MaintenanceStatus.QUALITY_CHECK]: [MaintenanceStatus.COMPLETED, MaintenanceStatus.IN_PROGRESS],
    [MaintenanceStatus.COMPLETED]: [],
    [MaintenanceStatus.CANCELLED]: [],
  };

  validateTransition(currentStatus: MaintenanceStatus, nextStatus: MaintenanceStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Job cannot transition from ${currentStatus} to ${nextStatus}`);
    }
  }

  async startJob(id: string) {
    const job = await this.repository.findById(id);
    if (!job) throw new NotFoundException('Job not found');

    this.validateTransition(job.status as MaintenanceStatus, MaintenanceStatus.IN_PROGRESS);
    await this.repository.updateStatus(id, MaintenanceStatus.IN_PROGRESS);

    // CRITICAL: Fire Kafka Event -> vehicle.maintenance.started
    // The Depot Service will consume this and flag the bus as UNDER_MAINTENANCE

    return { success: true, message: 'Job started. Bus locked in Depot.' };
  }

  async completeJob(id: string, dto: CompleteMaintenanceDto) {
    const job = await this.repository.findById(id);
    if (!job) throw new NotFoundException('Job not found');

    this.validateTransition(job.status as MaintenanceStatus, MaintenanceStatus.COMPLETED);

    // 1. Enforce Quality Check
    const hasPassed = await this.repository.hasPassedInspection(id);
    if (!hasPassed) {
      throw new BadRequestException('Cannot complete job without a passing Quality Check inspection.');
    }

    // 2. Complete Job
    await this.repository.updateStatus(id, MaintenanceStatus.COMPLETED);
    
    // Fire Kafka Event -> vehicle.available
    // The Depot Service unlocks the bus

    return { success: true, message: 'Job completed. Bus unlocked.' };
  }
}
"""
with open(os.path.join(base_dir, "maintenance/workshop.service.ts"), "w", encoding="utf-8") as f: f.write(workshop_svc)

inspection_svc = """import { Injectable, NotFoundException } from '@nestjs/common';
import { MaintenanceRepository } from './repository/maintenance.repository';
import { WorkshopService } from './workshop.service';
import { InspectionDto } from './dto/maintenance.dto';
import { MaintenanceStatus } from './enums/maintenance.enums';

@Injectable()
export class InspectionService {
  constructor(
    private repository: MaintenanceRepository,
    private workshop: WorkshopService
  ) {}

  async performInspection(jobId: string, dto: InspectionDto) {
    const job = await this.repository.findById(jobId);
    if (!job) throw new NotFoundException();

    this.workshop.validateTransition(job.status as MaintenanceStatus, MaintenanceStatus.QUALITY_CHECK);
    await this.repository.updateStatus(jobId, MaintenanceStatus.QUALITY_CHECK);

    const passed = dto.passed.toUpperCase() === 'YES';
    await this.repository.logInspection(jobId, dto.comments, passed);

    return { success: true, passed };
  }
}
"""
with open(os.path.join(base_dir, "maintenance/inspection.service.ts"), "w", encoding="utf-8") as f: f.write(inspection_svc)


# 3. Breakdown & Schedules
maint_svc = """import { Injectable } from '@nestjs/common';
import { MaintenanceRepository } from './repository/maintenance.repository';
import { CreateMaintenanceJobDto, BreakdownReportDto } from './dto/maintenance.dto';

@Injectable()
export class MaintenanceService {
  constructor(private repository: MaintenanceRepository) {}

  async createJob(dto: CreateMaintenanceJobDto) {
    return this.repository.createJob(dto);
  }

  async reportBreakdown(dto: BreakdownReportDto, reportedById: string) {
    const report = await this.repository.logBreakdown({
      busId: dto.busId,
      locationCoordinates: dto.locationCoordinates,
      issueDescription: dto.issueDescription,
      reportedById
    });

    // Fire Kafka Event -> vehicle.breakdown
    // Depot service locks bus. Notification service alerts Workshop Foreman.

    return report;
  }
}
"""
with open(os.path.join(base_dir, "maintenance/maintenance.service.ts"), "w", encoding="utf-8") as f: f.write(maint_svc)

schedule_svc = """import { Injectable } from '@nestjs/common';

@Injectable()
export class ScheduleService {
  // Logic to auto-create preventive maintenance jobs based on bus mileage
}
"""
with open(os.path.join(base_dir, "maintenance/schedule.service.ts"), "w", encoding="utf-8") as f: f.write(schedule_svc)


# 4. Controllers
maint_ctrl = """import { Controller, Post, Body, UseGuards, Request } from '@nestjs/common';
import { MaintenanceService } from './maintenance.service';
import { BreakdownReportDto } from './dto/maintenance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Fleet Reporting')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('maintenance')
export class MaintenanceController {
  constructor(private readonly maintenanceService: MaintenanceService) {}

  @Post('breakdown')
  @Roles('Driver', 'Conductor')
  @ApiOperation({ summary: 'Report a breakdown on the road (locks vehicle)' })
  async reportBreakdown(@Request() req, @Body() dto: BreakdownReportDto) {
    return this.maintenanceService.reportBreakdown(dto, req.user.userId);
  }
}
"""
with open(os.path.join(base_dir, "maintenance/maintenance.controller.ts"), "w", encoding="utf-8") as f: f.write(maint_ctrl)


workshop_ctrl = """import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
import { WorkshopService } from './workshop.service';
import { CompleteMaintenanceDto } from './dto/maintenance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Workshop Operations')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('workshop/jobs')
export class WorkshopController {
  constructor(private readonly workshopService: WorkshopService) {}

  @Post(':id/start')
  @Roles('Mechanic', 'Foreman')
  @ApiOperation({ summary: 'Start a maintenance job (Notifies Depot to lock bus)' })
  async start(@Param('id') id: string) {
    return this.workshopService.startJob(id);
  }

  @Post(':id/complete')
  @Roles('Foreman')
  @ApiOperation({ summary: 'Complete a job (Notifies Depot to unlock bus)' })
  async complete(@Param('id') id: string, @Body() dto: CompleteMaintenanceDto) {
    return this.workshopService.completeJob(id, dto);
  }
}
"""
with open(os.path.join(base_dir, "maintenance/workshop.controller.ts"), "w", encoding="utf-8") as f: f.write(workshop_ctrl)


insp_ctrl = """import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
import { InspectionService } from './inspection.service';
import { InspectionDto } from './dto/maintenance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Quality & Inspection')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('inspections')
export class InspectionController {
  constructor(private readonly inspectionService: InspectionService) {}

  @Post('job/:jobId')
  @Roles('Foreman', 'Inspector')
  @ApiOperation({ summary: 'Log a Quality Check for an in-progress job' })
  async performInspection(@Param('jobId') jobId: string, @Body() dto: InspectionDto) {
    return this.inspectionService.performInspection(jobId, dto);
  }
}
"""
with open(os.path.join(base_dir, "maintenance/inspection.controller.ts"), "w", encoding="utf-8") as f: f.write(insp_ctrl)


admin_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { MaintenanceService } from './maintenance.service';
import { CreateMaintenanceJobDto } from './dto/maintenance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Maintenance Administration')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/maintenance')
export class AdminController {
  constructor(private readonly maintenanceService: MaintenanceService) {}

  @Post('jobs')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Create a new Scheduled/Preventive Job' })
  async createJob(@Body() dto: CreateMaintenanceJobDto) {
    return this.maintenanceService.createJob(dto);
  }
}
"""
with open(os.path.join(base_dir, "maintenance/admin.controller.ts"), "w", encoding="utf-8") as f: f.write(admin_ctrl)


# 5. Modules
maint_mod = """import { Module } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "maintenance/maintenance.module.ts"), "w", encoding="utf-8") as f: f.write(maint_mod)

app_module = """import { Module } from '@nestjs/common';
import { MaintenanceModule } from './maintenance/maintenance.module';

@Module({
  imports: [MaintenanceModule],
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
    .setTitle('MSRTC Maintenance & Workshop Service')
    .setDescription('Fleet repairs, inspections, and breakdown management')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/maintenance', app, document);

  await app.listen(3016);
  console.log('Maintenance Service is running on http://localhost:3016');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Maintenance Service Phase 2 Scaffolded (Workshop, Inspection, Breakdown, Controllers)")
