import { Injectable, Logger } from '@nestjs/common';
import { EventBusService, Topics } from '@msrtc/kafka';

@Injectable()
export class AutomationService {
  private readonly logger = new Logger(AutomationService.name);

  constructor(private eventBus: EventBusService) {}

  async executeCommand(topic: string, payload: any) {
    this.logger.log(`Dispatching automation command to topic: ${topic}`);
    await this.eventBus.publish(topic, {
      type: 'automation.execute',
      timestamp: new Date().toISOString(),
      ...payload
    });
  }
}
