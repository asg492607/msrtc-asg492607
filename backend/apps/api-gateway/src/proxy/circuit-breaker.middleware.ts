import { Injectable, Logger, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import * as CircuitBreaker from 'opossum';

@Injectable()
export class CircuitBreakerProxyMiddleware implements NestMiddleware {
  private readonly logger = new Logger('CircuitBreaker');
  private breakers: Map<string, CircuitBreaker> = new Map();

  // Basic route map
  private readonly routes = {
    '/api/v1/auth': 'http://localhost:3001',
    '/api/v1/bookings': 'http://localhost:3002',
    '/api/v1/seats': 'http://localhost:3003',
  };

  use(req: Request, res: Response, next: NextFunction) {
    const targetUrl = this.resolveTarget(req.path);
    
    if (!targetUrl) {
      return next(); // Let Nest handle it or return 404
    }

    const breaker = this.getBreaker(targetUrl);

    // Fire the circuit breaker
    breaker.fire(req, res, next).catch(err => {
      this.logger.error(`Circuit Open for ${targetUrl}: ${err.message}`);
      res.status(503).json({
        statusCode: 503,
        message: 'Service Unavailable',
        details: 'The downstream service is currently experiencing instability. The circuit breaker has opened to prevent cascading failures.'
      });
    });
  }

  private resolveTarget(path: string): string | null {
    for (const [prefix, url] of Object.entries(this.routes)) {
      if (path.startsWith(prefix)) return url;
    }
    return null;
  }

  private getBreaker(target: string): CircuitBreaker {
    if (!this.breakers.has(target)) {
      const proxy = createProxyMiddleware({ target, changeOrigin: true });
      
      const breaker = new CircuitBreaker(
        (req: Request, res: Response, next: NextFunction) => {
          return new Promise((resolve, reject) => {
            // http-proxy-middleware acts on the response stream directly
            // For a robust breaker, we listen to proxy events
            (proxy as any)(req, res, (err: any) => {
               if (err) return reject(err);
               resolve(true);
            });
          });
        },
        {
          timeout: 5000,       // If downstream takes longer than 5s, trigger failure
          errorThresholdPercentage: 50, // Open circuit if 50% of requests fail
          resetTimeout: 30000  // After 30s, try 1 request to see if service is back
        }
      );

      breaker.fallback(() => Promise.reject(new Error('Circuit Open')));
      breaker.on('open', () => this.logger.warn(`CIRCUIT BREAKER TRIPPED for ${target}`));
      breaker.on('halfOpen', () => this.logger.log(`CIRCUIT BREAKER TESTING ${target}`));
      breaker.on('close', () => this.logger.log(`CIRCUIT BREAKER RECOVERED for ${target}`));

      this.breakers.set(target, breaker);
    }
    return this.breakers.get(target);
  }
}
