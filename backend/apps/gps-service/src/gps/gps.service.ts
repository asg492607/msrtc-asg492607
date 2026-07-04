import { Injectable } from '@nestjs/common';
import { GpsRepository } from './repository/gps.repository';
import { RedisService } from '../redis/redis.service';
import { LiveTrackingGateway } from './live-tracking.gateway';
import { EtaService } from './eta.service';
import { GpsPingDto } from './dto/gps.dto';

@Injectable()
export class GpsService {
  constructor(
    private readonly repository: GpsRepository,
    private readonly redis: RedisService,
    private readonly gateway: LiveTrackingGateway,
    private readonly etaService: EtaService
  ) {}

  async processPing(dto: GpsPingDto) {
    // 1. Write to Redis (ultra-fast access for "current location" queries)
    const redisKey = `vehicle_loc:${dto.vehicleId}`;
    await this.redis.client.set(redisKey, JSON.stringify(dto), 'EX', 3600); // Expire after 1 hr of inactivity

    // 2. Broadcast via WebSockets to any passenger watching the map
    this.gateway.broadcastLocation(dto.tripInstanceId, {
      lat: dto.latitude,
      lng: dto.longitude,
      speed: dto.speed,
      timestamp: new Date().toISOString()
    });

    // 3. Persist historical trail asynchronously (fire and forget)
    this.repository.savePingHistory(dto.vehicleId, dto.tripInstanceId, dto.latitude, dto.longitude, dto.speed).catch(console.error);

    // 4. Run ETA/Delay detection
    // this.etaService.calculateDelay(...)

    return { processed: true };
  }

  async getLastKnownLocation(vehicleId: string) {
    const data = await this.redis.client.get(`vehicle_loc:${vehicleId}`);
    return data ? JSON.parse(data) : null;
  }
}
