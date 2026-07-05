import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { v4 as uuidv4 } from 'uuid'; // Need to install uuid, mocking uuid generation here for now

@Injectable()
export class CorrelationIdInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const correlationId = request.headers['x-correlation-id'] || `CORR-${Math.floor(Date.now() / 1000)}`;
    request.headers['x-correlation-id'] = correlationId;
    return next.handle();
  }
}
