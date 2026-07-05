import { Module, NestModule, MiddlewareConsumer } from '@nestjs/common';
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';
import { APP_GUARD } from '@nestjs/core';
import { CircuitBreakerProxyMiddleware } from './proxy/circuit-breaker.middleware';
import { SwaggerAggregatorController } from './swagger/swagger.controller';
// import { RedisModule } from '@msrtc/redis';

@Module({
  imports: [
    // RedisModule, // In reality, we'd use ThrottlerStorageRedisService
    ThrottlerModule.forRoot([{
      ttl: 60000, // 60 seconds
      limit: 100, // 100 requests per minute per IP
    }])
  ],
  controllers: [SwaggerAggregatorController],
  providers: [
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard
    }
  ],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(CircuitBreakerProxyMiddleware)
      .exclude('swagger-json') // Don't proxy the swagger endpoint itself
      .forRoutes('*');
  }
}
