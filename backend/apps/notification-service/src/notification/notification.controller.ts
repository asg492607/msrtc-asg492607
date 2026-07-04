import { Controller, Get } from '@nestjs/common';
import { NotificationService } from './notification.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Notification')
@Controller()
export class NotificationController {
  constructor(private readonly service: NotificationService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
