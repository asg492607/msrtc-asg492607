import { Controller, Post, Body } from '@nestjs/common';
import { DemandService } from '../services/demand.service';

@Controller('ai')
export class PredictionController {
  constructor(private demandService: DemandService) {}

  @Post('predict-demand')
  async predictDemand(@Body() body: { routeId: string, date: string }) {
    return this.demandService.predictDemand(body.routeId, body.date);
  }
}
