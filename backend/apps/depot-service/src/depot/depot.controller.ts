import { Controller, Get } from '@nestjs/common';
import { DepotService } from './depot.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Depot')
@Controller()
export class DepotController {
  constructor(private readonly service: DepotService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
