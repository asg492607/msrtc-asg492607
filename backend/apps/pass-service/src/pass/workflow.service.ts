import { Injectable, BadRequestException } from '@nestjs/common';
import { PassStatus } from './enums/pass.enums';

@Injectable()
export class WorkflowService {
  private allowedTransitions = {
    [PassStatus.SUBMITTED]: [PassStatus.UNDER_REVIEW],
    [PassStatus.UNDER_REVIEW]: [PassStatus.APPROVED, PassStatus.REJECTED],
    [PassStatus.APPROVED]: [PassStatus.PAYMENT_PENDING],
    [PassStatus.PAYMENT_PENDING]: [PassStatus.ACTIVE],
    [PassStatus.ACTIVE]: [PassStatus.EXPIRED, PassStatus.SUSPENDED, PassStatus.CANCELLED],
    [PassStatus.SUSPENDED]: [PassStatus.ACTIVE, PassStatus.CANCELLED],
  };

  validateTransition(currentStatus: PassStatus, nextStatus: PassStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Invalid state transition from ${currentStatus} to ${nextStatus}`);
    }
  }
}
