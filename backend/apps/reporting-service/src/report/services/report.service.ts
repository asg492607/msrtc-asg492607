import { Injectable, Logger } from '@nestjs/common';
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
