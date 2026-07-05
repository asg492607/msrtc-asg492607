import { Controller, Get, UseGuards } from '@nestjs/common';
import { AnalyticsService } from './analytics.service';
import { ForecastingService } from './forecasting.service';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Deep Analytics & Forecasting')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('analytics')
export class AnalyticsController {
  constructor(
    private readonly analyticsService: AnalyticsService,
    private readonly forecastingService: ForecastingService
  ) {}

  @Get('finance')
  @Roles('Executive', 'HQ_Admin')
  @ApiOperation({ summary: 'Get YTD Revenue vs Expense analysis' })
  async getFinanceAnalytics() {
    return this.analyticsService.getRevenueVsExpense();
  }

  @Get('forecast/demand')
  @Roles('Executive', 'HQ_Admin')
  @ApiOperation({ summary: 'Get AI-driven passenger demand forecast' })
  async getDemandForecast() {
    return this.forecastingService.predictPassengerDemand('RTE-MUM-PUN');
  }
}
