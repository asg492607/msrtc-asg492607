import { Module } from '@nestjs/common';
import { AuditService } from './audit/services/audit.service';
import { ComplianceService } from './audit/services/compliance.service';
import { AuditController } from './audit/controllers/audit.controller';
import { ComplianceController } from './audit/controllers/compliance.controller';
import { PrismaModule } from './prisma/prisma.module';
import { KafkaModule } from '@msrtc/kafka';

@Module({
  imports: [PrismaModule, KafkaModule],
  controllers: [AuditController, ComplianceController],
  providers: [AuditService, ComplianceService],
})
export class AppModule {}
