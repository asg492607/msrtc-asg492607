import { Controller, Get } from '@nestjs/common';
import { PassService } from './pass.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Pass')
@Controller()
export class PassController {
  constructor(private readonly service: PassService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
