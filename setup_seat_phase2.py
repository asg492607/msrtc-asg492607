import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\seat-service\src"

# 1. Seat Repository
seat_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class SeatRepository {
  constructor(private prisma: PrismaService) {}

  /**
   * Checks if a seat is permanently booked in PostgreSQL.
   */
  async isSeatPermanentlyBooked(tripId: string, seatNo: string): Promise<boolean> {
    const bookingPassenger = await this.prisma.bookingPassenger.findFirst({
      where: {
        seatNo: seatNo,
        booking: {
          tripInstanceId: tripId,
          status: { in: ['CONFIRMED', 'COMPLETED'] }
        }
      }
    });
    return !!bookingPassenger;
  }
}
"""
with open(os.path.join(base_dir, "seat/repository/seat.repository.ts"), "w") as f: f.write(seat_repo)


# 2. Seat Service
seat_svc = """import { Injectable, ConflictException, BadRequestException } from '@nestjs/common';
import { SeatRepository } from './repository/seat.repository';
import { RedisService } from '../redis/redis.service';
import { LockSeatDto } from './dto/lock-seat.dto';

@Injectable()
export class SeatService {
  constructor(
    private readonly repository: SeatRepository,
    private readonly redis: RedisService
  ) {}

  /**
   * Attempts to lock seats concurrently via Redis.
   */
  async lockSeats(userId: string, dto: LockSeatDto) {
    const lockedSeats: string[] = [];
    const TTL_SECONDS = 600; // 10 minutes to complete booking & payment

    try {
      for (const seatNo of dto.seatNumbers) {
        // 1. Check if permanently booked in Postgres
        const isPermanentlyBooked = await this.repository.isSeatPermanentlyBooked(dto.tripInstanceId, seatNo);
        if (isPermanentlyBooked) {
          throw new ConflictException(`Seat ${seatNo} is already booked.`);
        }

        // 2. Attempt to acquire Redis Lock
        const lockAcquired = await this.redis.lockSeat(dto.tripInstanceId, seatNo, TTL_SECONDS, userId);
        if (!lockAcquired) {
          throw new ConflictException(`Seat ${seatNo} is currently reserved by another user.`);
        }
        
        lockedSeats.push(seatNo);
      }

      return {
        message: 'Seats locked successfully for 10 minutes.',
        tripInstanceId: dto.tripInstanceId,
        lockedSeats,
        expiresIn: TTL_SECONDS
      };

    } catch (error) {
      // Rollback: Release any seats we managed to lock before the failure occurred
      for (const seatNo of lockedSeats) {
        await this.redis.releaseSeat(dto.tripInstanceId, seatNo);
      }
      throw error;
    }
  }

  /**
   * Releases seats manually (e.g. if passenger cancels booking before payment).
   */
  async releaseSeats(userId: string, dto: LockSeatDto) {
    for (const seatNo of dto.seatNumbers) {
      // In a real system, we'd verify the user owns the lock before releasing it
      await this.redis.releaseSeat(dto.tripInstanceId, seatNo);
    }
    return { message: 'Seats released successfully.' };
  }
}
"""
with open(os.path.join(base_dir, "seat/seat.service.ts"), "w") as f: f.write(seat_svc)


# 3. Seat Controller
seat_ctrl = """import { Controller, Post, Body, UseGuards, Request } from '@nestjs/common';
import { SeatService } from './seat.service';
import { LockSeatDto } from './dto/lock-seat.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Seats')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('seats')
export class SeatController {
  constructor(private readonly seatService: SeatService) {}

  @Post('lock')
  @ApiOperation({ summary: 'Lock seats temporarily in Redis for a booking session' })
  async lockSeats(@Request() req, @Body() dto: LockSeatDto) {
    return this.seatService.lockSeats(req.user.userId, dto);
  }

  @Post('release')
  @ApiOperation({ summary: 'Manually release held seats' })
  async releaseSeats(@Request() req, @Body() dto: LockSeatDto) {
    return this.seatService.releaseSeats(req.user.userId, dto);
  }
}
"""
with open(os.path.join(base_dir, "seat/seat.controller.ts"), "w") as f: f.write(seat_ctrl)


# 4. Seat Module
seat_mod = """import { Module } from '@nestjs/common';
import { SeatController } from './seat.controller';
import { SeatService } from './seat.service';
import { SeatRepository } from './repository/seat.repository';
import { PrismaModule } from '../prisma/prisma.module';
import { RedisModule } from '../redis/redis.module';

@Module({
  imports: [PrismaModule, RedisModule],
  controllers: [SeatController],
  providers: [SeatService, SeatRepository],
})
export class SeatModule {}
"""
with open(os.path.join(base_dir, "seat/seat.module.ts"), "w") as f: f.write(seat_mod)


# 5. Main.ts update
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
    .setTitle('MSRTC Seat Service')
    .setDescription('High-concurrency Redis Seat Locking API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/seat', app, document);

  await app.listen(3006);
  console.log('Seat Service is running on http://localhost:3006');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w") as f: f.write(main_ts)

print("Seat Service Phase 2 Scaffolded (Service, Controller, Repo)")
