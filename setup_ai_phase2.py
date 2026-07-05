import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\ai-service\src"

# 1. Feature Store Service
feature_svc = """import { Injectable, Logger } from '@nestjs/common';
import { CacheService } from '@msrtc/redis';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class FeatureStoreService {
  private readonly logger = new Logger(FeatureStoreService.name);

  constructor(private cache: CacheService, private cls: ClsService) {}

  async getRouteFeatures(routeId: string) {
    const tenantId = this.cls.get('tenantId');
    const key = `tenant:${tenantId}:features:route:${routeId}`;
    
    let features = await this.cache.get(key);
    if (!features) {
      // Simulate heavy DB aggregation for average speed, historical delays, etc.
      features = { avgSpeedKmh: 45, historicalDelayMinutes: 12, seasonalityIndex: 1.2 };
      await this.cache.set(key, JSON.stringify(features), 3600);
    } else {
      features = JSON.parse(features);
    }
    return features;
  }
}
"""
with open(os.path.join(base_dir, "ai/services/feature-store.service.ts"), "w", encoding="utf-8") as f: f.write(feature_svc)


# 2. Demand Service (Dynamic Pricing)
demand_svc = """import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { FeatureStoreService } from './feature-store.service';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class DemandService {
  private readonly logger = new Logger(DemandService.name);

  constructor(
    private prisma: PrismaService,
    private featureStore: FeatureStoreService,
    private cls: ClsService
  ) {}

  async predictDemand(routeId: string, date: string) {
    const startTime = Date.now();
    const features = await this.featureStore.getRouteFeatures(routeId);
    
    // Simulated ML Logic (Random Forest approximation)
    const baseDemand = 60;
    const seasonality = features.seasonalityIndex || 1;
    const predictedOccupancy = Math.min(100, Math.round(baseDemand * seasonality));
    
    const fareMultiplier = predictedOccupancy > 80 ? 1.25 : 1.0;
    const confidence = 0.88;

    const output = { occupancyPercent: predictedOccupancy, fareMultiplier };

    await this.logInference('demand-forecasting-v1', { routeId, date, features }, output, confidence, Date.now() - startTime);

    return output;
  }

  private async logInference(modelName: string, inputs: any, outputs: any, confidence: number, latencyMs: number) {
    const tenantId = this.cls.get('tenantId');
    await this.prisma.inferenceLog.create({
      data: { modelName, tenantId, inputs, outputs, confidence, latencyMs }
    });
  }
}
"""
with open(os.path.join(base_dir, "ai/services/demand.service.ts"), "w", encoding="utf-8") as f: f.write(demand_svc)


# 3. Controllers
prediction_ctrl = """import { Controller, Post, Body } from '@nestjs/common';
import { DemandService } from '../services/demand.service';

@Controller('ai')
export class PredictionController {
  constructor(private demandService: DemandService) {}

  @Post('predict-demand')
  async predictDemand(@Body() body: { routeId: string, date: string }) {
    return this.demandService.predictDemand(body.routeId, body.date);
  }
}
"""
with open(os.path.join(base_dir, "ai/controllers/prediction.controller.ts"), "w", encoding="utf-8") as f: f.write(prediction_ctrl)


# 4. Module & Main
ai_mod = """import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { DemandService } from './ai/services/demand.service';
import { FeatureStoreService } from './ai/services/feature-store.service';
import { PredictionController } from './ai/controllers/prediction.controller';
import { PrismaModule } from './prisma/prisma.module';
import { KafkaModule } from '@msrtc/kafka';
import { RedisModule } from '@msrtc/redis';
import { TenantModule, TenantMiddleware } from '@msrtc/tenant';

@Module({
  imports: [PrismaModule, KafkaModule, RedisModule, TenantModule],
  controllers: [PredictionController],
  providers: [DemandService, FeatureStoreService],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
     // Apply the shared TenantMiddleware from Task 32
     consumer.apply(TenantMiddleware).forRoutes('*');
  }
}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(ai_mod)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.setGlobalPrefix('api/v1');
  await app.listen(3023);
  console.log('AI Service is running on http://localhost:3023');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("AI Service Phase 2 Scaffolded (FeatureStore, Demand Prediction, Tenant middleware)")
