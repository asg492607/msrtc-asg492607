import { Controller, Get, Param, Query } from '@nestjs/common';
import { FeatureFlagService } from '../services/feature-flag.service';

@Controller('feature-flags')
export class FeatureFlagController {
  constructor(private flagService: FeatureFlagService) {}

  @Get(':key/eval')
  async evaluateFlag(@Param('key') key: string) {
    const isEnabled = await this.flagService.isEnabled(key);
    return { key, isEnabled };
  }
}
