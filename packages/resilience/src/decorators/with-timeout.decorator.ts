import { Logger } from '@nestjs/common';
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
