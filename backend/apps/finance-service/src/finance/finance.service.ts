import { Injectable } from '@nestjs/common';
import { LedgerService } from './ledger.service';
import { RevenueEntryDto } from './dto/finance.dto';
import { AccountType } from './enums/finance.enums';

@Injectable()
export class FinanceService {
  constructor(private ledger: LedgerService) {}

  async recordRevenue(dto: RevenueEntryDto) {
    // Debit ASSET, Credit REVENUE
    return this.ledger.postTransaction(
      AccountType.ASSET,
      AccountType.REVENUE,
      dto.amount,
      dto.sourceType,
      dto.sourceId
    );
  }
}
