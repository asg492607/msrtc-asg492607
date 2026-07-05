import { Injectable } from '@nestjs/common';
import { PassCategory } from './enums/pass.enums';

@Injectable()
export class ConcessionService {
  calculateDiscount(category: PassCategory): number {
    switch (category) {
      case PassCategory.SENIOR_CITIZEN: return 50; // 50% discount
      case PassCategory.STUDENT: return 66; // 66% discount
      case PassCategory.DISABLED: return 100; // 100% discount
      default: return 0;
    }
  }
}
