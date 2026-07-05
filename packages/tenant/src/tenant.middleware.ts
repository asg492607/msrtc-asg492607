import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class TenantMiddleware implements NestMiddleware {
  constructor(private readonly cls: ClsService) {}

  use(req: Request, res: Response, next: NextFunction) {
    // 1. Try to resolve from Header
    let tenantId = req.headers['x-tenant-id'] as string;

    // 2. Try to resolve from JWT payload (if auth middleware ran before this)
    if (!tenantId && req.user && (req.user as any).tenantId) {
       tenantId = (req.user as any).tenantId;
    }

    // 3. Fallback to default tenant if none provided (for initial setup or monolithic default)
    if (!tenantId) {
      tenantId = 'default-tenant';
    }

    // Inject into global AsyncLocalStorage context
    this.cls.set('tenantId', tenantId);
    next();
  }
}
