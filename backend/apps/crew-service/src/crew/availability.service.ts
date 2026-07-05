import { Injectable, BadRequestException } from '@nestjs/common';
import { CrewStatus } from './enums/crew.enums';

@Injectable()
export class AvailabilityService {
  private allowedTransitions = {
    [CrewStatus.AVAILABLE]: [CrewStatus.ASSIGNED, CrewStatus.ON_LEAVE, CrewStatus.MEDICAL_HOLD],
    [CrewStatus.ASSIGNED]: [CrewStatus.CHECKED_IN, CrewStatus.AVAILABLE], // Can un-assign
    [CrewStatus.CHECKED_IN]: [CrewStatus.ON_DUTY],
    [CrewStatus.ON_DUTY]: [CrewStatus.CHECKED_OUT],
    [CrewStatus.CHECKED_OUT]: [CrewStatus.AVAILABLE],
    [CrewStatus.ON_LEAVE]: [CrewStatus.AVAILABLE],
    [CrewStatus.MEDICAL_HOLD]: [CrewStatus.AVAILABLE],
  };

  validateTransition(currentStatus: CrewStatus, nextStatus: CrewStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Invalid state transition from ${currentStatus} to ${nextStatus}`);
    }
  }
}
