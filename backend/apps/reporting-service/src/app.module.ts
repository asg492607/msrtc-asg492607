import { Module } from '@nestjs/common';
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
