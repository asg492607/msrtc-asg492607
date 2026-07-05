import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\depot-service"
src_dir = os.path.join(base_dir, "src")

# Ensure package.json has validation
pkg_json = """{
  "name": "depot-service",
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
    "class-validator": "^0.14.0",
    "class-transformer": "^0.5.1"
  }
}
"""
with open(os.path.join(base_dir, "package.json"), "w", encoding="utf-8") as f: f.write(pkg_json)


dirs = [
    "common/filters",
    "common/guards",
    "common/decorators",
    "depot/dto",
    "depot/enums",
    "depot/repository",
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
with open(os.path.join(src_dir, "prisma/prisma.service.ts"), "w", encoding="utf-8") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(src_dir, "prisma/prisma.module.ts"), "w", encoding="utf-8") as f: f.write(prisma_module)


# 2. Enums
enums_ts = """export enum VehicleStatus {
  AVAILABLE = 'AVAILABLE',
  CREW_ASSIGNED = 'CREW_ASSIGNED',
  PLATFORM_ASSIGNED = 'PLATFORM_ASSIGNED',
  READY_FOR_DISPATCH = 'READY_FOR_DISPATCH',
  DISPATCHED = 'DISPATCHED',
  RUNNING = 'RUNNING',
  ARRIVED = 'ARRIVED',
  PARKED = 'PARKED',
  UNDER_MAINTENANCE = 'UNDER_MAINTENANCE',
}

export enum PlatformStatus {
  EMPTY = 'EMPTY',
  OCCUPIED = 'OCCUPIED',
  RESERVED = 'RESERVED',
}
"""
with open(os.path.join(src_dir, "depot/enums/depot.enums.ts"), "w", encoding="utf-8") as f: f.write(enums_ts)


# 3. DTOs
dto_ts = """import { IsString, IsNotEmpty, IsUUID, IsNumber } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateDepotDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  name: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  location: string;
}

export class AddBusDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  registrationNumber: string;

  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  depotId: string;
}

export class DispatchBusDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  busId: string;

  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  tripInstanceId: string;

  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  crewAssignmentId: string; // To verify crew check-in
}

export class AssignPlatformDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  busId: string;

  @ApiProperty()
  @IsNumber()
  @IsNotEmpty()
  platformNumber: number;
}
"""
with open(os.path.join(src_dir, "depot/dto/depot.dto.ts"), "w", encoding="utf-8") as f: f.write(dto_ts)


# 4. Exception Filter & Guards (Ported)
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
with open(os.path.join(src_dir, "common/filters/http-exception.filter.ts"), "w", encoding="utf-8") as f: f.write(http_exception_filter)

jwt_guard = """import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers.authorization;
    if (!authHeader) {
      throw new UnauthorizedException('Missing authorization header');
    }
    // Mock user decoding
    request.user = { userId: '123e4567-e89b-12d3-a456-426614174000', roles: ['Dispatcher', 'Depot_Manager', 'HQ_Admin'] };
    return true;
  }
}
"""
with open(os.path.join(src_dir, "common/guards/jwt-auth.guard.ts"), "w", encoding="utf-8") as f: f.write(jwt_guard)

roles_decorator = """import { SetMetadata } from '@nestjs/common';
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);
"""
with open(os.path.join(src_dir, "common/decorators/roles.decorator.ts"), "w", encoding="utf-8") as f: f.write(roles_decorator)

roles_guard = """import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.get<string[]>('roles', context.getHandler());
    if (!roles) {
      return true;
    }
    const request = context.switchToHttp().getRequest();
    const user = request.user;
    
    if (!user || !user.roles) return false;
    return roles.some((role) => user.roles.includes(role));
  }
}
"""
with open(os.path.join(src_dir, "common/guards/roles.guard.ts"), "w", encoding="utf-8") as f: f.write(roles_guard)


print("Depot Service Phase 1 Scaffolded (DTOs, Enums, Guards, Prisma)")
