import { Controller, Get } from '@nestjs/common';
import { HqService } from './hq.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Hq')
@Controller()
export class HqController {
  constructor(private readonly service: HqService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
