import { Injectable } from '@nestjs/common';
import { FinanceRepository } from './repository/finance.repository';
import { LedgerService } from './ledger.service';
import { AccountType, TransactionSource } from './enums/finance.enums';

@Injectable()
export class PayrollService {
  constructor(
    private repository: FinanceRepository,
    private ledger: LedgerService
  ) {}

  async generatePayroll(crewId: string, hoursWorked: number) {
    // Extremely simplified calculation
    const hourlyRate = 200;
    const grossPay = hoursWorked * hourlyRate;
    const taxDeduction = grossPay * 0.10;
    const netPay = grossPay - taxDeduction;

    const record = await this.repository.createPayrollRecord({
      crewId, hoursWorked, grossPay, taxDeduction, netPay, processedAt: new Date()
    });

    // Debit EXPENSE, Credit ASSET (Cash/Bank)
    await this.ledger.postTransaction(
      AccountType.EXPENSE,
      AccountType.ASSET,
      netPay,
      TransactionSource.PAYROLL,
      record.id
    );

    return record;
  }
}
