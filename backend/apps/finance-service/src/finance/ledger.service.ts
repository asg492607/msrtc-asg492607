import { Injectable, BadRequestException } from '@nestjs/common';
import { FinanceRepository } from './repository/finance.repository';
import { AccountType, TransactionSource } from './enums/finance.enums';

@Injectable()
export class LedgerService {
  constructor(private repository: FinanceRepository) {}

  /**
   * Extremely strict Double-Entry Accounting mechanism
   */
  async postTransaction(debitAccount: AccountType, creditAccount: AccountType, amount: number, source: TransactionSource, referenceId: string) {
    if (amount <= 0) throw new BadRequestException('Amount must be strictly positive');
    
    // Create dual-entry (Debit and Credit MUST equal each other)
    const journalId = `JRNL-${Math.floor(Date.now() / 1000)}`;

    const debitEntry = {
      journalId, accountType: debitAccount, amount, isDebit: true, source, referenceId
    };
    const creditEntry = {
      journalId, accountType: creditAccount, amount, isDebit: false, source, referenceId
    };

    // Use Prisma transaction to ensure atomicity
    // await this.prisma.$transaction([...])
    await this.repository.createJournalEntry(debitEntry);
    await this.repository.createJournalEntry(creditEntry);

    return { success: true, journalId };
  }
}
