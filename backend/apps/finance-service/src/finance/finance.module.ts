import { Module } from '@nestjs/common';
import { FinanceController } from './finance.controller';
import { ReconciliationController } from './reconciliation.controller';
import { ExpenseController } from './expense.controller';
import { AdminController } from './admin.controller';
import { FinanceService } from './finance.service';
import { LedgerService } from './ledger.service';
import { ExpenseService } from './expense.service';
import { ReconciliationService } from './reconciliation.service';
import { PayrollService } from './payroll.service';
import { GstService } from './gst.service';
import { FinanceRepository } from './repository/finance.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [
    FinanceController, ReconciliationController, 
    ExpenseController, AdminController
  ],
  providers: [
    FinanceService, LedgerService, ExpenseService, 
    ReconciliationService, PayrollService, GstService, FinanceRepository
  ],
})
export class FinanceModule {}
