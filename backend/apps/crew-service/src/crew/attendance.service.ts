import { Injectable, NotFoundException } from '@nestjs/common';
import { CrewRepository } from './repository/crew.repository';
import { AvailabilityService } from './availability.service';
import { CrewStatus } from './enums/crew.enums';

@Injectable()
export class AttendanceService {
  constructor(
    private repository: CrewRepository,
    private availability: AvailabilityService
  ) {}

  async markCheckIn(crewId: string) {
    const crew = await this.repository.findById(crewId);
    if (!crew) throw new NotFoundException();

    this.availability.validateTransition(crew.status as CrewStatus, CrewStatus.CHECKED_IN);
    await this.repository.updateStatus(crewId, CrewStatus.CHECKED_IN);
    // Fire Kafka event: crew.checked_in (so Depot Dispatch knows they are ready)
    return { success: true, status: CrewStatus.CHECKED_IN };
  }

  async markCheckOut(crewId: string) {
    const crew = await this.repository.findById(crewId);
    if (!crew) throw new NotFoundException();

    this.availability.validateTransition(crew.status as CrewStatus, CrewStatus.CHECKED_OUT);
    await this.repository.updateStatus(crewId, CrewStatus.CHECKED_OUT);
    // Automatic transition back to available after checkout logic
    await this.repository.updateStatus(crewId, CrewStatus.AVAILABLE);
    return { success: true, status: CrewStatus.AVAILABLE };
  }
}
