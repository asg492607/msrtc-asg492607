import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { ServiceRegistry } from '../service-registry';

@Injectable()
export class ProxyMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    const pathParts = req.path.split('/');
    // Example path: /api/booking/trips
    if (pathParts.length >= 3 && pathParts[1] === 'api') {
      const serviceName = pathParts[2];
      const targetUrl = ServiceRegistry[serviceName];

      if (targetUrl) {
        const proxy = createProxyMiddleware({
          target: targetUrl,
          changeOrigin: true,
          pathRewrite: {
            [`^/api/${serviceName}`]: '/api/v1', // Assuming microservices use /api/v1
          },
        });
        return proxy(req, res, next);
      }
    }
    
    // Fallback if no matching route
    next();
  }
}
