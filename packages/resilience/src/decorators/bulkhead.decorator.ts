import { Logger } from '@nestjs/common';
import * as CircuitBreaker from 'opossum';

// This decorator utilizes opossum's capacity limits to create a Bulkhead.
// If concurrent executions exceed 'capacity', requests are rejected instantly.
export function Bulkhead(capacity: number) {
  const logger = new Logger('Bulkhead');

  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    // We instantiate one breaker/bulkhead instance for this method prototype
    const breaker = new CircuitBreaker(
      function(context: any, args: any[]) {
        return originalMethod.apply(context, args);
      },
      {
        capacity,
        timeout: 30000, // generic fallback
        errorThresholdPercentage: 100 // we only want the bulkhead feature here, not the breaker
      }
    );

    breaker.fallback(() => Promise.reject(new Error(`Bulkhead Rejected: ${propertyKey} exceeds maximum capacity of ${capacity} concurrent executions.`)));
    
    breaker.on('reject', () => logger.warn(`[${propertyKey}] Bulkhead execution rejected. Threads saturated.`));

    descriptor.value = async function (...args: any[]) {
      // opossum breaker requires passing the 'this' context explicitly to the function wrapped
      return breaker.fire(this, args);
    };

    return descriptor;
  };
}
