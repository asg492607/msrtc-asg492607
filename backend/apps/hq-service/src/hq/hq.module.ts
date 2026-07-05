import { Module } from '@nestjs/common';
import { DashboardController } from './dashboard.controller';
import { AnalyticsController } from './analytics.controller';
import { ReportsController } from './reports.controller';
import { AlertsController } from './alerts.controller';
import { AdminController } from './admin.controller';
import { DashboardService } from './dashboard.service';
import { AnalyticsService } from './analytics.service';
import { AggregationService } from './aggregation.service';
import { ForecastingService } from './forecasting.service';
import { AlertService } from './alert.service';
import { CacheService } from './cache.service';
import { HqRepository } from './repository/hq.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [
    DashboardController, AnalyticsController, ReportsController, 
    AlertsController, AdminController
  ],
  providers: [
    DashboardService, AnalyticsService, AggregationService, 
    ForecastingService, AlertService, CacheService, HqRepository
  ],
})
export class HqModule {}
