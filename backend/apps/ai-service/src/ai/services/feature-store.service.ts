import { Injectable, Logger } from '@nestjs/common';
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
