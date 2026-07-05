import { Injectable, BadRequestException } from '@nestjs/common';
import { DepotRepository } from './repository/depot.repository';
import { AvailabilityService } from './availability.service';
import { AssignPlatformDto } from './dto/depot.dto';
import { VehicleStatus } from './enums/depot.enums';

@Injectable()
export class PlatformService {
  constructor(
    private repository: DepotRepository,
    private availability: AvailabilityService
  ) {}

  async assignToPlatform(dto: AssignPlatformDto) {
    const bus = await this.repository.findBusById(dto.busId);
    if (!bus) throw new BadRequestException('Bus not found');

    this.availability.validateTransition(bus.status as VehicleStatus, VehicleStatus.PLATFORM_ASSIGNED);
    
    // In real app, check if platformNumber is currently OCCUPIED
    
    await this.repository.updateBusStatus(dto.busId, VehicleStatus.PLATFORM_ASSIGNED);
    return { success: true, platformNumber: dto.platformNumber };
  }
}
