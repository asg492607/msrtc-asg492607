import { Injectable, Logger } from '@nestjs/common';
import { v4 as uuidv4 } from 'uuid';
import { EventEnvelope, PublishOptions } from './interfaces/event.interface';

@Injectable()
export class EventBusService {
  private readonly logger = new Logger(EventBusService.name);

  // In production, inject ClientKafka
  constructor() {}

  async publish<T>(eventType: string, payload: T, options?: PublishOptions): Promise<EventEnvelope<T>> {
    const envelope: EventEnvelope<T> = {
      eventId: uuidv4(),
      eventType,
      eventVersion: options?.version || '1.0',
      occurredAt: new Date().toISOString(),
      correlationId: options?.correlationId || uuidv4(),
      producer: options?.producer || 'unknown-service',
      payload,
    };

    try {
      // clientKafka.emit(topic, envelope)
      this.logger.log(`[EventBus] Published ${eventType} (EventId: ${envelope.eventId})`);
      return envelope;
    } catch (error) {
      this.logger.error(`[EventBus] Failed to publish ${eventType}`, error.stack);
      throw error;
    }
  }
}
