import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\file-service\src"

# 1. File Service (Business Logic + Kafka)
file_svc = """import { Injectable } from '@nestjs/common';
import { StorageService } from './storage.service';
import { PrismaService } from '../../prisma/prisma.service';
import { EventBusService, Topics } from '@msrtc/kafka';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class FileService {
  constructor(
    private storage: StorageService,
    private prisma: PrismaService,
    private eventBus: EventBusService
  ) {}

  async processUpload(file: Express.Multer.File, folder: string, userId: string) {
    const bucket = process.env.S3_BUCKET || 'msrtc-assets';
    const uuid = uuidv4();
    const extension = file.originalname.split('.').pop();
    const objectKey = `${folder}/${uuid}.${extension}`;

    // 1. Upload to MinIO/S3
    await this.storage.uploadFile(bucket, objectKey, file.buffer, file.mimetype);

    // 2. Save Metadata to Postgres
    const metadata = await this.prisma.fileMetadata.create({
      data: {
        originalName: file.originalname,
        mimeType: file.mimetype,
        size: file.size,
        bucket,
        objectKey,
        folder,
        uploadedBy: userId,
      }
    });

    // 3. Publish Event
    await this.eventBus.publish('file.events', {
      type: 'file.uploaded',
      fileId: metadata.id,
      objectKey,
    });

    return metadata;
  }

  async getDownloadUrl(fileId: string): Promise<string> {
    const file = await this.prisma.fileMetadata.findUnique({ where: { id: fileId } });
    if (!file || file.isDeleted) throw new Error('File not found');

    return this.storage.getPresignedUrl(file.bucket, file.objectKey);
  }
}
"""
with open(os.path.join(base_dir, "file/services/file.service.ts"), "w", encoding="utf-8") as f: f.write(file_svc)


# 2. Controllers
upload_ctrl = """import { Controller, Post, UseInterceptors, UploadedFile, Body, UseGuards, Request } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { FileService } from '../services/file.service';
// import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth, ApiConsumes, ApiBody } from '@nestjs/swagger';

@ApiTags('File Upload')
@Controller('files')
// @UseGuards(JwtAuthGuard)
export class UploadController {
  constructor(private fileService: FileService) {}

  @Post('upload')
  @ApiConsumes('multipart/form-data')
  @ApiOperation({ summary: 'Upload a binary file to object storage' })
  @UseInterceptors(FileInterceptor('file'))
  async uploadFile(@UploadedFile() file: Express.Multer.File, @Body('folder') folder: string, @Request() req: any) {
    // const userId = req.user.userId;
    const userId = 'sys-admin'; // mocked for now
    return this.fileService.processUpload(file, folder || 'misc', userId);
  }
}
"""
with open(os.path.join(base_dir, "file/controllers/upload.controller.ts"), "w", encoding="utf-8") as f: f.write(upload_ctrl)


download_ctrl = """import { Controller, Get, Param, UseGuards } from '@nestjs/common';
import { FileService } from '../services/file.service';
// import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('File Download')
@Controller('files')
// @UseGuards(JwtAuthGuard)
export class DownloadController {
  constructor(private fileService: FileService) {}

  @Get(':id/presign')
  @ApiOperation({ summary: 'Get a temporary, secure download URL' })
  async getPresignedUrl(@Param('id') id: string) {
    const url = await this.fileService.getDownloadUrl(id);
    return { url, expiresIn: 900 }; // 15 mins
  }
}
"""
with open(os.path.join(base_dir, "file/controllers/download.controller.ts"), "w", encoding="utf-8") as f: f.write(download_ctrl)


# 3. Module & Main
file_mod = """import { Module } from '@nestjs/common';
import { StorageService } from './file/services/storage.service';
import { FileService } from './file/services/file.service';
import { UploadController } from './file/controllers/upload.controller';
import { DownloadController } from './file/controllers/download.controller';
import { PrismaModule } from './prisma/prisma.module';
import { KafkaModule } from '@msrtc/kafka';

@Module({
  imports: [PrismaModule, KafkaModule],
  controllers: [UploadController, DownloadController],
  providers: [StorageService, FileService],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(file_mod)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.setGlobalPrefix('api/v1');

  const config = new DocumentBuilder()
    .setTitle('MSRTC File Storage Service')
    .setDescription('Centralized Object Storage and Asset Manager')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/files', app, document);

  await app.listen(3019);
  console.log('File Service is running on http://localhost:3019');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("File Service Phase 2 Scaffolded (FileService, Controllers, Module)")
