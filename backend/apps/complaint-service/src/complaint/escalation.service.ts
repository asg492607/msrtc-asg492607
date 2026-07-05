import { Injectable } from '@nestjs/common';
import { ComplaintRepository } from './repository/complaint.repository';
import { ComplaintStatus } from './enums/complaint.enums';

@Injectable()
export class EscalationService {
  constructor(private repository: ComplaintRepository) {}

  async escalateComplaint(id: string) {
    // In real app, this might be triggered by a Cron Job if SLA is breached
    await this.repository.updateStatus(id, ComplaintStatus.ESCALATED);
    // Trigger Kafka event for HQ Admin notification
    return { message: 'Complaint escalated successfully.' };
  }
}
