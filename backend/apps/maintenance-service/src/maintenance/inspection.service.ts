import { Injectable, NotFoundException } from '@nestjs/common';
import { MaintenanceRepository } from './repository/maintenance.repository';
import { WorkshopService } from './workshop.service';
import { InspectionDto } from './dto/maintenance.dto';
import { MaintenanceStatus } from './enums/maintenance.enums';

@Injectable()
export class InspectionService {
  constructor(
    private repository: MaintenanceRepository,
    private workshop: WorkshopService
  ) {}

  async performInspection(jobId: string, dto: InspectionDto) {
    const job = await this.repository.findById(jobId);
    if (!job) throw new NotFoundException();

    this.workshop.validateTransition(job.status as MaintenanceStatus, MaintenanceStatus.QUALITY_CHECK);
    await this.repository.updateStatus(jobId, MaintenanceStatus.QUALITY_CHECK);

    const passed = dto.passed.toUpperCase() === 'YES';
    await this.repository.logInspection(jobId, dto.comments, passed);

    return { success: true, passed };
  }
}
