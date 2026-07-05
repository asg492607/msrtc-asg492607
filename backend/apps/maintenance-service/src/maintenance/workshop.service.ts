import { Injectable, BadRequestException, NotFoundException } from '@nestjs/common';
import { MaintenanceRepository } from './repository/maintenance.repository';
import { CompleteMaintenanceDto } from './dto/maintenance.dto';
import { MaintenanceStatus } from './enums/maintenance.enums';

@Injectable()
export class WorkshopService {
  constructor(private repository: MaintenanceRepository) {}

  private allowedTransitions = {
    [MaintenanceStatus.SCHEDULED]: [MaintenanceStatus.ASSIGNED, MaintenanceStatus.CANCELLED],
    [MaintenanceStatus.ASSIGNED]: [MaintenanceStatus.IN_PROGRESS],
    [MaintenanceStatus.IN_PROGRESS]: [MaintenanceStatus.QUALITY_CHECK],
    [MaintenanceStatus.QUALITY_CHECK]: [MaintenanceStatus.COMPLETED, MaintenanceStatus.IN_PROGRESS],
    [MaintenanceStatus.COMPLETED]: [],
    [MaintenanceStatus.CANCELLED]: [],
  };

  validateTransition(currentStatus: MaintenanceStatus, nextStatus: MaintenanceStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Job cannot transition from ${currentStatus} to ${nextStatus}`);
    }
  }

  async startJob(id: string) {
    const job = await this.repository.findById(id);
    if (!job) throw new NotFoundException('Job not found');

    this.validateTransition(job.status as MaintenanceStatus, MaintenanceStatus.IN_PROGRESS);
    await this.repository.updateStatus(id, MaintenanceStatus.IN_PROGRESS);

    // CRITICAL: Fire Kafka Event -> vehicle.maintenance.started
    // The Depot Service will consume this and flag the bus as UNDER_MAINTENANCE

    return { success: true, message: 'Job started. Bus locked in Depot.' };
  }

  async completeJob(id: string, dto: CompleteMaintenanceDto) {
    const job = await this.repository.findById(id);
    if (!job) throw new NotFoundException('Job not found');

    this.validateTransition(job.status as MaintenanceStatus, MaintenanceStatus.COMPLETED);

    // 1. Enforce Quality Check
    const hasPassed = await this.repository.hasPassedInspection(id);
    if (!hasPassed) {
      throw new BadRequestException('Cannot complete job without a passing Quality Check inspection.');
    }

    // 2. Complete Job
    await this.repository.updateStatus(id, MaintenanceStatus.COMPLETED);
    
    // Fire Kafka Event -> vehicle.available
    // The Depot Service unlocks the bus

    return { success: true, message: 'Job completed. Bus unlocked.' };
  }
}
