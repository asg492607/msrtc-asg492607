import { Controller, Post, Body, Request } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Controller('reports/schedules')
export class ScheduleController {
  constructor(private prisma: PrismaService) {}

  @Post()
  async createSchedule(@Body() body: any, @Request() req: any) {
    return this.prisma.reportSchedule.create({
      data: {
        type: body.type,
        cron: body.cron,
        deliveryType: body.deliveryType,
        parameters: body.parameters,
        requestedBy: 'sys-admin'
      }
    });
  }
}
