import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\notification-service\src"

# 1. Interfaces & Adapters
interfaces = """export interface INotificationProvider {
  send(to: string, content: string, subject?: string): Promise<boolean>;
}
"""
with open(os.path.join(base_dir, "providers/interfaces/provider.interface.ts"), "w", encoding="utf-8") as f: f.write(interfaces)

msg91 = """import { Injectable } from '@nestjs/common';
import { INotificationProvider } from '../interfaces/provider.interface';

@Injectable()
export class Msg91Adapter implements INotificationProvider {
  async send(to: string, content: string): Promise<boolean> {
    console.log(`[MSG91] Sending SMS to ${to}: ${content}`);
    return true; // Mock success
  }
}
"""
with open(os.path.join(base_dir, "providers/adapters/msg91.adapter.ts"), "w", encoding="utf-8") as f: f.write(msg91)

ses = """import { Injectable } from '@nestjs/common';
import { INotificationProvider } from '../interfaces/provider.interface';

@Injectable()
export class SesAdapter implements INotificationProvider {
  async send(to: string, content: string, subject: string): Promise<boolean> {
    console.log(`[SES] Sending Email to ${to} | Sub: ${subject}`);
    return true; // Mock success
  }
}
"""
with open(os.path.join(base_dir, "providers/adapters/ses.adapter.ts"), "w", encoding="utf-8") as f: f.write(ses)

firebase = """import { Injectable } from '@nestjs/common';
import { INotificationProvider } from '../interfaces/provider.interface';

@Injectable()
export class FirebaseAdapter implements INotificationProvider {
  async send(to: string, content: string, subject: string): Promise<boolean> {
    console.log(`[Firebase] Sending Push to token ${to} | Title: ${subject}`);
    return true; // Mock success
  }
}
"""
with open(os.path.join(base_dir, "providers/adapters/firebase.adapter.ts"), "w", encoding="utf-8") as f: f.write(firebase)


# 2. Template Service
template_svc = """import { Injectable } from '@nestjs/common';

@Injectable()
export class TemplateService {
  private templates = {
    'booking.confirmed': {
      en: 'Dear {{name}}, your booking is confirmed. PNR: {{pnr}}.',
      mr: 'प्रिय {{name}}, तुमचे बुकिंग निश्चित झाले आहे. PNR: {{pnr}}.'
    }
  };

  compile(templateCode: string, lang: string, payload: any): string {
    const template = this.templates[templateCode]?.[lang] || this.templates[templateCode]?.['en'];
    if (!template) return 'Notification content unavailable.';

    return template.replace(/{{(.*?)}}/g, (_, key) => payload[key.trim()] || '');
  }
}
"""
with open(os.path.join(base_dir, "notification/template.service.ts"), "w", encoding="utf-8") as f: f.write(template_svc)


# 3. Notification Repository
notif_repo = """import { Injectable } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "notification/repository/notification.repository.ts"), "w", encoding="utf-8") as f: f.write(notif_repo)


# 4. Notification Service (Router)
notif_svc = """import { Injectable } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "notification/notification.service.ts"), "w", encoding="utf-8") as f: f.write(notif_svc)


# 5. Controllers
notif_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { NotificationService } from './notification.service';
import { SendNotificationDto } from './dto/notification.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Notifications')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('notifications')
export class NotificationController {
  constructor(private readonly notificationService: NotificationService) {}

  @Post('send')
  @Roles('Admin', 'System')
  @ApiOperation({ summary: 'Manually trigger a notification (Admin/System only)' })
  async sendNotification(@Body() dto: SendNotificationDto) {
    return this.notificationService.processNotification(dto);
  }
}
"""
with open(os.path.join(base_dir, "notification/notification.controller.ts"), "w", encoding="utf-8") as f: f.write(notif_ctrl)


# 6. Modules
notif_mod = """import { Module } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "notification/notification.module.ts"), "w", encoding="utf-8") as f: f.write(notif_mod)

app_module = """import { Module } from '@nestjs/common';
import { NotificationModule } from './notification/notification.module';

@Module({
  imports: [NotificationModule],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(app_module)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AllExceptionsFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.useGlobalFilters(new AllExceptionsFilter());
  
  app.setGlobalPrefix('api/v1');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Notification Service')
    .setDescription('Centralized Communication and Templating Hub')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/notification', app, document);

  await app.listen(3010);
  console.log('Notification Service is running on http://localhost:3010');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Notification Service Phase 2 Scaffolded (Adapters, Router, Templates)")
