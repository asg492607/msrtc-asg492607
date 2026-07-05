import { Injectable } from '@nestjs/common';
import { HqRepository } from './repository/hq.repository';
import { AlertSeverity } from './enums/hq.enums';

@Injectable()
export class AlertService {
  constructor(private repository: HqRepository) {}

  async triggerAlert(title: string, message: string, severity: AlertSeverity) {
    const alert = await this.repository.saveAlert({ title, message, severity, triggeredAt: new Date() });
    
    if (severity === AlertSeverity.CRITICAL) {
      // Send WebSocket or Push notification to Executive App
      console.error(`[CRITICAL HQ ALERT] ${title}: ${message}`);
    }

    return alert;
  }
}
