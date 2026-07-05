import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\auth-service\src\auth"

# 1. ApiKey Service
apikey_svc = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import * as crypto from 'crypto';

@Injectable()
export class ApiKeyService {
  constructor(private prisma: PrismaService) {}

  async generateApiKey(name: string, serviceName?: string) {
    const rawKey = crypto.randomBytes(32).toString('hex');
    const keyHash = crypto.createHash('sha256').update(rawKey).digest('hex');

    const apiKey = await this.prisma.apiKey.create({
      data: { name, serviceName, keyHash }
    });

    return { apiKeyId: apiKey.id, rawKey }; // rawKey is only shown once
  }

  async validateApiKey(rawKey: string): Promise<boolean> {
    const keyHash = crypto.createHash('sha256').update(rawKey).digest('hex');
    const key = await this.prisma.apiKey.findUnique({ where: { keyHash } });
    return key ? key.isActive : false;
  }
}
"""
with open(os.path.join(base_dir, "apikey/apikey.service.ts"), "w", encoding="utf-8") as f: f.write(apikey_svc)


# 2. Audit Service
audit_svc = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class AuditService {
  constructor(private prisma: PrismaService) {}

  async logAction(userId: string, action: string, status: string, ipAddress?: string, metadata?: any) {
    return this.prisma.iamAuditLog.create({
      data: { userId, action, status, ipAddress, metadata }
    });
  }
}
"""
with open(os.path.join(base_dir, "audit/audit.service.ts"), "w", encoding="utf-8") as f: f.write(audit_svc)


# 3. Controllers
mfa_ctrl = """import { Controller, Post, Body, UseGuards, Request } from '@nestjs/common';
import { MfaService } from './mfa.service';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('IAM MFA')
@Controller('iam/mfa')
export class MfaController {
  constructor(private mfaService: MfaService) {}

  @Post('setup')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Setup TOTP MFA for user' })
  async setupMfa(@Request() req) {
    // req.user contains userId and email from JWT
    const email = req.user.email || 'user@msrtc.gov.in'; 
    return this.mfaService.generateMfaSecret(email);
  }

  @Post('verify')
  @ApiOperation({ summary: 'Verify TOTP code' })
  async verifyMfa(@Body('token') token: string, @Body('secret') secret: string) {
    const isValid = this.mfaService.verifyMfaToken(token, secret);
    return { valid: isValid };
  }
}
"""
with open(os.path.join(base_dir, "mfa/mfa.controller.ts"), "w", encoding="utf-8") as f: f.write(mfa_ctrl)


session_ctrl = """import { Controller, Get, Delete, Param, UseGuards, Request } from '@nestjs/common';
import { SessionService } from './session.service';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('IAM Sessions')
@Controller('iam/sessions')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class SessionController {
  constructor(private sessionService: SessionService) {}

  @Get()
  @ApiOperation({ summary: 'Get active sessions for user' })
  async getSessions(@Request() req) {
    return this.sessionService.getActiveSessions(req.user.userId);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Revoke a specific session' })
  async revokeSession(@Param('id') id: string) {
    await this.sessionService.revokeSession(id);
    return { success: true };
  }
}
"""
with open(os.path.join(base_dir, "session/session.controller.ts"), "w", encoding="utf-8") as f: f.write(session_ctrl)


print("IAM Phase 2 Scaffolded (ApiKey, Audit, Controllers)")
