import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
reporting_dir = os.path.join(base_dir, "backend/apps/reporting-service")
reporting_src = os.path.join(reporting_dir, "src")

# 1. Update schema.prisma
schema_path = os.path.join(base_dir, "packages/database/prisma/schema.prisma")
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        schema_content = f.read()
    
    # Check if Reporting models already exist
    if "model ReportJob" not in schema_content:
        reporting_models = """
model ReportJob {
  id           String   @id @default(uuid())
  type         String
  status       String   @default("PENDING") // PENDING, PROCESSING, COMPLETED, FAILED
  requestedBy  String?
  fileId       String?  // Reference to FileMetadata.id
  error        String?
  parameters   Json?
  createdAt    DateTime @default(now())
  completedAt  DateTime?
}

model ReportSchedule {
  id           String   @id @default(uuid())
  type         String
  cron         String
  requestedBy  String?
  deliveryType String   @default("EMAIL") // EMAIL, DOWNLOAD
  parameters   Json?
  isActive     Boolean  @default(true)
  createdAt    DateTime @default(now())
}
"""
        schema_content += reporting_models
        with open(schema_path, "w") as f:
            f.write(schema_content)

os.makedirs(reporting_dir, exist_ok=True)
os.makedirs(reporting_src, exist_ok=True)

# 2. Package.json
pkg_json = {
  "name": "reporting-service",
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
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "typescript": "^5.1.3",
    "@types/node": "^20.0.0"
  }
}

with open(os.path.join(reporting_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)


# 3. Directories
dirs = [
    "report/controllers",
    "report/services",
    "report/dto",
    "prisma",
    "common/guards",
    "common/filters"
]
for d in dirs:
    os.makedirs(os.path.join(reporting_src, d), exist_ok=True)


# 4. Export Service (CSV Generation logic)
export_svc = """import { Injectable } from '@nestjs/common';

@Injectable()
export class ExportService {
  generateCsv(data: any[]): Buffer {
    if (!data || data.length === 0) return Buffer.from('');
    
    // Extract headers
    const headers = Object.keys(data[0]).join(',');
    
    // Map rows
    const rows = data.map(row => 
      Object.values(row)
        .map(value => `"${String(value).replace(/"/g, '""')}"`)
        .join(',')
    );

    const csvContent = [headers, ...rows].join('\\n');
    return Buffer.from(csvContent, 'utf-8');
  }
}
"""
with open(os.path.join(reporting_src, "report/services/export.service.ts"), "w", encoding="utf-8") as f: f.write(export_svc)

# 5. Prisma Service
prisma_service = """import { Injectable, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }
}
"""
with open(os.path.join(reporting_src, "prisma/prisma.service.ts"), "w", encoding="utf-8") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(reporting_src, "prisma/prisma.module.ts"), "w", encoding="utf-8") as f: f.write(prisma_module)


print("Reporting Service Phase 1 Scaffolded (Schema, Package, ExportService)")
