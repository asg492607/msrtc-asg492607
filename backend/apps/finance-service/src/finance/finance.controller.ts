import { Controller, Get } from '@nestjs/common';
import { FinanceService } from './finance.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Finance')
@Controller()
export class FinanceController {
  constructor(private readonly service: FinanceService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
