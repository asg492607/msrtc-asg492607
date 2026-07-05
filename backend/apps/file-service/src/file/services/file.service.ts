import { Injectable } from '@nestjs/common';
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
