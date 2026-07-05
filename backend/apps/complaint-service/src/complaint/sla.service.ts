import { Injectable } from '@nestjs/common';
import { ComplaintCategory, ComplaintPriority } from './enums/complaint.enums';

@Injectable()
export class SlaService {
  /**
   * Determines priority and resolution deadlines based on category.
   */
  calculateSla(category: ComplaintCategory) {
    if (category === ComplaintCategory.STAFF_BEHAVIOR) {
      return { priority: ComplaintPriority.HIGH, resolutionHours: 24 };
    }
    if (category === ComplaintCategory.DELAY) {
      return { priority: ComplaintPriority.LOW, resolutionHours: 72 };
    }
    return { priority: ComplaintPriority.MEDIUM, resolutionHours: 48 };
  }
}
