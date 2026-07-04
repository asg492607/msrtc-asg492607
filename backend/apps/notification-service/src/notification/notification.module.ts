import { Module } from '@nestjs/common';
import { NotificationController } from './notification.controller';
import { NotificationService } from './notification.service';
import { TemplateService } from './template.service';
import { NotificationRepository } from './repository/notification.repository';
import { Msg91Adapter } from '../providers/adapters/msg91.adapter';
import { SesAdapter } from '../providers/adapters/ses.adapter';
import { FirebaseAdapter } from '../providers/adapters/firebase.adapter';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [NotificationController],
  providers: [
    NotificationService, 
    TemplateService, 
    NotificationRepository,
    Msg91Adapter,
    SesAdapter,
    FirebaseAdapter
  ],
})
export class NotificationModule {}
