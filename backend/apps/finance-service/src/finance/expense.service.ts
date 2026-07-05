import { Injectable } from '@nestjs/common';
import { FinanceRepository } from './repository/finance.repository';
import { LedgerService } from './ledger.service';
import { ExpenseDto } from './dto/finance.dto';
import { AccountType, TransactionSource } from './enums/finance.enums';

@Injectable()
export class ExpenseService {
  constructor(
    private repository: FinanceRepository,
    private ledger: LedgerService
  ) {}

  async recordDepotExpense(dto: ExpenseDto) {
    const expense = await this.repository.logExpense(dto);
    
    // Debit EXPENSE, Credit ASSET (Cash)
    await this.ledger.postTransaction(
      AccountType.EXPENSE, 
      AccountType.ASSET, 
      dto.amount, 
      TransactionSource.DEPOT_EXPENSE, 
      expense.id
    );

    return expense;
  }
}
