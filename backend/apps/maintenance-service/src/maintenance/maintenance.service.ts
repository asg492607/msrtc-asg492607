import { Injectable } from '@nestjs/common';
import { MaintenanceRepository } from './repository/maintenance.repository';
import { CreateMaintenanceJobDto, BreakdownReportDto } from './dto/maintenance.dto';

@Injectable()
export class MaintenanceService {
  constructor(private repository: MaintenanceRepository) {}

  async createJob(dto: CreateMaintenanceJobDto) {
    return this.repository.createJob(dto);
  }

  async reportBreakdown(dto: BreakdownReportDto, reportedById: string) {
    const report = await this.repository.logBreakdown({
      busId: dto.busId,
      locationCoordinates: dto.locationCoordinates,
      issueDescription: dto.issueDescription,
      reportedById
    });

    // Fire Kafka Event -> vehicle.breakdown
    // Depot service locks bus. Notification service alerts Workshop Foreman.

    return report;
  }
}
