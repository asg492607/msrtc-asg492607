import { Injectable, Logger } from '@nestjs/common';
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
