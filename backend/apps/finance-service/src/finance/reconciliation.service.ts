import { Injectable, BadRequestException } from '@nestjs/common';
import { FinanceRepository } from './repository/finance.repository';
import { ReconciliationDto } from './dto/finance.dto';

@Injectable()
export class ReconciliationService {
  constructor(private repository: FinanceRepository) {}

  async reconcileDepotCash(dto: ReconciliationDto) {
    // 1. Fetch all digital revenue attributed to this depot (mocked)
    const digitalRevenue = 50000;
    
    // 2. Compare with reported physical cash
    const discrepancy = dto.reportedCash - digitalRevenue;

    const log = await this.repository.logReconciliation({
      depotId: dto.depotId,
      expectedAmount: digitalRevenue,
      actualAmount: dto.reportedCash,
      discrepancy,
      reconciledAt: new Date()
    });

    if (discrepancy !== 0) {
      // Fire Kafka Event -> finance.reconciliation.discrepancy
      console.warn(`[AUDIT] Discrepancy found at Depot ${dto.depotId}: ${discrepancy}`);
    }

    return log;
  }
}
