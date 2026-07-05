import { Logger } from '@nestjs/common';
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
