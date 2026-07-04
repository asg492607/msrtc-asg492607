import { Controller, Get } from '@nestjs/common';
import { CrewService } from './crew.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Crew')
@Controller()
export class CrewController {
  constructor(private readonly service: CrewService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
