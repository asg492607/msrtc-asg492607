import { Injectable, BadRequestException, NotFoundException } from '@nestjs/common';
import { DepotRepository } from './repository/depot.repository';
import { AvailabilityService } from './availability.service';
import { DispatchBusDto } from './dto/depot.dto';
import { VehicleStatus } from './enums/depot.enums';

@Injectable()
export class DispatchService {
  constructor(
    private repository: DepotRepository,
    private availability: AvailabilityService
  ) {}

  /**
   * Extremely critical cross-domain validation engine
   */
  async dispatchBus(dto: DispatchBusDto) {
    const bus = await this.repository.findBusById(dto.busId);
    if (!bus) throw new NotFoundException('Bus not found');

    // 1. Check if bus is mechanically available and on a platform
    this.availability.validateTransition(bus.status as VehicleStatus, VehicleStatus.DISPATCHED);

    // 2. Validate Crew Check-In (Mocking inter-service call to Crew Service)
    const isCrewCheckedIn = true; 
    if (!isCrewCheckedIn) {
      throw new BadRequestException('Cannot dispatch: Assigned crew has not checked in.');
    }

    // 3. Dispatch
    await this.repository.logDispatch(dto.busId, dto.tripInstanceId);
    await this.repository.updateBusStatus(dto.busId, VehicleStatus.DISPATCHED);
    
    // Fire Kafka Event: bus.dispatched
    return { success: true, message: 'Bus officially dispatched from Depot' };
  }
}
