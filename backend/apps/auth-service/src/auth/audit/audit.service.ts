import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class AuditService {
  constructor(private prisma: PrismaService) {}

  async logAction(userId: string, action: string, status: string, ipAddress?: string, metadata?: any) {
    return this.prisma.iamAuditLog.create({
      data: { userId, action, status, ipAddress, metadata }
    });
  }
}
