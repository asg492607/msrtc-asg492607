import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
file_dir = os.path.join(base_dir, "backend/apps/file-service")
file_src = os.path.join(file_dir, "src")

# 1. Update schema.prisma
schema_path = os.path.join(base_dir, "packages/database/prisma/schema.prisma")
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        schema_content = f.read()
    
    # Check if FileMetadata models already exist to avoid duplication
    if "model FileMetadata" not in schema_content:
        file_models = """
model FileMetadata {
  id           String   @id @default(uuid())
  originalName String
  mimeType     String
  size         Int
  bucket       String
  objectKey    String   @unique
  folder       String?
  uploadedBy   String?
  createdAt    DateTime @default(now())
  isDeleted    Boolean  @default(false)
}
"""
        schema_content += file_models
        with open(schema_path, "w") as f:
            f.write(schema_content)

os.makedirs(file_dir, exist_ok=True)
os.makedirs(file_src, exist_ok=True)

# 2. Package.json
pkg_json = {
  "name": "file-service",
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
    "@nestjs/platform-express": "^10.0.0",
    "@aws-sdk/client-s3": "^3.400.0",
    "@aws-sdk/s3-request-presigner": "^3.400.0",
    "@msrtc/database": "workspace:*",
    "@msrtc/kafka": "workspace:*",
    "uuid": "^9.0.0",
    "multer": "1.4.5-lts.1"
  },
  "devDependencies": {
    "@types/multer": "^1.4.7",
    "typescript": "^5.1.3"
  }
}

with open(os.path.join(file_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)


# 3. Directories
dirs = [
    "file/controllers",
    "file/services",
    "file/dto",
    "prisma",
    "common/guards",
    "common/filters",
    "common/decorators"
]
for d in dirs:
    os.makedirs(os.path.join(file_src, d), exist_ok=True)


# 4. Storage Service (AWS S3 Abstraction)
storage_svc = """import { Injectable, Logger } from '@nestjs/common';
import { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

@Injectable()
export class StorageService {
  private s3Client: S3Client;
  private readonly logger = new Logger(StorageService.name);

  constructor() {
    this.s3Client = new S3Client({
      region: process.env.AWS_REGION || 'us-east-1',
      endpoint: process.env.S3_ENDPOINT || 'http://localhost:9000', // Default MinIO
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID || 'minioadmin',
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || 'minioadmin',
      },
      forcePathStyle: true, // Required for MinIO
    });
  }

  async uploadFile(bucket: string, key: string, buffer: Buffer, mimeType: string) {
    const command = new PutObjectCommand({
      Bucket: bucket,
      Key: key,
      Body: buffer,
      ContentType: mimeType,
    });
    await this.s3Client.send(command);
    this.logger.log(`Uploaded ${key} to ${bucket}`);
  }

  async deleteFile(bucket: string, key: string) {
    const command = new DeleteObjectCommand({ Bucket: bucket, Key: key });
    await this.s3Client.send(command);
  }

  async getPresignedUrl(bucket: string, key: string, expiresIn: number = 900) {
    const command = new GetObjectCommand({ Bucket: bucket, Key: key });
    return getSignedUrl(this.s3Client, command, { expiresIn });
  }
}
"""
with open(os.path.join(file_src, "file/services/storage.service.ts"), "w", encoding="utf-8") as f: f.write(storage_svc)

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
with open(os.path.join(file_src, "prisma/prisma.service.ts"), "w", encoding="utf-8") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(file_src, "prisma/prisma.module.ts"), "w", encoding="utf-8") as f: f.write(prisma_module)


print("File Service Phase 1 Scaffolded (Schema, Package, StorageService)")
