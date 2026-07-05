import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { DemandService } from './ai/services/demand.service';
import { FeatureStoreService } from './ai/services/feature-store.service';
import { PredictionController } from './ai/controllers/prediction.controller';
import { PrismaModule } from './prisma/prisma.module';
import { KafkaModule } from '@msrtc/kafka';
import { RedisModule } from '@msrtc/redis';
import { TenantModule, TenantMiddleware } from '@msrtc/tenant';

@Module({
  imports: [PrismaModule, KafkaModule, RedisModule, TenantModule],
  controllers: [PredictionController],
  providers: [DemandService, FeatureStoreService],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
     // Apply the shared TenantMiddleware from Task 32
     consumer.apply(TenantMiddleware).forRoutes('*');
  }
}
