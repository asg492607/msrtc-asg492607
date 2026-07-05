import { Injectable, BadRequestException } from '@nestjs/common';
import { VehicleStatus } from './enums/depot.enums';

@Injectable()
export class AvailabilityService {
  private allowedTransitions = {
    [VehicleStatus.AVAILABLE]: [VehicleStatus.CREW_ASSIGNED, VehicleStatus.UNDER_MAINTENANCE],
    [VehicleStatus.CREW_ASSIGNED]: [VehicleStatus.PLATFORM_ASSIGNED, VehicleStatus.AVAILABLE],
    [VehicleStatus.PLATFORM_ASSIGNED]: [VehicleStatus.READY_FOR_DISPATCH, VehicleStatus.AVAILABLE],
    [VehicleStatus.READY_FOR_DISPATCH]: [VehicleStatus.DISPATCHED, VehicleStatus.AVAILABLE],
    [VehicleStatus.DISPATCHED]: [VehicleStatus.RUNNING],
    [VehicleStatus.RUNNING]: [VehicleStatus.ARRIVED],
    [VehicleStatus.ARRIVED]: [VehicleStatus.PARKED],
    [VehicleStatus.PARKED]: [VehicleStatus.AVAILABLE, VehicleStatus.UNDER_MAINTENANCE],
    [VehicleStatus.UNDER_MAINTENANCE]: [VehicleStatus.AVAILABLE],
  };

  validateTransition(currentStatus: VehicleStatus, nextStatus: VehicleStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Bus cannot transition from ${currentStatus} to ${nextStatus}`);
    }
  }
}
