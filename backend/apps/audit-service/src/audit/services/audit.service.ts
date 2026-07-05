import { Injectable, Logger, OnModuleInit } from '@nestjs/common';
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
