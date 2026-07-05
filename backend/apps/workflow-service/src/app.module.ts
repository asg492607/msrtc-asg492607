import { Module } from '@nestjs/common';
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
