import { Injectable, NotFoundException } from '@nestjs/common';
import { ParcelRepository } from './repository/parcel.repository';
import { BarcodeService } from './barcode.service';

@Injectable()
export class TrackingService {
  constructor(
    private repository: ParcelRepository,
    private barcode: BarcodeService
  ) {}

  async track(trackingNumber: string) {
    const parcel = await this.repository.findByTrackingNumber(trackingNumber);
    if (!parcel) throw new NotFoundException('Tracking number not found');
    
    return {
      trackingNumber: parcel.trackingNumber,
      status: parcel.status,
      origin: parcel.originDepotId,
      destination: parcel.destinationDepotId
    };
  }
  
  async getWaybill(trackingNumber: string) {
    const barcodeBase64 = await this.barcode.generateWaybillBarcode(trackingNumber);
    return { trackingNumber, barcodeBase64 };
  }
}
