import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
workflow_dir = os.path.join(base_dir, "backend/apps/workflow-service")
workflow_src = os.path.join(workflow_dir, "src")

# 1. Update schema.prisma
schema_path = os.path.join(base_dir, "packages/database/prisma/schema.prisma")
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        schema_content = f.read()
    
    # Check if Workflow models already exist
    if "model WorkflowJob" not in schema_content:
        workflow_models = """
model WorkflowJob {
  id           String            @id @default(uuid())
  name         String            @unique
  topicToEmit  String
  payload      Json?
  cron         String
  isActive     Boolean           @default(true)
  lastRun      DateTime?
  nextRun      DateTime?
  createdAt    DateTime          @default(now())
  histories    WorkflowHistory[]
}

model WorkflowHistory {
  id           String      @id @default(uuid())
  jobId        String
  status       String      // SUCCESS, FAILED
  durationMs   Int
  error        String?
  createdAt    DateTime    @default(now())
  job          WorkflowJob @relation(fields: [jobId], references: [id])
}
"""
        schema_content += workflow_models
        with open(schema_path, "w") as f:
            f.write(schema_content)

os.makedirs(workflow_dir, exist_ok=True)
os.makedirs(workflow_src, exist_ok=True)

# 2. Package.json
pkg_json = {
  "name": "workflow-service",
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
    "@nestjs/schedule": "^4.0.0",
    "@msrtc/database": "workspace:*",
    "@msrtc/kafka": "workspace:*",
    "@msrtc/redis": "workspace:*"
  },
  "devDependencies": {
    "typescript": "^5.1.3",
    "@types/node": "^20.0.0"
  }
}

with open(os.path.join(workflow_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)


# 3. Directories
dirs = [
    "workflow/controllers",
    "workflow/services",
    "workflow/dto",
    "prisma",
    "common/guards",
    "common/filters"
]
for d in dirs:
    os.makedirs(os.path.join(workflow_src, d), exist_ok=True)

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
with open(os.path.join(workflow_src, "prisma/prisma.service.ts"), "w", encoding="utf-8") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(workflow_src, "prisma/prisma.module.ts"), "w", encoding="utf-8") as f: f.write(prisma_module)


print("Workflow Service Phase 1 Scaffolded (Schema, Package)")
