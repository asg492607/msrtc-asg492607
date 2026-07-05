import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { FinOpsService } from './finops/services/finops.service';
import { FinOpsController } from './finops/controllers/finops.controller';
import { PrismaModule } from './prisma/prisma.module';
import { TenantModule, TenantMiddleware } from '@msrtc/tenant';

@Module({
  imports: [PrismaModule, TenantModule],
  controllers: [FinOpsController],
  providers: [FinOpsService],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
     consumer.apply(TenantMiddleware).forRoutes('*');
  }
}
