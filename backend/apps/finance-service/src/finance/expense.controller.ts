import { Controller, Post, Body, UseGuards } from '@nestjs/common';
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
