import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\workflow-service\src"

# 1. Automation Service (Kafka Publisher)
auto_svc = """import { Injectable, Logger } from '@nestjs/common';
import { EventBusService, Topics } from '@msrtc/kafka';

@Injectable()
export class AutomationService {
  private readonly logger = new Logger(AutomationService.name);

  constructor(private eventBus: EventBusService) {}

  async executeCommand(topic: string, payload: any) {
    this.logger.log(`Dispatching automation command to topic: ${topic}`);
    await this.eventBus.publish(topic, {
      type: 'automation.execute',
      timestamp: new Date().toISOString(),
      ...payload
    });
  }
}
"""
with open(os.path.join(base_dir, "workflow/services/automation.service.ts"), "w", encoding="utf-8") as f: f.write(auto_svc)


# 2. Cron Service (Scheduler + Redis Lock)
cron_svc = """import { Injectable, Logger, OnModuleInit } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "workflow/services/cron.service.ts"), "w", encoding="utf-8") as f: f.write(cron_svc)


# 3. Controller
wf_ctrl = """import { Controller, Post, Get, Param, Body, Request } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Controller('workflows')
export class WorkflowController {
  constructor(private prisma: PrismaService) {}

  @Get('jobs')
  async getJobs() {
    return this.prisma.workflowJob.findMany();
  }

  @Post('jobs/:id/pause')
  async pauseJob(@Param('id') id: string) {
    return this.prisma.workflowJob.update({ where: { id }, data: { isActive: false } });
  }

  @Post('jobs/:id/resume')
  async resumeJob(@Param('id') id: string) {
    return this.prisma.workflowJob.update({ where: { id }, data: { isActive: true } });
  }
}
"""
with open(os.path.join(base_dir, "workflow/controllers/workflow.controller.ts"), "w", encoding="utf-8") as f: f.write(wf_ctrl)


# 4. Module & Main
wf_mod = """import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';
import { CronService } from './workflow/services/cron.service';
import { AutomationService } from './workflow/services/automation.service';
import { WorkflowController } from './workflow/controllers/workflow.controller';
import { PrismaModule } from './prisma/prisma.module';
import { KafkaModule } from '@msrtc/kafka';
import { RedisModule } from '@msrtc/redis';

@Module({
  imports: [PrismaModule, KafkaModule, RedisModule, ScheduleModule.forRoot()],
  controllers: [WorkflowController],
  providers: [CronService, AutomationService],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(wf_mod)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.setGlobalPrefix('api/v1');
  await app.listen(3021);
  console.log('Workflow Service is running on http://localhost:3021');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Workflow Service Phase 2 Scaffolded (Cron, Auto, Controller)")
