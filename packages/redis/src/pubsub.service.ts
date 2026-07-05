import { Injectable } from '@nestjs/common';
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
