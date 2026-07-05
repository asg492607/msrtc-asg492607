import { Injectable, Logger } from '@nestjs/common';
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
