import { PrismaClient } from '@prisma/client';
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
