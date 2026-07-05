import { Injectable } from '@nestjs/common';
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
