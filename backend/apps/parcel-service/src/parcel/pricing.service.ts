import { Injectable } from '@nestjs/common';
import { ParcelItemDto } from './dto/parcel.dto';

@Injectable()
export class PricingService {
  /**
   * Complex pricing based on weight (kg) and volume (Cubic Meters).
   * E.g. Base rate 50 + (10 per kg) + (20 per cbm)
   */
  calculateFare(items: ParcelItemDto[]): number {
    let totalFare = 50; // Base fare
    for (const item of items) {
      totalFare += (item.weightKg * 10) + (item.volumeCbM * 20);
    }
    return totalFare;
  }
}
