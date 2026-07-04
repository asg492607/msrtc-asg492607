import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { NotificationStatus } from '../enums/notification.enums';

@Injectable()
export class NotificationRepository {
  constructor(private prisma: PrismaService) {}

  async createLog(userId: string, channel: string, status: NotificationStatus, content: string) {
    // In actual implementation, we map this to Prisma NotificationLog model
    return { id: `log_${Date.now()}`, userId, channel, status };
  }
}
