import { Injectable, Logger } from '@nestjs/common';
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
