import { Injectable } from '@nestjs/common';
import { RedisService } from './redis.service';

@Injectable()
export class CacheService {
  constructor(private redisService: RedisService) {}

  async set(key: string, value: any, ttlSeconds?: number): Promise<void> {
    const client = this.redisService.getClient();
    const payload = JSON.stringify(value);
    
    if (ttlSeconds) {
      await client.set(key, payload, 'EX', ttlSeconds);
    } else {
      await client.set(key, payload);
    }
  }

  async get<T>(key: string): Promise<T | null> {
    const client = this.redisService.getClient();
    const data = await client.get(key);
    if (!data) return null;
    return JSON.parse(data) as T;
  }

  async delete(key: string): Promise<void> {
    const client = this.redisService.getClient();
    await client.del(key);
  }
}
