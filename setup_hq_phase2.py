import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\hq-service\src"

# 1. Repository
hq_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { AlertSeverity } from '../enums/hq.enums';

@Injectable()
export class HqRepository {
  constructor(private prisma: PrismaService) {}

  async saveAlert(data: any) {
    return this.prisma.operationalAlert.create({ data });
  }

  async saveReport(data: any) {
    return this.prisma.generatedReport.create({ data });
  }
}
"""
with open(os.path.join(base_dir, "hq/repository/hq.repository.ts"), "w", encoding="utf-8") as f: f.write(hq_repo)


# 2. Engines (Cache, Aggregation)
cache_svc = """import { Injectable } from '@nestjs/common';

@Injectable()
export class CacheService {
  // In a real app, this would use Redis client
  private cache = new Map<string, any>();

  async setMetric(key: string, value: any, ttlSeconds: number = 60) {
    this.cache.set(key, value);
    // implementation of ttl mocked
  }

  async getMetric(key: string) {
    return this.cache.get(key) || null;
  }
}
"""
with open(os.path.join(base_dir, "hq/cache.service.ts"), "w", encoding="utf-8") as f: f.write(cache_svc)

aggregation_svc = """import { Injectable, OnModuleInit } from '@nestjs/common';
import { CacheService } from './cache.service';

@Injectable()
export class AggregationService implements OnModuleInit {
  constructor(private cache: CacheService) {}

  onModuleInit() {
    // Here we would setup Kafka Consumers for:
    // booking.*, depot.*, finance.*, maintenance.*, etc.
    this.startMockAggregation();
  }

  private startMockAggregation() {
    // Mocks consuming streams and updating Redis
    setInterval(() => {
      this.cache.setMetric('hq:live:active_fleet', Math.floor(Math.random() * 500) + 4000);
      this.cache.setMetric('hq:live:today_revenue', Math.floor(Math.random() * 1000000) + 5000000);
      this.cache.setMetric('hq:live:active_complaints', Math.floor(Math.random() * 50) + 10);
    }, 5000);
  }
}
"""
with open(os.path.join(base_dir, "hq/aggregation.service.ts"), "w", encoding="utf-8") as f: f.write(aggregation_svc)


# 3. Operations (Alert, Forecasting, Dashboard, Analytics)
alert_svc = """import { Injectable } from '@nestjs/common';
import { HqRepository } from './repository/hq.repository';
import { AlertSeverity } from './enums/hq.enums';

@Injectable()
export class AlertService {
  constructor(private repository: HqRepository) {}

  async triggerAlert(title: string, message: string, severity: AlertSeverity) {
    const alert = await this.repository.saveAlert({ title, message, severity, triggeredAt: new Date() });
    
    if (severity === AlertSeverity.CRITICAL) {
      // Send WebSocket or Push notification to Executive App
      console.error(`[CRITICAL HQ ALERT] ${title}: ${message}`);
    }

    return alert;
  }
}
"""
with open(os.path.join(base_dir, "hq/alert.service.ts"), "w", encoding="utf-8") as f: f.write(alert_svc)

forecast_svc = """import { Injectable } from '@nestjs/common';

@Injectable()
export class ForecastingService {
  async predictPassengerDemand(routeId: string) {
    // Interface for future Machine Learning models
    return {
      routeId,
      predictedPassengersNext7Days: 4500,
      confidenceScore: 0.89
    };
  }
}
"""
with open(os.path.join(base_dir, "hq/forecasting.service.ts"), "w", encoding="utf-8") as f: f.write(forecast_svc)

dashboard_svc = """import { Injectable } from '@nestjs/common';
import { CacheService } from './cache.service';

@Injectable()
export class DashboardService {
  constructor(private cache: CacheService) {}

  async getExecutiveSnapshot() {
    return {
      activeFleet: await this.cache.getMetric('hq:live:active_fleet') || 0,
      todayRevenue: await this.cache.getMetric('hq:live:today_revenue') || 0,
      activeComplaints: await this.cache.getMetric('hq:live:active_complaints') || 0,
      timestamp: new Date().toISOString()
    };
  }
}
"""
with open(os.path.join(base_dir, "hq/dashboard.service.ts"), "w", encoding="utf-8") as f: f.write(dashboard_svc)

analytics_svc = """import { Injectable } from '@nestjs/common';

@Injectable()
export class AnalyticsService {
  async getRevenueVsExpense() {
    // Would run complex Prisma queries on historical data
    return {
      status: 'healthy',
      revenueYTD: 150000000,
      expenseYTD: 110000000,
      margin: '26.6%'
    };
  }
}
"""
with open(os.path.join(base_dir, "hq/analytics.service.ts"), "w", encoding="utf-8") as f: f.write(analytics_svc)


# 4. Controllers
dash_ctrl = """import { Controller, Get, UseGuards } from '@nestjs/common';
import { DashboardService } from './dashboard.service';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Executive Dashboard')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('dashboard')
export class DashboardController {
  constructor(private readonly dashboardService: DashboardService) {}

  @Get('live')
  @Roles('Executive', 'HQ_Admin')
  @ApiOperation({ summary: 'Get real-time cached KPIs for the entire platform' })
  async getLiveSnapshot() {
    return this.dashboardService.getExecutiveSnapshot();
  }
}
"""
with open(os.path.join(base_dir, "hq/dashboard.controller.ts"), "w", encoding="utf-8") as f: f.write(dash_ctrl)

analytics_ctrl = """import { Controller, Get, UseGuards } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "hq/analytics.controller.ts"), "w", encoding="utf-8") as f: f.write(analytics_ctrl)


reports_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { ReportConfigDto } from './dto/hq.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Report Generation')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('reports')
export class ReportsController {
  @Post('generate')
  @Roles('Executive', 'HQ_Admin', 'Regional_Admin')
  @ApiOperation({ summary: 'Generate a PDF/CSV historical report' })
  async generateReport(@Body() dto: ReportConfigDto) {
    return { success: true, message: `Report ${dto.reportName} generation started in background.` };
  }
}
"""
with open(os.path.join(base_dir, "hq/reports.controller.ts"), "w", encoding="utf-8") as f: f.write(reports_ctrl)

alert_ctrl = """import { Controller, Get, UseGuards } from '@nestjs/common';
import { AlertService } from './alert.service';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Operational Alerts')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('alerts')
export class AlertsController {
  constructor(private readonly alertService: AlertService) {}

  @Get()
  @Roles('Executive', 'HQ_Admin')
  @ApiOperation({ summary: 'Get recent operational anomalies' })
  async getAlerts() {
    return { alerts: [] }; // Mock
  }
}
"""
with open(os.path.join(base_dir, "hq/alerts.controller.ts"), "w", encoding="utf-8") as f: f.write(alert_ctrl)

admin_ctrl = """import { Controller, Get, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('HQ System Config')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/hq')
export class AdminController {
  @Get('health')
  @Roles('HQ_Admin')
  @ApiOperation({ summary: 'Check aggregation engine health' })
  async getHealth() {
    return { status: 'OK', kafkaLag: '0ms', redisLatency: '2ms' };
  }
}
"""
with open(os.path.join(base_dir, "hq/admin.controller.ts"), "w", encoding="utf-8") as f: f.write(admin_ctrl)


# 5. Modules
hq_mod = """import { Module } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "hq/hq.module.ts"), "w", encoding="utf-8") as f: f.write(hq_mod)

app_module = """import { Module } from '@nestjs/common';
import { HqModule } from './hq/hq.module';

@Module({
  imports: [HqModule],
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
    .setTitle('MSRTC HQ & Executive Analytics Service')
    .setDescription('Real-time Executive Command Center and Aggregation Engine')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/hq', app, document);

  await app.listen(3018);
  console.log('HQ Service is running on http://localhost:3018');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("HQ Service Phase 2 Scaffolded (Dashboard, Analytics, Alerts, Controllers)")
