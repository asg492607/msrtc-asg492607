import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\notification-service"
src_dir = os.path.join(base_dir, "src")

# Ensure package.json has validation
pkg_json = """{
  "name": "notification-service",
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
with open(os.path.join(base_dir, "package.json"), "w") as f: f.write(pkg_json)


dirs = [
    "common/filters",
    "common/guards",
    "common/decorators",
    "notification/dto",
    "notification/enums",
    "notification/repository",
    "providers/interfaces",
    "providers/adapters",
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


# 2. Enums
enums_ts = """export enum NotificationStatus {
  QUEUED = 'QUEUED',
  SENT = 'SENT',
  DELIVERED = 'DELIVERED',
  FAILED = 'FAILED',
}

export enum NotificationChannel {
  SMS = 'SMS',
  EMAIL = 'EMAIL',
  PUSH = 'PUSH',
}
"""
with open(os.path.join(src_dir, "notification/enums/notification.enums.ts"), "w") as f: f.write(enums_ts)


# 3. DTOs
dto_ts = """import { IsString, IsNotEmpty, IsEnum, IsUUID, IsObject, IsOptional, IsArray } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { NotificationChannel } from '../enums/notification.enums';

export class SendNotificationDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  userId: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  templateCode: string;

  @ApiProperty({ enum: [NotificationChannel] })
  @IsArray()
  @IsEnum(NotificationChannel, { each: true })
  channels: NotificationChannel[];

  @ApiProperty()
  @IsObject()
  @IsOptional()
  payload?: Record<string, any>;
}
"""
with open(os.path.join(src_dir, "notification/dto/notification.dto.ts"), "w") as f: f.write(dto_ts)


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
with open(os.path.join(src_dir, "common/filters/http-exception.filter.ts"), "w") as f: f.write(http_exception_filter)

jwt_guard = """import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers.authorization;
    if (!authHeader) {
      throw new UnauthorizedException('Missing authorization header');
    }
    request.user = { userId: '123e4567-e89b-12d3-a456-426614174000', roles: ['Admin', 'System'] };
    return true;
  }
}
"""
with open(os.path.join(src_dir, "common/guards/jwt-auth.guard.ts"), "w") as f: f.write(jwt_guard)

roles_decorator = """import { SetMetadata } from '@nestjs/common';
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);
"""
with open(os.path.join(src_dir, "common/decorators/roles.decorator.ts"), "w") as f: f.write(roles_decorator)

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
with open(os.path.join(src_dir, "common/guards/roles.guard.ts"), "w") as f: f.write(roles_guard)


print("Notification Service Phase 1 Scaffolded (DTOs, Enums, Guards, Prisma)")
