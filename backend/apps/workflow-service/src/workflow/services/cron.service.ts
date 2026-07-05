import { Injectable, Logger, OnModuleInit } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { PrismaService } from '../../prisma/prisma.service';
import { AutomationService } from './automation.service';
import { LockService } from '@msrtc/redis';

@Injectable()
export class CronService implements OnModuleInit {
  private readonly logger = new Logger(CronService.name);

  constructor(
    private prisma: PrismaService,
    private automation: AutomationService,
    private lockService: LockService
  ) {}

  async onModuleInit() {
    // Seed some default workflows if none exist
    const count = await this.prisma.workflowJob.count();
    if (count === 0) {
      await this.prisma.workflowJob.createMany({
        data: [
          { name: 'seat-lock-sweep', topicToEmit: 'seat.events', cron: CronExpression.EVERY_5_MINUTES, payload: { action: 'sweep_expired' } },
          { name: 'pass-expiry-reminder', topicToEmit: 'pass.events', cron: CronExpression.EVERY_DAY_AT_MIDNIGHT, payload: { action: 'send_reminders' } }
        ]
      });
    }
  }

  // A generic dispatcher that runs every minute, checks the DB, and fires events
  // For this demonstration, we use a fixed 5-minute interval to simulate the cron sweep
  @Cron(CronExpression.EVERY_5_MINUTES)
  async evaluateWorkflows() {
    this.logger.log('Evaluating pending workflows...');
    
    // 1. Acquire Distributed Lock to prevent multiple workflow-service instances from running this simultaneously
    const lockToken = await this.lockService.acquire('workflow:cron:lock', 300); // 5 min lock
    if (!lockToken) {
      this.logger.warn('Another instance is currently evaluating workflows. Skipping.');
      return;
    }

    try {
      const activeJobs = await this.prisma.workflowJob.findMany({ where: { isActive: true } });
      
      for (const job of activeJobs) {
        const startTime = Date.now();
        try {
          // Dispatch the Kafka command
          await this.automation.executeCommand(job.topicToEmit, job.payload);
          
          // Log success
          await this.prisma.workflowHistory.create({
            data: { jobId: job.id, status: 'SUCCESS', durationMs: Date.now() - startTime }
          });
        } catch (error) {
          // Log failure
          await this.prisma.workflowHistory.create({
            data: { jobId: job.id, status: 'FAILED', error: error.message, durationMs: Date.now() - startTime }
          });
        }
      }
    } finally {
      // Release lock
      await this.lockService.release('workflow:cron:lock', lockToken);
    }
  }
}
