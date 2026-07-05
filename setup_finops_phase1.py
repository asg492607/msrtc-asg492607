import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
finops_dir = os.path.join(base_dir, "backend/apps/finops-service")
finops_src = os.path.join(finops_dir, "src")

# 1. Update schema.prisma
schema_path = os.path.join(base_dir, "packages/database/prisma/schema.prisma")
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        schema_content = f.read()
    
    if "model Budget" not in schema_content:
        finops_models = """
model Budget {
  id            String   @id @default(uuid())
  tenantId      String
  serviceName   String
  monthlyLimit  Float
  currentSpend  Float    @default(0.0)
  currency      String   @default("INR")
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
}

model CostAnomaly {
  id            String   @id @default(uuid())
  tenantId      String
  description   String
  severity      String   // LOW, MEDIUM, HIGH, CRITICAL
  status        String   // OPEN, ACKNOWLEDGED, RESOLVED
  detectedAt    DateTime @default(now())
}
"""
        schema_content += finops_models
        with open(schema_path, "w") as f:
            f.write(schema_content)

os.makedirs(finops_dir, exist_ok=True)
os.makedirs(finops_src, exist_ok=True)

# 2. Package.json
pkg_json = {
  "name": "finops-service",
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
    "@msrtc/tenant": "workspace:*"
  },
  "devDependencies": {
    "typescript": "^5.1.3",
    "@types/node": "^20.0.0"
  }
}

with open(os.path.join(finops_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)


# 3. Directories
dirs = [
    "finops/controllers",
    "finops/services",
    "prisma"
]
for d in dirs:
    os.makedirs(os.path.join(finops_src, d), exist_ok=True)

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
with open(os.path.join(finops_src, "prisma/prisma.service.ts"), "w", encoding="utf-8") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(finops_src, "prisma/prisma.module.ts"), "w", encoding="utf-8") as f: f.write(prisma_module)


print("FinOps Phase 1 Scaffolded (Schema, Package)")
