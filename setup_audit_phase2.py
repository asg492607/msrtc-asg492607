import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\audit-service\src"

# 1. Audit Service (Hash Chaining & Consumer)
audit_svc = """import { Injectable, Logger, OnModuleInit } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { ConsumerService, Topics, EventEnvelope } from '@msrtc/kafka';
import * as crypto from 'crypto';

@Injectable()
export class AuditService implements OnModuleInit {
  private readonly logger = new Logger(AuditService.name);

  constructor(
    private prisma: PrismaService,
    private consumer: ConsumerService
  ) {}

  onModuleInit() {
    this.consumer.handleEvent('audit.events', null as any, async (envelope: EventEnvelope) => {
      await this.recordEvent(envelope.payload);
    });
  }

  async recordEvent(payload: any) {
    // 1. Get previous hash
    const lastRecord = await this.prisma.auditRecord.findFirst({
      orderBy: { timestamp: 'desc' }
    });
    const previousHash = lastRecord ? lastRecord.hash : 'GENESIS_HASH';

    // 2. Calculate current hash (payload + previousHash)
    const dataString = JSON.stringify({ ...payload, previousHash });
    const currentHash = crypto.createHash('sha256').update(dataString).digest('hex');

    // 3. Persist Immutable Record
    await this.prisma.auditRecord.create({
      data: {
        userId: payload.userId,
        role: payload.role,
        service: payload.service,
        entityType: payload.entityType,
        entityId: payload.entityId,
        operation: payload.operation,
        oldValues: payload.oldValues,
        newValues: payload.newValues,
        correlationId: payload.correlationId,
        ipAddress: payload.ipAddress,
        status: payload.status || 'SUCCESS',
        previousHash,
        hash: currentHash
      }
    });

    this.logger.log(`Audit recorded for ${payload.entityType}:${payload.entityId}`);
  }

  async verifyChain(): Promise<boolean> {
    const records = await this.prisma.auditRecord.findMany({ orderBy: { timestamp: 'asc' } });
    let expectedPrevious = 'GENESIS_HASH';

    for (const record of records) {
      if (record.previousHash !== expectedPrevious) {
        this.logger.error(`Chain broken at record ${record.id}`);
        return false;
      }
      const dataString = JSON.stringify({
        userId: record.userId,
        role: record.role,
        service: record.service,
        entityType: record.entityType,
        entityId: record.entityId,
        operation: record.operation,
        oldValues: record.oldValues,
        newValues: record.newValues,
        correlationId: record.correlationId,
        ipAddress: record.ipAddress,
        status: record.status,
        previousHash: record.previousHash
      });
      const calculatedHash = crypto.createHash('sha256').update(dataString).digest('hex');
      
      if (calculatedHash !== record.hash) {
        this.logger.error(`Data tampered at record ${record.id}`);
        return false;
      }
      expectedPrevious = record.hash;
    }
    return true;
  }
}
"""
with open(os.path.join(base_dir, "audit/services/audit.service.ts"), "w", encoding="utf-8") as f: f.write(audit_svc)


# 2. Compliance Service
compliance_svc = """import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { EventBusService } from '@msrtc/kafka';

@Injectable()
export class ComplianceService {
  private readonly logger = new Logger(ComplianceService.name);

  constructor(
    private prisma: PrismaService,
    private eventBus: EventBusService
  ) {}

  async requestDataExport(targetUserId: string, requestedBy: string) {
    const request = await this.prisma.complianceRequest.create({
      data: { type: 'EXPORT', targetUserId, requestedBy, status: 'PENDING' }
    });

    // Fire & Forget background processing
    this.processExport(request.id, targetUserId).catch(e => this.logger.error(e));

    return { requestId: request.id, status: 'PENDING' };
  }

  private async processExport(requestId: string, targetUserId: string) {
    await this.prisma.complianceRequest.update({ where: { id: requestId }, data: { status: 'PROCESSING' } });
    
    // In reality: Query all DBs or emit Kafka events asking services to dump user data
    // Then generate CSV, upload to File Service, and get fileId.
    const mockFileId = 'file-gdpr-123';

    await this.prisma.complianceRequest.update({
      where: { id: requestId },
      data: { status: 'COMPLETED', fileId: mockFileId, completedAt: new Date() }
    });

    await this.eventBus.publish('compliance.events', { type: 'compliance.export.completed', requestId, fileId: mockFileId });
  }

  async executeRightToErasure(targetUserId: string, requestedBy: string) {
    const request = await this.prisma.complianceRequest.create({
      data: { type: 'DELETION', targetUserId, requestedBy, status: 'PENDING' }
    });
    
    // Broadcast strict deletion command across the Kafka network
    await this.eventBus.publish('compliance.events', { type: 'command.erase.user_data', targetUserId });

    await this.prisma.complianceRequest.update({ where: { id: request.id }, data: { status: 'COMPLETED', completedAt: new Date() } });
    return { requestId: request.id, status: 'COMPLETED' };
  }
}
"""
with open(os.path.join(base_dir, "audit/services/compliance.service.ts"), "w", encoding="utf-8") as f: f.write(compliance_svc)


# 3. Controllers
audit_ctrl = """import { Controller, Get, Param, Post } from '@nestjs/common';
import { AuditService } from '../services/audit.service';
import { PrismaService } from '../../prisma/prisma.service';

@Controller('audit')
export class AuditController {
  constructor(private auditService: AuditService, private prisma: PrismaService) {}

  @Get('entity/:type/:id')
  async getEntityHistory(@Param('type') entityType: string, @Param('id') entityId: string) {
    return this.prisma.auditRecord.findMany({ where: { entityType, entityId }, orderBy: { timestamp: 'desc' } });
  }

  @Post('verify-chain')
  async verifyChain() {
    const isValid = await this.auditService.verifyChain();
    return { valid: isValid };
  }
}
"""
with open(os.path.join(base_dir, "audit/controllers/audit.controller.ts"), "w", encoding="utf-8") as f: f.write(audit_ctrl)

compliance_ctrl = """import { Controller, Post, Body, Request } from '@nestjs/common';
import { ComplianceService } from '../services/compliance.service';

@Controller('compliance')
export class ComplianceController {
  constructor(private complianceService: ComplianceService) {}

  @Post('data-export')
  async exportData(@Body('targetUserId') targetUserId: string, @Request() req: any) {
    const requestedBy = 'compliance-officer'; // mocked
    return this.complianceService.requestDataExport(targetUserId, requestedBy);
  }

  @Post('data-deletion')
  async deleteData(@Body('targetUserId') targetUserId: string, @Request() req: any) {
    const requestedBy = 'compliance-officer'; // mocked
    return this.complianceService.executeRightToErasure(targetUserId, requestedBy);
  }
}
"""
with open(os.path.join(base_dir, "audit/controllers/compliance.controller.ts"), "w", encoding="utf-8") as f: f.write(compliance_ctrl)


# 4. Module & Main
audit_mod = """import { Module } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(audit_mod)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.setGlobalPrefix('api/v1');
  await app.listen(3022);
  console.log('Audit Service is running on http://localhost:3022');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Audit Service Phase 2 Scaffolded (AuditService, ComplianceService, Controllers)")
