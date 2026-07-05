import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
audit_dir = os.path.join(base_dir, "backend/apps/audit-service")
audit_src = os.path.join(audit_dir, "src")

# 1. Update schema.prisma
schema_path = os.path.join(base_dir, "packages/database/prisma/schema.prisma")
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        schema_content = f.read()
    
    # Check if Audit models already exist
    if "model AuditRecord" not in schema_content:
        audit_models = """
model AuditRecord {
  id            String   @id @default(uuid())
  timestamp     DateTime @default(now())
  userId        String?
  role          String?
  service       String
  entityType    String
  entityId      String
  operation     String
  oldValues     Json?
  newValues     Json?
  correlationId String?
  ipAddress     String?
  status        String   @default("SUCCESS")
  previousHash  String?
  hash          String   @unique
}

model ComplianceRequest {
  id            String   @id @default(uuid())
  type          String   // EXPORT, DELETION
  targetUserId  String
  status        String   @default("PENDING") // PENDING, PROCESSING, COMPLETED, FAILED
  requestedBy   String
  fileId        String?  // Reference to export archive if applicable
  createdAt     DateTime @default(now())
  completedAt   DateTime?
}
"""
        schema_content += audit_models
        with open(schema_path, "w") as f:
            f.write(schema_content)

os.makedirs(audit_dir, exist_ok=True)
os.makedirs(audit_src, exist_ok=True)

# 2. Package.json
pkg_json = {
  "name": "audit-service",
  "version": "1.0.0",
  "private": True,
  "scripts": {
    "build": "nest build",
    "start": "nest start",
    "start:dev": "nest start --watch"
  },
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@msrtc/database": "workspace:*",
    "@msrtc/kafka": "workspace:*",
    "crypto": "^1.0.1"
  },
  "devDependencies": {
    "typescript": "^5.1.3",
    "@types/node": "^20.0.0"
  }
}

with open(os.path.join(audit_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)


# 3. Directories
dirs = [
    "audit/controllers",
    "audit/services",
    "audit/dto",
    "prisma",
    "common/guards",
    "common/filters"
]
for d in dirs:
    os.makedirs(os.path.join(audit_src, d), exist_ok=True)

# 4. Prisma Service
prisma_service = """import { Injectable, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }
}
"""
with open(os.path.join(audit_src, "prisma/prisma.service.ts"), "w", encoding="utf-8") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(audit_src, "prisma/prisma.module.ts"), "w", encoding="utf-8") as f: f.write(prisma_module)


print("Audit Service Phase 1 Scaffolded (Schema, Package)")
