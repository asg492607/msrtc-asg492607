import { Injectable, Logger } from '@nestjs/common';
import { EventEnvelope } from './interfaces/event.interface';

@Injectable()
export class ConsumerService {
  private readonly logger = new Logger(ConsumerService.name);

  // In production, inject CacheService / Redis for Idempotency
  constructor() {}

  async handleEvent(topic: string, envelope: EventEnvelope, handler: () => Promise<void>) {
    this.logger.log(`[Consumer] Received ${envelope.eventType} from ${topic}`);
    
    // 1. Idempotency Check
    const isProcessed = await this.checkIdempotency(envelope.eventId);
    if (isProcessed) {
      this.logger.warn(`[Consumer] Duplicate event ${envelope.eventId}. Ignoring.`);
      return;
    }

    try {
      // 2. Process
      await handler();
      
      // 3. Mark Processed
      await this.markProcessed(envelope.eventId);
    } catch (error) {
      this.logger.error(`[Consumer] Error processing ${envelope.eventId}`, error.stack);
      
      // 4. Trigger Retry & DLQ logic
      await this.handleFailure(topic, envelope, error);
    }
  }

  private async checkIdempotency(eventId: string): Promise<boolean> {
    // Check redis key `processed_events:${eventId}`
    return false;
  }

  private async markProcessed(eventId: string): Promise<void> {
    // Set redis key `processed_events:${eventId}` with 7-day TTL
  }

  private async handleFailure(topic: string, envelope: EventEnvelope, error: any) {
    // Pseudo logic for DLQ
    // const retryCount = envelope.retryCount || 0;
    // if (retryCount < 3) { retry... } else { route to ${topic}.dlq }
    this.logger.error(`[DLQ] Routing ${envelope.eventId} to ${topic}.dlq`);
  }
}
