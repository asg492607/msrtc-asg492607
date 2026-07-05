import { Controller, Get } from '@nestjs/common';
import { FinOpsService } from '../services/finops.service';

@Controller('finops')
export class FinOpsController {
  constructor(private finopsService: FinOpsService) {}

  @Get('dashboard')
  async getDashboard() {
    return this.finopsService.getDashboard();
  }
}
