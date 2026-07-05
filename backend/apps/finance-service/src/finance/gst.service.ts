import { Injectable } from '@nestjs/common';

@Injectable()
export class GstService {
  calculateGST(amount: number): number {
    return amount * 0.05; // 5% GST for transit
  }

  generateMonthlyReport() {
    return {
      month: new Date().getMonth(),
      totalTaxableRevenue: 1000000,
      totalGstCollected: 50000
    };
  }
}
