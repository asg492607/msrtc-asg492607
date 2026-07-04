import { Controller, Get } from '@nestjs/common';
import { MasterDataService } from './master-data.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('MasterData')
@Controller()
export class MasterDataController {
  constructor(private readonly service: MasterDataService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
