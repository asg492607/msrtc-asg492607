import { Module, Global } from '@nestjs/common';
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
