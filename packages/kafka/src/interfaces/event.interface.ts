export interface EventEnvelope<T = any> {
  eventId: string;
  eventType: string;
  eventVersion: string;
  occurredAt: string;
  correlationId: string;
  producer: string;
  payload: T;
}

export interface PublishOptions {
  correlationId?: string;
  producer?: string;
  version?: string;
}
