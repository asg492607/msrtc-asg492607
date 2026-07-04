import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\gps-service\src"

# 1. Repository
gps_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class GpsRepository {
  constructor(private prisma: PrismaService) {}

  async savePingHistory(vehicleId: string, tripInstanceId: string, lat: number, lng: number, speed?: number) {
    // Note: In a real system, we'd batch these writes to avoid killing the DB
    return this.prisma.vehicleLocation.create({
      data: {
        vehicleId,
        tripInstanceId,
        latitude: lat,
        longitude: lng,
        speed,
        timestamp: new Date()
      }
    });
  }
}
"""
with open(os.path.join(base_dir, "gps/repository/gps.repository.ts"), "w") as f: f.write(gps_repo)


# 2. ETA Service
eta_svc = """import { Injectable } from '@nestjs/common';

@Injectable()
export class EtaService {
  /**
   * Mock calculation of distance/delay based on current coordinates.
   */
  calculateDelay(lat: number, lng: number, expectedLat: number, expectedLng: number): number {
    // Return delay in minutes
    return 5;
  }
}
"""
with open(os.path.join(base_dir, "gps/eta.service.ts"), "w") as f: f.write(eta_svc)


# 3. Live Tracking Gateway (Socket.io)
ws_gateway = """import { 
  WebSocketGateway, 
  WebSocketServer, 
  SubscribeMessage, 
  MessageBody, 
  ConnectedSocket 
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({ cors: true, namespace: '/live-tracking' })
export class LiveTrackingGateway {
  @WebSocketServer()
  server: Server;

  /**
   * Passengers subscribe to a specific trip ID to get live location updates.
   */
  @SubscribeMessage('subscribe_trip')
  handleSubscribe(@MessageBody('tripId') tripId: string, @ConnectedSocket() client: Socket) {
    const room = `trip_${tripId}`;
    client.join(room);
    return { event: 'subscribed', room };
  }

  /**
   * Called by the internal GpsService when a new ping is processed.
   */
  broadcastLocation(tripId: string, payload: any) {
    this.server.to(`trip_${tripId}`).emit('location_update', payload);
  }
}
"""
with open(os.path.join(base_dir, "gps/live-tracking.gateway.ts"), "w") as f: f.write(ws_gateway)


# 4. GPS Service
gps_svc = """import { Injectable } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "gps/gps.service.ts"), "w") as f: f.write(gps_svc)


# 5. Controllers
gps_ctrl = """import { Controller, Post, Get, Body, Param, UseGuards } from '@nestjs/common';
import { GpsService } from './gps.service';
import { GpsPingDto } from './dto/gps.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('GPS Ingestion')
@Controller('gps')
export class GpsController {
  constructor(private readonly gpsService: GpsService) {}

  @Post('ping')
  @ApiOperation({ summary: 'Receive GPS ping from vehicle IoT device or conductor app' })
  async receivePing(@Body() dto: GpsPingDto) {
    return this.gpsService.processPing(dto);
  }

  @Get('vehicle/:id/current')
  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  @ApiOperation({ summary: 'Get the last known location of a vehicle (reads from Redis)' })
  async getCurrentLocation(@Param('id') vehicleId: string) {
    return this.gpsService.getLastKnownLocation(vehicleId);
  }
}
"""
with open(os.path.join(base_dir, "gps/gps.controller.ts"), "w") as f: f.write(gps_ctrl)


# 6. Modules
gps_mod = """import { Module } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "gps/gps.module.ts"), "w") as f: f.write(gps_mod)

app_module = """import { Module } from '@nestjs/common';
import { GpsModule } from './gps/gps.module';

@Module({
  imports: [GpsModule],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w") as f: f.write(app_module)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AllExceptionsFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.useGlobalFilters(new AllExceptionsFilter());
  
  app.setGlobalPrefix('api/v1');

  const config = new DocumentBuilder()
    .setTitle('MSRTC GPS & Live Operations Service')
    .setDescription('Real-time location ingestion and WebSocket broadcasting')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/gps', app, document);

  await app.listen(3009);
  console.log('GPS Service is running on http://localhost:3009');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w") as f: f.write(main_ts)


print("GPS Service Phase 2 Scaffolded (Redis caching, WebSockets, Prisma history)")
