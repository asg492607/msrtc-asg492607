import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\route-service\src"

# 1. Trip Repository
trip_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { SearchTripsDto } from '../dto/search-trips.dto';

@Injectable()
export class TripRepository {
  constructor(private prisma: PrismaService) {}

  /**
   * Complex query to find trips running on a specific date 
   * where the route includes both source and destination stations in the correct order.
   */
  async searchTrips(dto: SearchTripsDto) {
    // In a real implementation, this would involve joining Route, RouteStop, TripInstance, and Schedule.
    // We mock the structure returned from Prisma for the reference architecture.
    
    // Example Prisma Query Structure:
    /*
    return this.prisma.tripInstance.findMany({
      where: {
        date: new Date(dto.travelDate),
        schedule: {
          route: {
            stops: {
              some: { stationId: dto.sourceStationId },
              // Needs advanced raw query or careful ordering logic in Prisma to ensure source is BEFORE destination
            }
          }
        },
        status: 'SCHEDULED'
      },
      include: {
        bus: true,
        schedule: { include: { route: true } }
      }
    });
    */

    return [
      {
        id: 'trip-123',
        departureTime: '2026-07-05T08:00:00Z',
        arrivalTime: '2026-07-05T14:30:00Z',
        busType: 'Shivneri (AC Volvo)',
        availableSeats: 32,
        baseFare: 450,
      },
      {
        id: 'trip-124',
        departureTime: '2026-07-05T10:00:00Z',
        arrivalTime: '2026-07-05T17:15:00Z',
        busType: 'Hirkani (Non-AC Seater)',
        availableSeats: 12,
        baseFare: 220,
      }
    ];
  }
}
"""
with open(os.path.join(base_dir, "trip/repository/trip.repository.ts"), "w") as f: f.write(trip_repo)


# 2. Trip Service
trip_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
import { TripRepository } from './repository/trip.repository';
import { SearchTripsDto } from './dto/search-trips.dto';

@Injectable()
export class TripService {
  constructor(private readonly repository: TripRepository) {}

  /**
   * Executes the search engine logic.
   */
  async searchAvailableTrips(dto: SearchTripsDto) {
    const travelDate = new Date(dto.travelDate);
    if (travelDate < new Date(new Date().setHours(0,0,0,0))) {
      throw new BadRequestException('Travel date cannot be in the past');
    }

    if (dto.sourceStationId === dto.destinationStationId) {
      throw new BadRequestException('Source and destination cannot be the same');
    }

    const trips = await this.repository.searchTrips(dto);
    
    return {
      message: 'Trips found successfully',
      date: dto.travelDate,
      count: trips.length,
      trips
    };
  }
}
"""
with open(os.path.join(base_dir, "trip/trip.service.ts"), "w") as f: f.write(trip_svc)


# 3. Trip Controller
trip_ctrl = """import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { TripService } from './trip.service';
import { SearchTripsDto } from './dto/search-trips.dto';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';

@ApiTags('Trips (Search Engine)')
@Controller('trips')
export class TripController {
  constructor(private readonly tripService: TripService) {}

  @Get('search')
  @ApiOperation({ summary: 'Search for available buses between two stations on a given date' })
  @ApiResponse({ status: 200, description: 'List of available trips with fares and timings.' })
  async searchTrips(@Query() dto: SearchTripsDto) {
    return this.tripService.searchAvailableTrips(dto);
  }
}
"""
with open(os.path.join(base_dir, "trip/trip.controller.ts"), "w") as f: f.write(trip_ctrl)


# 4. Trip Module
trip_mod = """import { Module } from '@nestjs/common';
import { TripController } from './trip.controller';
import { TripService } from './trip.service';
import { TripRepository } from './repository/trip.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [TripController],
  providers: [TripService, TripRepository],
})
export class TripModule {}
"""
with open(os.path.join(base_dir, "trip/trip.module.ts"), "w") as f: f.write(trip_mod)


# 5. Main.ts & AppModule update
app_module = """import { Module } from '@nestjs/common';
import { TripModule } from './trip/trip.module';

@Module({
  imports: [TripModule],
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
    .setTitle('MSRTC Route & Schedule Service')
    .setDescription('Core Search Engine and Trip Management API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/route', app, document);

  await app.listen(3004);
  console.log('Route & Schedule Service is running on http://localhost:3004');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w") as f: f.write(main_ts)

print("Route Service Phase 2 Scaffolded (Trip Search Engine, Repo)")
