import { Injectable, OnModuleInit } from '@nestjs/common';
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
