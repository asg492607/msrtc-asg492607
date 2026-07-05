import { Injectable, NotFoundException } from '@nestjs/common';
import { CrewRepository } from './repository/crew.repository';
import { ComplianceService } from './compliance.service';
import { AvailabilityService } from './availability.service';
import { AssignCrewDto } from './dto/crew.dto';
import { CrewStatus } from './enums/crew.enums';

@Injectable()
export class AssignmentService {
  constructor(
    private repository: CrewRepository,
    private compliance: ComplianceService,
    private availability: AvailabilityService
  ) {}

  async assignTrip(crewId: string, dto: AssignCrewDto) {
    const crew = await this.repository.findById(crewId);
    if (!crew) throw new NotFoundException('Crew member not found');

    // 1. Check state machine
    this.availability.validateTransition(crew.status as CrewStatus, CrewStatus.ASSIGNED);

    // 2. Run compliance checks (License, Rest period)
    await this.compliance.checkAssignmentCompliance(crew);

    // 3. Save Assignment
    await this.repository.saveAssignment(crewId, dto.tripInstanceId);
    
    // 4. Update status
    await this.repository.updateStatus(crewId, CrewStatus.ASSIGNED);

    return { success: true, message: 'Crew assigned to trip successfully' };
  }
}
