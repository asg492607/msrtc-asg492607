import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { FeatureFlagService } from './flags/services/feature-flag.service';
import { FeatureFlagController } from './flags/controllers/feature-flag.controller';
import { PrismaModule } from './prisma/prisma.module';
import { RedisModule } from '@msrtc/redis';
import { TenantModule, TenantMiddleware } from '@msrtc/tenant';

@Module({
  imports: [PrismaModule, RedisModule, TenantModule],
  controllers: [FeatureFlagController],
  providers: [FeatureFlagService],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
     consumer.apply(TenantMiddleware).forRoutes('*');
  }
}
