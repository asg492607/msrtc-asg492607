import { Controller, Post, Body, UseGuards } from '@nestjs/common';
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
