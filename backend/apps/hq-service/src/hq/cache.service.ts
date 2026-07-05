import { Injectable } from '@nestjs/common';

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
