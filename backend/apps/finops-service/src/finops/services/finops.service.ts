import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class FinOpsService {
  private readonly logger = new Logger(FinOpsService.name);

  constructor(
    private prisma: PrismaService,
    private cls: ClsService
  ) {}

  async getDashboard() {
    const tenantId = this.cls.get('tenantId');
    const budgets = await this.prisma.budget.findMany({ where: { tenantId } });
    
    // Simulate an internal HTTP call to the ai-service (Task 34) for cost forecasting
    const forecastedSpend = budgets.map(b => ({
      serviceName: b.serviceName,
      projectedEomSpend: b.currentSpend * 1.15 // Dummy forecast
    }));

    return {
      currentBudgets: budgets,
      forecasts: forecastedSpend
    };
  }
}
