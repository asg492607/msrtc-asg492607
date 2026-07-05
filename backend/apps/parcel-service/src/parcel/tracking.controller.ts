import { Controller, Get, Param } from '@nestjs/common';
import { TrackingService } from './tracking.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Parcel Tracking (Public)')
@Controller('tracking')
export class TrackingController {
  constructor(private readonly trackingService: TrackingService) {}

  @Get(':trackingNumber')
  @ApiOperation({ summary: 'Publicly track a parcel status (No Auth Required)' })
  async track(@Param('trackingNumber') trackingNumber: string) {
    return this.trackingService.track(trackingNumber);
  }

  @Get(':trackingNumber/waybill')
  @ApiOperation({ summary: 'Generate Barcode/QR Waybill for package label' })
  async waybill(@Param('trackingNumber') trackingNumber: string) {
    return this.trackingService.getWaybill(trackingNumber);
  }
}
