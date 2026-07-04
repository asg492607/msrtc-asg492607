import { Module } from '@nestjs/common';
import { GpsController } from './gps.controller';
import { GpsService } from './gps.service';
import { EtaService } from './eta.service';
import { LiveTrackingGateway } from './live-tracking.gateway';
import { GpsRepository } from './repository/gps.repository';
import { PrismaModule } from '../prisma/prisma.module';
import { RedisModule } from '../redis/redis.module';

@Module({
  imports: [PrismaModule, RedisModule],
  controllers: [GpsController],
  providers: [GpsService, EtaService, LiveTrackingGateway, GpsRepository],
})
export class GpsModule {}
