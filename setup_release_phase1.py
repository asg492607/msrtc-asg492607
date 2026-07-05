import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
ff_dir = os.path.join(base_dir, "backend/apps/feature-flag-service")
ff_src = os.path.join(ff_dir, "src")

# 1. Update schema.prisma
schema_path = os.path.join(base_dir, "packages/database/prisma/schema.prisma")
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        schema_content = f.read()
    
    if "model FeatureFlag" not in schema_content:
        ff_models = """
model FeatureFlag {
  id          String   @id @default(uuid())
  key         String   @unique
  description String?
  isEnabled   Boolean  @default(false)
  tenantId    String?  // Null means global, otherwise tenant-specific
  rules       Json?    // Complex targeting (e.g., percentage, region)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model ReleaseTracker {
  id            String   @id @default(uuid())
  serviceName   String
  version       String
  strategy      String   // CANARY, BLUE_GREEN, ROLLING
  status        String   // PROGRESSING, HEALTHY, DEGRADED, ROLLED_BACK
  deploymentId  String?
  startedAt     DateTime @default(now())
  completedAt   DateTime?
}
"""
        schema_content += ff_models
        with open(schema_path, "w") as f:
            f.write(schema_content)

os.makedirs(ff_dir, exist_ok=True)
os.makedirs(ff_src, exist_ok=True)

# 2. Package.json
pkg_json = {
  "name": "feature-flag-service",
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
    "@msrtc/redis": "workspace:*",
    "@msrtc/tenant": "workspace:*"
  },
  "devDependencies": {
    "typescript": "^5.1.3",
    "@types/node": "^20.0.0"
  }
}

with open(os.path.join(ff_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)


# 3. Directories
dirs = [
    "flags/controllers",
    "flags/services",
    "prisma"
]
for d in dirs:
    os.makedirs(os.path.join(ff_src, d), exist_ok=True)

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
with open(os.path.join(ff_src, "prisma/prisma.service.ts"), "w", encoding="utf-8") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(ff_src, "prisma/prisma.module.ts"), "w", encoding="utf-8") as f: f.write(prisma_module)


print("Release Management Phase 1 Scaffolded (Schema, FF Package)")
