import { Injectable, Logger } from '@nestjs/common';
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
