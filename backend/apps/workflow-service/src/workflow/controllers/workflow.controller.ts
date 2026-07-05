import { Controller, Post, Get, Param, Body, Request } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Controller('workflows')
export class WorkflowController {
  constructor(private prisma: PrismaService) {}

  @Get('jobs')
  async getJobs() {
    return this.prisma.workflowJob.findMany();
  }

  @Post('jobs/:id/pause')
  async pauseJob(@Param('id') id: string) {
    return this.prisma.workflowJob.update({ where: { id }, data: { isActive: false } });
  }

  @Post('jobs/:id/resume')
  async resumeJob(@Param('id') id: string) {
    return this.prisma.workflowJob.update({ where: { id }, data: { isActive: true } });
  }
}
