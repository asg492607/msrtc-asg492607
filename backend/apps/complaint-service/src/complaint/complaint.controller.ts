import { Controller, Get } from '@nestjs/common';
import { ComplaintService } from './complaint.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Complaint')
@Controller()
export class ComplaintController {
  constructor(private readonly service: ComplaintService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
