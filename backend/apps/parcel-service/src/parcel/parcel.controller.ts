import { Controller, Get } from '@nestjs/common';
import { ParcelService } from './parcel.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Parcel')
@Controller()
export class ParcelController {
  constructor(private readonly service: ParcelService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
