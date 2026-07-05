import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { AlertSeverity } from '../enums/hq.enums';

@Injectable()
export class HqRepository {
  constructor(private prisma: PrismaService) {}

  async saveAlert(data: any) {
    return this.prisma.operationalAlert.create({ data });
  }

  async saveReport(data: any) {
    return this.prisma.generatedReport.create({ data });
  }
}
