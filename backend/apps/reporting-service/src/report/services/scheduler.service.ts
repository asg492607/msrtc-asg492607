import { Injectable, Logger } from '@nestjs/common';
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
