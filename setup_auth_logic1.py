import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\auth-service\src"

# 1. Prisma Module & Service
prisma_service = """import { Injectable, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }
}
"""
with open(os.path.join(base_dir, "prisma/prisma.service.ts"), "w") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(base_dir, "prisma/prisma.module.ts"), "w") as f: f.write(prisma_module)


# 2. DTOs
login_dto = """import { IsEmail, IsNotEmpty, IsString, MinLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class LoginDto {
  @ApiProperty({ example: 'passenger@msrtc.gov.in' })
  @IsEmail()
  @IsNotEmpty()
  email: string;

  @ApiProperty({ example: 'password123' })
  @IsString()
  @MinLength(6)
  password: string;
}
"""
with open(os.path.join(base_dir, "auth/dto/login.dto.ts"), "w") as f: f.write(login_dto)

signup_dto = """import { IsEmail, IsNotEmpty, IsString, MinLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class SignupDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  firstName: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  lastName: string;

  @ApiProperty()
  @IsEmail()
  email: string;

  @ApiProperty()
  @IsString()
  @MinLength(6)
  password: string;
}
"""
with open(os.path.join(base_dir, "auth/dto/signup.dto.ts"), "w") as f: f.write(signup_dto)


# 3. Guards and Decorators
jwt_guard = """import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}
"""
with open(os.path.join(base_dir, "auth/guards/jwt-auth.guard.ts"), "w") as f: f.write(jwt_guard)

roles_decorator = """import { SetMetadata } from '@nestjs/common';
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);
"""
with open(os.path.join(base_dir, "auth/decorators/roles.decorator.ts"), "w") as f: f.write(roles_decorator)

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
with open(os.path.join(base_dir, "auth/guards/roles.guard.ts"), "w") as f: f.write(roles_guard)


# 4. Strategy
jwt_strategy = """import { ExtractJwt, Strategy } from 'passport-jwt';
import { PassportStrategy } from '@nestjs/passport';
import { Injectable } from '@nestjs/common';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: 'MSRTC_SUPER_SECRET_KEY_PROD', // In prod, use process.env.JWT_SECRET
    });
  }

  async validate(payload: any) {
    return { userId: payload.sub, email: payload.email, roles: payload.roles };
  }
}
"""
with open(os.path.join(base_dir, "auth/strategies/jwt.strategy.ts"), "w") as f: f.write(jwt_strategy)

print("DTOs, Guards, Strategies generated.")
