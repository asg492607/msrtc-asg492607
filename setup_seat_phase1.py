import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\seat-service"
src_dir = os.path.join(base_dir, "src")

# Ensure package.json has ioredis
pkg_json = """{
  "name": "seat-service",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "build": "nest build",
    "start": "nest start",
    "start:dev": "nest start --watch"
  },
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/swagger": "^7.0.0",
    "@msrtc/database": "workspace:*",
    "ioredis": "^5.3.2",
    "class-validator": "^0.14.0",
    "class-transformer": "^0.5.1"
  }
}
"""
with open(os.path.join(base_dir, "package.json"), "w") as f: f.write(pkg_json)


dirs = [
    "common/filters",
    "common/guards",
    "seat/dto",
    "seat/repository",
    "redis",
    "prisma"
]

for d in dirs:
    os.makedirs(os.path.join(src_dir, d), exist_ok=True)

# 1. Prisma Service
prisma_service = """import { Injectable, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }
}
"""
with open(os.path.join(src_dir, "prisma/prisma.service.ts"), "w") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(src_dir, "prisma/prisma.module.ts"), "w") as f: f.write(prisma_module)


# 2. Redis Service (Distributed Locks)
redis_service = """import { Injectable, OnModuleDestroy } from '@nestjs/common';
import Redis from 'ioredis';

@Injectable()
export class RedisService implements OnModuleDestroy {
  private readonly client: Redis;

  constructor() {
    // In production, use env variables for Redis host/port
    this.client = new Redis({ host: 'localhost', port: 6379, maxRetriesPerRequest: null });
  }

  onModuleDestroy() {
    this.client.disconnect();
  }

  /**
   * Acquires a lock for a specific seat on a specific trip.
   * @param tripId The trip instance ID
   * @param seatNo The seat number (e.g., '1A')
   * @param ttlSeconds Time to live in seconds (e.g., 600 for 10 minutes)
   * @param userId The ID of the user acquiring the lock
   * @returns boolean True if lock acquired successfully, false if already locked
   */
  async lockSeat(tripId: string, seatNo: string, ttlSeconds: number, userId: string): Promise<boolean> {
    const key = `lock:trip:${tripId}:seat:${seatNo}`;
    // SETNX (Set if Not eXists) with EX (Expire in seconds)
    const result = await this.client.set(key, userId, 'EX', ttlSeconds, 'NX');
    return result === 'OK';
  }

  /**
   * Releases a lock for a specific seat on a specific trip.
   * @param tripId The trip instance ID
   * @param seatNo The seat number
   */
  async releaseSeat(tripId: string, seatNo: string): Promise<void> {
    const key = `lock:trip:${tripId}:seat:${seatNo}`;
    await this.client.del(key);
  }

  /**
   * Checks if a seat is currently locked in Redis.
   */
  async isSeatLocked(tripId: string, seatNo: string): Promise<boolean> {
    const key = `lock:trip:${tripId}:seat:${seatNo}`;
    const exists = await this.client.exists(key);
    return exists === 1;
  }
}
"""
with open(os.path.join(src_dir, "redis/redis.service.ts"), "w") as f: f.write(redis_service)

redis_module = """import { Global, Module } from '@nestjs/common';
import { RedisService } from './redis.service';

@Global()
@Module({
  providers: [RedisService],
  exports: [RedisService],
})
export class RedisModule {}
"""
with open(os.path.join(src_dir, "redis/redis.module.ts"), "w") as f: f.write(redis_module)

# 3. DTOs
lock_seat_dto = """import { IsString, IsNotEmpty, IsArray, ArrayMinSize, IsUUID } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class LockSeatDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  tripInstanceId: string;

  @ApiProperty({ type: [String], example: ['1A', '1B'] })
  @IsArray()
  @IsString({ each: true })
  @ArrayMinSize(1)
  seatNumbers: string[];
}
"""
with open(os.path.join(src_dir, "seat/dto/lock-seat.dto.ts"), "w") as f: f.write(lock_seat_dto)


# 4. Exception Filter (Ported from booking)
http_exception_filter = """import { ExceptionFilter, Catch, ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { Request, Response } from 'express';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    const message = 
      exception instanceof HttpException
        ? exception.getResponse()
        : 'Internal server error';

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message: typeof message === 'string' ? message : (message as any).message || message,
    });
  }
}
"""
with open(os.path.join(src_dir, "common/filters/http-exception.filter.ts"), "w") as f: f.write(http_exception_filter)


# 5. JWT Guard (Mocked)
jwt_guard = """import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers.authorization;
    if (!authHeader) {
      throw new UnauthorizedException('Missing authorization header');
    }
    request.user = { userId: '123e4567-e89b-12d3-a456-426614174000', roles: ['Passenger'] };
    return true;
  }
}
"""
with open(os.path.join(src_dir, "common/guards/jwt-auth.guard.ts"), "w") as f: f.write(jwt_guard)


print("Seat Service Phase 1 Scaffolded (Redis, Prisma, DTOs)")
