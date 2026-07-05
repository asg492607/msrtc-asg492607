import { Controller, Post, Body, UseGuards } from '@nestjs/common';
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
