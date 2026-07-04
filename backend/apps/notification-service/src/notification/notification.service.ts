import { Injectable } from '@nestjs/common';
import { TemplateService } from './template.service';
import { NotificationRepository } from './repository/notification.repository';
import { Msg91Adapter } from '../providers/adapters/msg91.adapter';
import { SesAdapter } from '../providers/adapters/ses.adapter';
import { FirebaseAdapter } from '../providers/adapters/firebase.adapter';
import { SendNotificationDto } from './dto/notification.dto';
import { NotificationChannel, NotificationStatus } from './enums/notification.enums';

@Injectable()
export class NotificationService {
  constructor(
    private templateService: TemplateService,
    private repository: NotificationRepository,
    private smsAdapter: Msg91Adapter,
    private emailAdapter: SesAdapter,
    private pushAdapter: FirebaseAdapter
  ) {}

  async processNotification(dto: SendNotificationDto) {
    // 1. Fetch user preferences & language (Mocked)
    const userPref = { lang: 'en', phone: '+919999999999', email: 'test@example.com', pushToken: 'token123' };

    // 2. Compile Template
    const content = this.templateService.compile(dto.templateCode, userPref.lang, dto.payload || {});

    const results = [];

    // 3. Route to Channels
    for (const channel of dto.channels) {
      let success = false;
      
      try {
        if (channel === NotificationChannel.SMS) {
          success = await this.smsAdapter.send(userPref.phone, content);
        } else if (channel === NotificationChannel.EMAIL) {
          success = await this.emailAdapter.send(userPref.email, content, 'MSRTC Update');
        } else if (channel === NotificationChannel.PUSH) {
          success = await this.pushAdapter.send(userPref.pushToken, content, 'MSRTC Update');
        }
      } catch (e) {
        success = false;
      }

      // 4. Log Delivery Status
      const status = success ? NotificationStatus.DELIVERED : NotificationStatus.FAILED;
      await this.repository.createLog(dto.userId, channel, status, content);
      
      results.push({ channel, status });
    }

    return { message: 'Notification processing completed', results };
  }
}
