import { Controller, Get, Param, Post } from '@nestjs/common';
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
