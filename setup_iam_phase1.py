import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
auth_dir = os.path.join(base_dir, "backend/apps/auth-service")
auth_src = os.path.join(auth_dir, "src/auth")

# 1. Update schema.prisma
schema_path = os.path.join(base_dir, "packages/database/prisma/schema.prisma")
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        schema_content = f.read()
    
    # Check if IAM models already exist to avoid duplication
    if "model Session" not in schema_content:
        iam_models = """
model Session {
  id           String   @id @default(uuid())
  userId       String
  refreshToken String   @unique
  deviceInfo   String?
  ipAddress    String?
  expiresAt    DateTime
  createdAt    DateTime @default(now())
  user         User     @relation(fields: [userId], references: [id])
}

model ApiKey {
  id          String   @id @default(uuid())
  keyHash     String   @unique
  name        String
  serviceName String?
  createdAt   DateTime @default(now())
  expiresAt   DateTime?
  isActive    Boolean  @default(true)
}

model IamAuditLog {
  id          String   @id @default(uuid())
  userId      String?
  action      String
  status      String
  ipAddress   String?
  metadata    Json?
  createdAt   DateTime @default(now())
}
"""
        schema_content += iam_models
        
        if "model User {" in schema_content and "sessions Session[]" not in schema_content:
            schema_content = schema_content.replace(
                "model User {",
                "model User {\\n  mfaEnabled      Boolean  @default(false)\\n  mfaSecret       String?\\n  failedAttempts  Int      @default(0)\\n  lockoutUntil    DateTime?\\n  sessions        Session[]"
            )

        with open(schema_path, "w") as f:
            f.write(schema_content)


# 2. Add dependencies to auth-service
pkg_path = os.path.join(auth_dir, "package.json")
if os.path.exists(pkg_path):
    with open(pkg_path, "r") as f:
        pkg = json.load(f)
    
    if 'dependencies' not in pkg:
        pkg['dependencies'] = {}
    pkg['dependencies']['otplib'] = "^12.0.1"
    pkg['dependencies']['qrcode'] = "^1.5.3"
    
    if 'devDependencies' not in pkg:
        pkg['devDependencies'] = {}
    pkg['devDependencies']['@types/qrcode'] = "^1.5.0"
    
    with open(pkg_path, "w") as f:
        json.dump(pkg, f, indent=2)


# 3. Create Controllers and Services structure
dirs = [
    "mfa",
    "session",
    "apikey",
    "audit"
]

for d in dirs:
    os.makedirs(os.path.join(auth_src, d), exist_ok=True)


# MFA Service
mfa_svc = """import { Injectable } from '@nestjs/common';
import { authenticator } from 'otplib';
import * as qrcode from 'qrcode';

@Injectable()
export class MfaService {
  async generateMfaSecret(email: string) {
    const secret = authenticator.generateSecret();
    const otpauthUrl = authenticator.keyuri(email, 'MSRTC Enterprise', secret);
    const qrCodeDataUrl = await qrcode.toDataURL(otpauthUrl);
    
    return { secret, qrCodeDataUrl };
  }

  verifyMfaToken(token: string, secret: string): boolean {
    return authenticator.verify({ token, secret });
  }
}
"""
with open(os.path.join(auth_src, "mfa/mfa.service.ts"), "w", encoding="utf-8") as f: f.write(mfa_svc)


# Session Service
session_svc = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class SessionService {
  constructor(private prisma: PrismaService) {}

  async createSession(userId: string, refreshToken: string, deviceInfo: string, ipAddress: string) {
    return this.prisma.session.create({
      data: {
        userId,
        refreshToken,
        deviceInfo,
        ipAddress,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
      }
    });
  }

  async revokeSession(sessionId: string) {
    return this.prisma.session.delete({ where: { id: sessionId } });
  }

  async revokeAllUserSessions(userId: string) {
    return this.prisma.session.deleteMany({ where: { userId } });
  }

  async getActiveSessions(userId: string) {
    return this.prisma.session.findMany({ where: { userId } });
  }
}
"""
with open(os.path.join(auth_src, "session/session.service.ts"), "w", encoding="utf-8") as f: f.write(session_svc)


print("IAM Phase 1 Scaffolded (Schema, MFA, Session Services)")
