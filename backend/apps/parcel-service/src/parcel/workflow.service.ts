import { Injectable, BadRequestException } from '@nestjs/common';
import { ParcelStatus } from './enums/parcel.enums';

@Injectable()
export class WorkflowService {
  private allowedTransitions = {
    [ParcelStatus.BOOKED]: [ParcelStatus.PAYMENT_PENDING, ParcelStatus.CONFIRMED],
    [ParcelStatus.PAYMENT_PENDING]: [ParcelStatus.CONFIRMED],
    [ParcelStatus.CONFIRMED]: [ParcelStatus.DISPATCHED],
    [ParcelStatus.DISPATCHED]: [ParcelStatus.IN_TRANSIT],
    [ParcelStatus.IN_TRANSIT]: [ParcelStatus.ARRIVED],
    [ParcelStatus.ARRIVED]: [ParcelStatus.READY_FOR_PICKUP],
    [ParcelStatus.READY_FOR_PICKUP]: [ParcelStatus.DELIVERED, ParcelStatus.RETURN_TO_SENDER],
  };

  validateTransition(currentStatus: ParcelStatus, nextStatus: ParcelStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Invalid state transition from ${currentStatus} to ${nextStatus}`);
    }
  }
}
