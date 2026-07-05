import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\packages\redis\src"

# 1. Connection Manager
redis_svc = """import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import Redis from 'ioredis';

@Injectable()
export class RedisService implements OnModuleInit, OnModuleDestroy {
  private client: Redis;

  onModuleInit() {
    this.client = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: Number(process.env.REDIS_PORT) || 6379,
    });
  }

  onModuleDestroy() {
    this.client.quit();
  }

  getClient(): Redis {
    return this.client;
  }
}
"""
with open(os.path.join(base_dir, "redis.service.ts"), "w", encoding="utf-8") as f: f.write(redis_svc)


# 2. Cache Service
cache_svc = """import { Injectable } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "cache.service.ts"), "w", encoding="utf-8") as f: f.write(cache_svc)


# 3. Lock Service
lock_svc = """import { Injectable, Logger } from '@nestjs/common';
import { RedisService } from './redis.service';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class LockService {
  private readonly logger = new Logger(LockService.name);

  constructor(private redisService: RedisService) {}

  /**
   * Attempts to acquire a distributed lock using SET NX EX.
   * @param key The lock key (e.g., seat:lock:123:4A)
   * @param ttlSeconds How long the lock should be held
   * @returns A lockToken if successful, null if lock is already held.
   */
  async acquire(key: string, ttlSeconds: number): Promise<string | null> {
    const client = this.redisService.getClient();
    const lockToken = uuidv4();

    // EX: Expiry time in seconds
    // NX: Only set if the key does not exist
    const result = await client.set(key, lockToken, 'EX', ttlSeconds, 'NX');

    if (result === 'OK') {
      this.logger.debug(`Acquired lock: ${key} (Token: ${lockToken})`);
      return lockToken;
    }
    
    return null;
  }

  /**
   * Safely releases the lock using a LUA script to ensure that the client 
   * only releases the lock if it holds the correct lockToken.
   */
  async release(key: string, lockToken: string): Promise<boolean> {
    const client = this.redisService.getClient();
    const luaScript = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;

    const result = await client.eval(luaScript, 1, key, lockToken);
    
    if (result === 1) {
      this.logger.debug(`Released lock: ${key}`);
      return true;
    }
    
    this.logger.warn(`Failed to release lock: ${key} (Invalid token or expired)`);
    return false;
  }
}
"""
with open(os.path.join(base_dir, "lock.service.ts"), "w", encoding="utf-8") as f: f.write(lock_svc)


# 4. PubSub Service
pubsub_svc = """import { Injectable } from '@nestjs/common';
import { RedisService } from './redis.service';
import Redis from 'ioredis';

@Injectable()
export class PubSubService {
  private subscriber: Redis;
  private publisher: Redis;

  constructor(private redisService: RedisService) {
    // PubSub requires dedicated connections in ioredis
    this.publisher = this.redisService.getClient().duplicate();
    this.subscriber = this.redisService.getClient().duplicate();
  }

  async publish(channel: string, message: string) {
    return this.publisher.publish(channel, message);
  }

  async subscribe(channel: string, callback: (message: string) => void) {
    await this.subscriber.subscribe(channel);
    this.subscriber.on('message', (chan, msg) => {
      if (chan === channel) {
        callback(msg);
      }
    });
  }
}
"""
with open(os.path.join(base_dir, "pubsub.service.ts"), "w", encoding="utf-8") as f: f.write(pubsub_svc)


# 5. Module & Index
redis_mod = """import { Module, Global } from '@nestjs/common';
import { RedisService } from './redis.service';
import { CacheService } from './cache.service';
import { LockService } from './lock.service';
import { PubSubService } from './pubsub.service';

@Global()
@Module({
  providers: [RedisService, CacheService, LockService, PubSubService],
  exports: [CacheService, LockService, PubSubService], // RedisService kept internal mostly
})
export class RedisModule {}
"""
with open(os.path.join(base_dir, "redis.module.ts"), "w", encoding="utf-8") as f: f.write(redis_mod)

index_ts = """export * from './redis.module';
export * from './cache.service';
export * from './lock.service';
export * from './pubsub.service';
export * from './constants/keys';
"""
with open(os.path.join(base_dir, "index.ts"), "w", encoding="utf-8") as f: f.write(index_ts)


print("Redis Package Phase 2 Scaffolded (Services and Module)")
