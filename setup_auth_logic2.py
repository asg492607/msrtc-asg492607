import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\auth-service\src"

# 1. Auth Service
auth_service = """import { Injectable, UnauthorizedException, ConflictException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { JwtService } from '@nestjs/jwt';
import * as argon2 from 'argon2';
import { LoginDto } from './dto/login.dto';
import { SignupDto } from './dto/signup.dto';

@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private jwtService: JwtService,
  ) {}

  async signup(dto: SignupDto) {
    const existingUser = await this.prisma.user.findUnique({
      where: { email: dto.email },
    });

    if (existingUser) {
      throw new ConflictException('Email already exists');
    }

    const passwordHash = await argon2.hash(dto.password);

    const user = await this.prisma.user.create({
      data: {
        email: dto.email,
        firstName: dto.firstName,
        lastName: dto.lastName,
        passwordHash,
      },
    });

    return this.generateTokens(user.id, user.email, ['Passenger']);
  }

  async login(dto: LoginDto) {
    const user = await this.prisma.user.findUnique({
      where: { email: dto.email },
      include: { userRoles: { include: { role: true } } },
    });

    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    const passwordMatches = await argon2.verify(user.passwordHash, dto.password);
    if (!passwordMatches) {
      throw new UnauthorizedException('Invalid credentials');
    }
    
    // Default to 'Passenger' if no roles exist in DB yet for this mockup
    const roles = user.userRoles.length > 0 
        ? user.userRoles.map(ur => ur.role.name) 
        : ['Passenger'];

    // Log the history asynchronously
    this.prisma.loginHistory.create({
        data: { userId: user.id, status: 'SUCCESS' }
    }).catch(console.error);

    return this.generateTokens(user.id, user.email, roles);
  }

  private async generateTokens(userId: string, email: string, roles: string[]) {
    const payload = { sub: userId, email, roles };
    
    const accessToken = this.jwtService.sign(payload, { expiresIn: '15m' });
    const refreshToken = this.jwtService.sign(payload, { expiresIn: '7d' });

    // Store refresh token in DB
    await this.prisma.refreshToken.create({
      data: {
        userId,
        token: refreshToken,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    });

    return {
      accessToken,
      refreshToken,
      user: { id: userId, email, roles }
    };
  }
}
"""
with open(os.path.join(base_dir, "auth/auth.service.ts"), "w") as f: f.write(auth_service)

# 2. Auth Controller
auth_controller = """import { Controller, Post, Body, Get, UseGuards, Request } from '@nestjs/common';
import { AuthService } from './auth.service';
import { LoginDto } from './dto/login.dto';
import { SignupDto } from './dto/signup.dto';
import { JwtAuthGuard } from './guards/jwt-auth.guard';
import { RolesGuard } from './guards/roles.guard';
import { Roles } from './decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Authentication')
@Controller()
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('signup')
  @ApiOperation({ summary: 'Register a new passenger account' })
  signup(@Body() dto: SignupDto) {
    return this.authService.signup(dto);
  }

  @Post('login')
  @ApiOperation({ summary: 'Login with email and password' })
  login(@Body() dto: LoginDto) {
    return this.authService.login(dto);
  }

  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  @Get('profile')
  @ApiOperation({ summary: 'Get current logged-in user profile' })
  getProfile(@Request() req) {
    return req.user;
  }

  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('Admin', 'HQ_Officer')
  @Get('admin-only')
  @ApiOperation({ summary: 'Test endpoint restricted to Admin roles' })
  getAdminData() {
    return { message: 'Welcome to the HQ Command Center, Admin!' };
  }
}
"""
with open(os.path.join(base_dir, "auth/auth.controller.ts"), "w") as f: f.write(auth_controller)

# 3. Auth Module
auth_module = """import { Module } from '@nestjs/common';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { JwtStrategy } from './strategies/jwt.strategy';

@Module({
  imports: [
    PassportModule,
    JwtModule.register({
      secret: 'MSRTC_SUPER_SECRET_KEY_PROD', // In prod, use .env
      signOptions: { expiresIn: '15m' },
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy],
})
export class AuthModule {}
"""
with open(os.path.join(base_dir, "auth/auth.module.ts"), "w") as f: f.write(auth_module)

print("Auth Controller, Service, and Module generated.")
