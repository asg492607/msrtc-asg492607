import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
ai_dir = os.path.join(base_dir, "backend/apps/ai-service")
ai_src = os.path.join(ai_dir, "src")

# 1. Update schema.prisma
schema_path = os.path.join(base_dir, "packages/database/prisma/schema.prisma")
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        schema_content = f.read()
    
    # Check if AI models already exist
    if "model AiModel" not in schema_content:
        ai_models = """
model AiModel {
  id          String   @id @default(uuid())
  name        String   @unique
  version     String
  endpoint    String?
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())
}

model InferenceLog {
  id            String   @id @default(uuid())
  modelName     String
  tenantId      String
  inputs        Json
  outputs       Json
  confidence    Float
  latencyMs     Int
  createdAt     DateTime @default(now())
}
"""
        schema_content += ai_models
        with open(schema_path, "w") as f:
            f.write(schema_content)

os.makedirs(ai_dir, exist_ok=True)
os.makedirs(ai_src, exist_ok=True)

# 2. Package.json
pkg_json = {
  "name": "ai-service",
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
    "@msrtc/redis": "workspace:*",
    "@msrtc/tenant": "workspace:*"
  },
  "devDependencies": {
    "typescript": "^5.1.3",
    "@types/node": "^20.0.0"
  }
}

with open(os.path.join(ai_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)


# 3. Directories
dirs = [
    "ai/controllers",
    "ai/services",
    "ai/dto",
    "prisma",
    "common/guards",
    "common/filters"
]
for d in dirs:
    os.makedirs(os.path.join(ai_src, d), exist_ok=True)

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
with open(os.path.join(ai_src, "prisma/prisma.service.ts"), "w", encoding="utf-8") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(ai_src, "prisma/prisma.module.ts"), "w", encoding="utf-8") as f: f.write(prisma_module)


print("AI Service Phase 1 Scaffolded (Schema, Package)")
