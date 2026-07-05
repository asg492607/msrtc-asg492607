import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\packages\resilience\src"

# 1. Retryable Decorator
retry_decorator = """import { Logger } from '@nestjs/common';
import { throwError, timer, lastValueFrom, from, Observable } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';

export interface RetryOptions {
  maxAttempts?: number;
  initialDelayMs?: number;
  backoffMultiplier?: number;
}

export function Retryable(options: RetryOptions = {}) {
  const maxAttempts = options.maxAttempts || 3;
  const initialDelayMs = options.initialDelayMs || 1000;
  const backoffMultiplier = options.backoffMultiplier || 2;
  const logger = new Logger('Retryable');

  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const source$ = new Observable(observer => {
        // Execute the original Promise/Async method
        Promise.resolve(originalMethod.apply(this, args))
          .then(res => {
            observer.next(res);
            observer.complete();
          })
          .catch(err => observer.error(err));
      });

      const result$ = source$.pipe(
        retry({
          count: maxAttempts,
          delay: (error, retryCount) => {
            const delay = initialDelayMs * Math.pow(backoffMultiplier, retryCount - 1);
            // Add 10-20% Jitter
            const jitter = delay * 0.1 * Math.random();
            const totalDelay = delay + jitter;
            
            logger.warn(`[${propertyKey}] Attempt ${retryCount}/${maxAttempts} failed. Retrying in ${Math.round(totalDelay)}ms. Error: ${error.message}`);
            return timer(totalDelay);
          }
        }),
        catchError(err => {
          logger.error(`[${propertyKey}] All ${maxAttempts} retry attempts failed.`);
          return throwError(() => err);
        })
      );

      return lastValueFrom(result$);
    };

    return descriptor;
  };
}
"""
with open(os.path.join(base_dir, "decorators/retryable.decorator.ts"), "w", encoding="utf-8") as f: f.write(retry_decorator)


# 2. WithTimeout Decorator
timeout_decorator = """import { Logger } from '@nestjs/common';
import { throwError, timer, lastValueFrom, Observable } from 'rxjs';
import { timeout, catchError } from 'rxjs/operators';

export function WithTimeout(ms: number) {
  const logger = new Logger('WithTimeout');

  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const source$ = new Observable(observer => {
        Promise.resolve(originalMethod.apply(this, args))
          .then(res => {
            observer.next(res);
            observer.complete();
          })
          .catch(err => observer.error(err));
      });

      const result$ = source$.pipe(
        timeout({
          each: ms,
          with: () => {
             logger.error(`[${propertyKey}] Execution exceeded timeout of ${ms}ms.`);
             return throwError(() => new Error(`Execution Timeout: ${propertyKey} exceeded ${ms}ms`));
          }
        })
      );

      return lastValueFrom(result$);
    };

    return descriptor;
  };
}
"""
with open(os.path.join(base_dir, "decorators/with-timeout.decorator.ts"), "w", encoding="utf-8") as f: f.write(timeout_decorator)


# 3. Bulkhead Decorator
bulkhead_decorator = """import { Logger } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "decorators/bulkhead.decorator.ts"), "w", encoding="utf-8") as f: f.write(bulkhead_decorator)


# 4. Index
index = """export * from './decorators/retryable.decorator';
export * from './decorators/with-timeout.decorator';
export * from './decorators/bulkhead.decorator';
"""
with open(os.path.join(base_dir, "index.ts"), "w", encoding="utf-8") as f: f.write(index)


print("Resilience Package Phase 2 Scaffolded (Decorators)")
