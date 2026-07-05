import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\packages\tenant\src"

# 1. Tenant Middleware
mw = """import { Injectable, NestMiddleware } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "tenant.middleware.ts"), "w", encoding="utf-8") as f: f.write(mw)


# 2. Prisma Client Extension for RLS
prisma_ext = """import { PrismaClient } from '@prisma/client';
import { ClsService } from 'nestjs-cls';

// This function wraps an existing PrismaClient and injects a global 'where: { tenantId }' clause
export function withTenantContext(prisma: PrismaClient, cls: ClsService) {
  return prisma.$extends({
    query: {
      $allModels: {
        async $allOperations({ model, operation, args, query }) {
          const tenantId = cls.get('tenantId');
          
          if (!tenantId) {
             // If somehow executing outside of an HTTP context (e.g. cron), allow it or throw.
             return query(args);
          }

          // Check if the model actually has a tenantId field (we shouldn't inject it on models that don't belong to a tenant)
          // For simplicity in this mock, we assume models like 'Booking', 'Route' are tenant-aware.
          const modelsToScope = ['Booking', 'Route', 'Seat', 'Ticket', 'User'];
          
          if (modelsToScope.includes(model)) {
            // Append tenantId to the where clause
            if (operation === 'findMany' || operation === 'findFirst' || operation === 'findUnique') {
               args.where = { ...args.where, tenantId };
            }
            if (operation === 'update' || operation === 'updateMany' || operation === 'delete' || operation === 'deleteMany') {
               args.where = { ...args.where, tenantId };
            }
            if (operation === 'create' || operation === 'createMany') {
               args.data = Array.isArray(args.data) 
                 ? args.data.map(d => ({ ...d, tenantId }))
                 : { ...args.data, tenantId };
            }
          }

          return query(args);
        },
      },
    },
  });
}
"""
with open(os.path.join(base_dir, "prisma.extension.ts"), "w", encoding="utf-8") as f: f.write(prisma_ext)


# 3. Decorator
decorator = """import { createParamDecorator, ExecutionContext } from '@nestjs/common';
import { ClsServiceManager } from 'nestjs-cls';

export const CurrentTenant = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const cls = ClsServiceManager.getClsService();
    return cls.get('tenantId');
  },
);
"""
with open(os.path.join(base_dir, "tenant.decorator.ts"), "w", encoding="utf-8") as f: f.write(decorator)


# 4. Module & Index
module = """import { Module, Global, NestModule, MiddlewareConsumer } from '@nestjs/common';
import { ClsModule } from 'nestjs-cls';
import { TenantMiddleware } from './tenant.middleware';

@Global()
@Module({
  imports: [
    ClsModule.forRoot({
      global: true,
      middleware: { mount: false } // We mount our custom TenantMiddleware instead
    })
  ],
  exports: [ClsModule]
})
export class TenantModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(TenantMiddleware).forRoutes('*');
  }
}
"""
with open(os.path.join(base_dir, "tenant.module.ts"), "w", encoding="utf-8") as f: f.write(module)

index = """export * from './tenant.module';
export * from './tenant.middleware';
export * from './prisma.extension';
export * from './tenant.decorator';
"""
with open(os.path.join(base_dir, "index.ts"), "w", encoding="utf-8") as f: f.write(index)


print("Tenant Package Phase 2 Scaffolded (Middleware, Prisma Ext, Decorators)")
