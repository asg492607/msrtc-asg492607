import { Module } from '@nestjs/common';
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
