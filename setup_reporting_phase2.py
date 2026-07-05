import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\reporting-service\src"

# 1. Report Service (Async processing)
report_svc = """import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { ExportService } from './export.service';
import { EventBusService, Topics } from '@msrtc/kafka';
import axios from 'axios';

@Injectable()
export class ReportService {
  private readonly logger = new Logger(ReportService.name);

  constructor(
    private prisma: PrismaService,
    private exportService: ExportService,
    private eventBus: EventBusService
  ) {}

  async queueReport(type: string, requestedBy: string, parameters: any) {
    const job = await this.prisma.reportJob.create({
      data: { type, requestedBy, parameters, status: 'PENDING' }
    });

    // Fire & Forget background processing
    this.processJob(job.id).catch(e => this.logger.error(e));

    return { jobId: job.id, status: 'PENDING' };
  }

  private async processJob(jobId: string) {
    await this.prisma.reportJob.update({ where: { id: jobId }, data: { status: 'PROCESSING' } });

    try {
      const job = await this.prisma.reportJob.findUnique({ where: { id: jobId } });
      
      // Simulate heavy data aggregation (e.g. JOINing across millions of rows)
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const mockData = [
        { date: '2026-07-01', revenue: 500000, bookings: 1200 },
        { date: '2026-07-02', revenue: 650000, bookings: 1450 }
      ];

      const csvBuffer = this.exportService.generateCsv(mockData);

      // Upload to File Service via HTTP (since File Service abstracts MinIO)
      // For this implementation, we will simulate a fileId response.
      // In reality: await axios.post('http://file-service/files/upload', form, ...)
      const mockFileId = 'file-abc-123';

      await this.prisma.reportJob.update({
        where: { id: jobId },
        data: { status: 'COMPLETED', fileId: mockFileId, completedAt: new Date() }
      });

      // Notify user
      await this.eventBus.publish('report.events', {
        type: 'report.generated',
        jobId,
        fileId: mockFileId,
        requestedBy: job.requestedBy
      });

      this.logger.log(`Report Job ${jobId} completed successfully.`);
    } catch (error) {
      await this.prisma.reportJob.update({
        where: { id: jobId },
        data: { status: 'FAILED', error: error.message }
      });
      this.logger.error(`Report Job ${jobId} failed: ${error.message}`);
    }
  }

  async getJobStatus(jobId: string) {
    const job = await this.prisma.reportJob.findUnique({ where: { id: jobId } });
    if (!job) throw new Error('Job not found');
    return { status: job.status, fileId: job.fileId, error: job.error };
  }
}
"""
with open(os.path.join(base_dir, "report/services/report.service.ts"), "w", encoding="utf-8") as f: f.write(report_svc)


# 2. Scheduler Service
scheduler_svc = """import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { PrismaService } from '../../prisma/prisma.service';
import { ReportService } from './report.service';

@Injectable()
export class SchedulerService {
  private readonly logger = new Logger(SchedulerService.name);

  constructor(
    private prisma: PrismaService,
    private reportService: ReportService
  ) {}

  @Cron(CronExpression.EVERY_DAY_AT_MIDNIGHT)
  async handleDailyReports() {
    this.logger.log('Running daily scheduled reports...');
    const schedules = await this.prisma.reportSchedule.findMany({
      where: { isActive: true, cron: '0 0 * * *' } // simplified check
    });

    for (const schedule of schedules) {
      await this.reportService.queueReport(schedule.type, schedule.requestedBy, schedule.parameters);
    }
  }
}
"""
with open(os.path.join(base_dir, "report/services/scheduler.service.ts"), "w", encoding="utf-8") as f: f.write(scheduler_svc)


# 3. Controllers
report_ctrl = """import { Controller, Post, Get, Param, Body, Request } from '@nestjs/common';
import { ReportService } from '../services/report.service';

@Controller('reports')
export class ReportController {
  constructor(private reportService: ReportService) {}

  @Post('generate')
  async requestReport(@Body() body: { type: string, parameters: any }, @Request() req: any) {
    const userId = 'sys-admin'; // mock req.user.userId
    return this.reportService.queueReport(body.type, userId, body.parameters);
  }

  @Get(':id')
  async getReportStatus(@Param('id') id: string) {
    return this.reportService.getJobStatus(id);
  }
}
"""
with open(os.path.join(base_dir, "report/controllers/report.controller.ts"), "w", encoding="utf-8") as f: f.write(report_ctrl)


schedule_ctrl = """import { Controller, Post, Body, Request } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Controller('reports/schedules')
export class ScheduleController {
  constructor(private prisma: PrismaService) {}

  @Post()
  async createSchedule(@Body() body: any, @Request() req: any) {
    return this.prisma.reportSchedule.create({
      data: {
        type: body.type,
        cron: body.cron,
        deliveryType: body.deliveryType,
        parameters: body.parameters,
        requestedBy: 'sys-admin'
      }
    });
  }
}
"""
with open(os.path.join(base_dir, "report/controllers/schedule.controller.ts"), "w", encoding="utf-8") as f: f.write(schedule_ctrl)


# 4. Module & Main
report_mod = """import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';
import { ReportService } from './report/services/report.service';
import { ExportService } from './report/services/export.service';
import { SchedulerService } from './report/services/scheduler.service';
import { ReportController } from './report/controllers/report.controller';
import { ScheduleController } from './report/controllers/schedule.controller';
import { PrismaModule } from './prisma/prisma.module';
import { KafkaModule } from '@msrtc/kafka';

@Module({
  imports: [PrismaModule, KafkaModule, ScheduleModule.forRoot()],
  controllers: [ReportController, ScheduleController],
  providers: [ReportService, ExportService, SchedulerService],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(report_mod)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.setGlobalPrefix('api/v1');
  await app.listen(3020);
  console.log('Reporting Service is running on http://localhost:3020');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Reporting Service Phase 2 Scaffolded (ReportService, Cron, Controllers)")
