import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\finance-service\src"

# 1. Repository
fin_repo = """import { Injectable } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "finance/repository/finance.repository.ts"), "w", encoding="utf-8") as f: f.write(fin_repo)


# 2. Engines (Ledger, Expense)
ledger_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "finance/ledger.service.ts"), "w", encoding="utf-8") as f: f.write(ledger_svc)

expense_svc = """import { Injectable } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "finance/expense.service.ts"), "w", encoding="utf-8") as f: f.write(expense_svc)


# 3. Operations (Reconciliation, Payroll, GST)
recon_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "finance/reconciliation.service.ts"), "w", encoding="utf-8") as f: f.write(recon_svc)


payroll_svc = """import { Injectable } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "finance/payroll.service.ts"), "w", encoding="utf-8") as f: f.write(payroll_svc)


gst_svc = """import { Injectable } from '@nestjs/common';

@Injectable()
export class GstService {
  calculateGST(amount: number): number {
    return amount * 0.05; // 5% GST for transit
  }

  generateMonthlyReport() {
    return {
      month: new Date().getMonth(),
      totalTaxableRevenue: 1000000,
      totalGstCollected: 50000
    };
  }
}
"""
with open(os.path.join(base_dir, "finance/gst.service.ts"), "w", encoding="utf-8") as f: f.write(gst_svc)


finance_svc = """import { Injectable } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "finance/finance.service.ts"), "w", encoding="utf-8") as f: f.write(finance_svc)


# 4. Controllers
fin_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { FinanceService } from './finance.service';
import { RevenueEntryDto } from './dto/finance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Core Accounting')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('finance')
export class FinanceController {
  constructor(private readonly financeService: FinanceService) {}

  @Post('revenue')
  @Roles('Finance_Officer', 'System') // System calls this via Kafka usually
  @ApiOperation({ summary: 'Record revenue into the ledger (Double-entry)' })
  async recordRevenue(@Body() dto: RevenueEntryDto) {
    return this.financeService.recordRevenue(dto);
  }
}
"""
with open(os.path.join(base_dir, "finance/finance.controller.ts"), "w", encoding="utf-8") as f: f.write(fin_ctrl)


recon_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { ReconciliationService } from './reconciliation.service';
import { ReconciliationDto } from './dto/finance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Reconciliation & Audit')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('reconciliation')
export class ReconciliationController {
  constructor(private readonly reconciliationService: ReconciliationService) {}

  @Post('depot')
  @Roles('Auditor', 'HQ_Admin')
  @ApiOperation({ summary: 'Reconcile depot cash collections against digital ledger' })
  async reconcileDepot(@Body() dto: ReconciliationDto) {
    return this.reconciliationService.reconcileDepotCash(dto);
  }
}
"""
with open(os.path.join(base_dir, "finance/reconciliation.controller.ts"), "w", encoding="utf-8") as f: f.write(recon_ctrl)


exp_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { ExpenseService } from './expense.service';
import { ExpenseDto } from './dto/finance.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Expense Management')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('expenses')
export class ExpenseController {
  constructor(private readonly expenseService: ExpenseService) {}

  @Post()
  @Roles('Depot_Manager', 'Finance_Officer')
  @ApiOperation({ summary: 'Log a depot-level operational expense' })
  async logExpense(@Body() dto: ExpenseDto) {
    return this.expenseService.recordDepotExpense(dto);
  }
}
"""
with open(os.path.join(base_dir, "finance/expense.controller.ts"), "w", encoding="utf-8") as f: f.write(exp_ctrl)


admin_ctrl = """import { Controller, Get, UseGuards } from '@nestjs/common';
import { GstService } from './gst.service';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Financial Reporting')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/finance')
export class AdminController {
  constructor(private readonly gstService: GstService) {}

  @Get('gst-report')
  @Roles('HQ_Admin', 'Auditor')
  @ApiOperation({ summary: 'Generate monthly GST liability report' })
  async getGstReport() {
    return this.gstService.generateMonthlyReport();
  }
}
"""
with open(os.path.join(base_dir, "finance/admin.controller.ts"), "w", encoding="utf-8") as f: f.write(admin_ctrl)


# 5. Modules
fin_mod = """import { Module } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "finance/finance.module.ts"), "w", encoding="utf-8") as f: f.write(fin_mod)

app_module = """import { Module } from '@nestjs/common';
import { FinanceModule } from './finance/finance.module';

@Module({
  imports: [FinanceModule],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(app_module)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AllExceptionsFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.useGlobalFilters(new AllExceptionsFilter());
  
  app.setGlobalPrefix('api/v1');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Finance & Accounting Service')
    .setDescription('Double-entry ledger, Reconciliation, and Payroll')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/finance', app, document);

  await app.listen(3017);
  console.log('Finance Service is running on http://localhost:3017');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Finance Service Phase 2 Scaffolded (Ledger, Reconciliation, Payroll, Controllers)")
