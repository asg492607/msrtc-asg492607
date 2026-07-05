import { Injectable } from '@nestjs/common';
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
