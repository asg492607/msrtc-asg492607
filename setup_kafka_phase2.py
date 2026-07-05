import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\packages\kafka\src"

# 1. EventBus Service (Producer)
event_bus_svc = """import { Injectable, Logger } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "event-bus.service.ts"), "w", encoding="utf-8") as f: f.write(event_bus_svc)

# 2. Consumer Service
consumer_svc = """import { Injectable, Logger } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "consumer.service.ts"), "w", encoding="utf-8") as f: f.write(consumer_svc)


# 3. Module & Index
kafka_mod = """import { Module, Global } from '@nestjs/common';
import { EventBusService } from './event-bus.service';
import { ConsumerService } from './consumer.service';

@Global()
@Module({
  providers: [EventBusService, ConsumerService],
  exports: [EventBusService, ConsumerService],
})
export class KafkaModule {}
"""
with open(os.path.join(base_dir, "kafka.module.ts"), "w", encoding="utf-8") as f: f.write(kafka_mod)

index_ts = """export * from './kafka.module';
export * from './event-bus.service';
export * from './consumer.service';
export * from './interfaces/event.interface';
export * from './constants/topics';
"""
with open(os.path.join(base_dir, "index.ts"), "w", encoding="utf-8") as f: f.write(index_ts)


print("Kafka Package Phase 2 Scaffolded (EventBus, Consumer, DLQ Logic)")
