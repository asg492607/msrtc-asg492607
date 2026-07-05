import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { AccountType, TransactionSource } from '../enums/finance.enums';

@Injectable()
export class FinanceRepository {
  constructor(private prisma: PrismaService) {}

  async createJournalEntry(data: any) {
    return this.prisma.journalEntry.create({ data });
  }

  async getLedgerBalance(accountType: AccountType) {
    // In a real app, this would aggregate debits and credits
    return 100000; 
  }

  async logExpense(data: any) {
    return this.prisma.depotExpense.create({ data });
  }

  async logReconciliation(data: any) {
    return this.prisma.reconciliationLog.create({ data });
  }

  async createPayrollRecord(data: any) {
    return this.prisma.payrollRecord.create({ data });
  }
}
