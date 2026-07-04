import { Injectable } from '@nestjs/common';

@Injectable()
export class EtaService {
  /**
   * Mock calculation of distance/delay based on current coordinates.
   */
  calculateDelay(lat: number, lng: number, expectedLat: number, expectedLng: number): number {
    // Return delay in minutes
    return 5;
  }
}
