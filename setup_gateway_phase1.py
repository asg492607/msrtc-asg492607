import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\api-gateway"
src_dir = os.path.join(base_dir, "src")

# Ensure package.json has proxy middleware
pkg_json = """{
  "name": "api-gateway",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "build": "nest build",
    "start": "nest start",
    "start:dev": "nest start --watch"
  },
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/swagger": "^7.0.0",
    "@nestjs/axios": "^3.0.0",
    "axios": "^1.6.0",
    "http-proxy-middleware": "^2.0.6",
    "class-validator": "^0.14.0",
    "class-transformer": "^0.5.1"
  }
}
"""
os.makedirs(base_dir, exist_ok=True)
with open(os.path.join(base_dir, "package.json"), "w", encoding="utf-8") as f: f.write(pkg_json)

dirs = [
    "middleware",
    "interceptors",
    "health",
    "auth",
]

for d in dirs:
    os.makedirs(os.path.join(src_dir, d), exist_ok=True)


# 1. Routing Config
routing_ts = """export const ServiceRegistry = {
  'auth': 'http://localhost:3001',
  'booking': 'http://localhost:3002',
  'seat': 'http://localhost:3003',
  'route': 'http://localhost:3004',
  'payment': 'http://localhost:3005',
  'ticket': 'http://localhost:3006',
  'gps': 'http://localhost:3007',
  'notification': 'http://localhost:3008',
  'complaint': 'http://localhost:3009',
  'pass': 'http://localhost:3010',
  'parcel': 'http://localhost:3011',
  'crew': 'http://localhost:3014',
  'depot': 'http://localhost:3015',
  'maintenance': 'http://localhost:3016',
  'finance': 'http://localhost:3017',
  'hq': 'http://localhost:3018',
};
"""
with open(os.path.join(src_dir, "service-registry.ts"), "w", encoding="utf-8") as f: f.write(routing_ts)


# 2. Proxy Middleware
proxy_middleware = """import { Injectable, NestMiddleware } from '@nestjs/common';
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
"""
with open(os.path.join(src_dir, "middleware/proxy.middleware.ts"), "w", encoding="utf-8") as f: f.write(proxy_middleware)


# 3. Interceptor
correlation_interceptor = """import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
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
"""
with open(os.path.join(src_dir, "interceptors/correlation-id.interceptor.ts"), "w", encoding="utf-8") as f: f.write(correlation_interceptor)


print("Gateway Phase 1 Scaffolded (Proxy Middleware, Routing Map, Interceptors)")
